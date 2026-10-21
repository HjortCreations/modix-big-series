"""Build reusable Modix BIG overlays and slicer presets, entirely offline."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def component(group, ident, ancestors=()):
    if not re.fullmatch(r'[a-z0-9.-]+', ident):
        raise ValueError('Invalid component identifier')
    if ident in ancestors:
        raise ValueError('Circular component inheritance')
    value = read(f'{group}/{ident}.json')
    if 'base' in value:
        parent = component(group, value['base'], (*ancestors, ident))
        value = {**parent, **value, 'settings': {**parent.get('settings', {}), **value.get('settings', {})}}
    return value

def text(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')

def template(path, substitutions=None):
    value = text(path)
    for key, replacement in (substitutions or {}).items():
        value = value.replace('@' + key + '@', str(replacement))
    if re.search(r'@[A-Z_]+@', value):
        raise ValueError('Unresolved template: ' + path)
    return value

def start_code(process, material, head, max_feedrate=None, insets=None):
    left,front,right,rear = insets or head['nozzle_insets_mm']
    substitutions = dict(PRINT_ACCEL=process['print_acceleration'],
                         TRAVEL_ACCEL=read('slicer/common/startup.json')['travel_acceleration'],
                         MAX_FEEDRATE=max_feedrate or '', PA=material['pressure_advance'],
                         LEFT=left, FRONT=front, RIGHT=right, REAR=rear)
    value = template('slicer/gcode/start.gcode', substitutions)
    if max_feedrate is None:
        value = value.replace(' ; Axis limits, mm/min', '; Keep the existing machine axis speed limits')
    if material['pressure_advance'] is None:
        # The all-in-one starter uses the selected filament's own PA command.
        value = ''.join(line for line in value.splitlines(keepends=True) if not line.startswith('M572 '))
    return value

def bed_wrapper(head, insets):
    left,front,right,rear = insets
    call = f'M98 P"g32_u.g" H"{head["name"]}" A{left} B{front} C{right} E{rear} S{{var.force}}'
    return ('; Toolhead clearance wrapper; independent of machine size and nozzle.\n'
            'var force = 0\nif exists(param.S)\n    set var.force = param.S\n'
            'if exists(param.D)\n    '+call+' D{param.D}\nelse\n    '+call+'\n').encode()

def profile_files(selection):
    """Print/material presets and head setup, without reading any machine model."""
    tool = component('slicer/toolheads', selection['toolhead'])
    head = component('config/toolheads', tool['head'])
    process = component('slicer/processes', selection['process'])
    material = component('slicer/materials', selection['material'])
    groups = {g:read(f'slicer/common/{g}.json') for g in ['print','filament']}
    groups['print'].update(process['settings'])
    groups['filament'].update(material['settings'])
    groups['print']['print_settings_id'] = 'BIG '+process['name']
    groups['filament']['filament_settings_id'] = '"BIG '+material['name']+'"'
    groups['print']['notes'] = 'Reusable BIG process; shared start G-code controls motion and pressure advance.'
    groups['filament']['filament_notes'] = '"Working material/nozzle settings; maximum throughput is not independently measured."'
    bundle = '# Machine-independent print and filament presets; Import Config Bundle.\n'
    for group,settings in groups.items():
        name = 'BIG '+(process if group=='print' else material)['name']
        bundle += '\n['+group+':'+name+']\n'+''.join(f'{k} = {v}\n' for k,v in sorted(settings.items()))
    return {'PrusaSlicer-process-material.ini':bundle.encode(),
            'gcode/start.gcode':start_code(process,material,head).encode(),
            'gcode/end.gcode':text('slicer/gcode/end.gcode').encode(),
            'gcode/before-layer.gcode':text('slicer/gcode/before-layer.gcode').encode(),
            'toolhead-settings-reference.json':(json.dumps({**{k:v for k,v in read('slicer/common/printer.json').items()
              if k in ['gcode_flavor','autoemit_temperature_commands','use_firmware_retraction','use_volumetric_e',
                       'retract_layer_change','retract_before_wipe','wipe']}, **tool['settings']},indent=2)+'\n').encode(),
            'README.md':text('slicer/README.md').encode()}

def macro_files():
    files = {name:text('macros/'+name).encode() for name in ['stop.g','adaptive_mesh.g','g32_u.g','axis_test.g']}
    for ident in ['griffin','griffin-high-flow','griffin-ultra']:
        head = component('config/toolheads',ident)
        files['bed-'+ident+'.g'] = bed_wrapper(head,head['nozzle_insets_mm'])
    files['README.md'] = text('macros/README.md').encode()
    return files

def starter_groups():
    """Ready-to-import presets; machine dimensions never select material/process values."""
    selection = read('slicer/starter.json')
    process = component('slicer/processes', selection['process'])
    print_name = process['name']
    printing = {**read('slicer/common/print.json'), **process['settings']}
    printing.update(print_settings_id=print_name,
                    compatible_printers_condition='printer_notes=~/.*HC_PROFILE_FAMILY=MODIX_BIG;.*/',
                    notes='Generic BIG starting process; change layer height to suit your nozzle and part.')
    groups = {'print:'+print_name: printing}
    machines = read('slicer/machines.json')['models']
    estimates = component('config/motion', 'nema23-250')['slicer_time_estimates']
    estimates.update(machine_max_feedrate_y='250,250', machine_max_feedrate_z='6.6667,6.6667',
                     machine_max_acceleration_extruding='250,250', machine_max_acceleration_travel='800,800')
    for variant in selection['variants']:
        tool = component('slicer/toolheads', variant['toolhead'])
        head = component('config/toolheads', tool['head'])
        material = component('slicer/materials', variant['material'])
        filament_name = material['name']
        filament = {**read('slicer/common/filament.json'), **material['settings']}
        filament.update(filament_settings_id=json.dumps(filament_name),
                        compatible_printers_condition=f'printer_notes=~/.*HC_PROFILE_FAMILY=MODIX_BIG;.*/ and printer_notes=~/.*HC_TOOLHEAD={tool["head"]};.*/',
                        start_filament_gcode=json.dumps(f'M572 S{material["pressure_advance"]} ; Basic start value for the {head["name"]} toolhead'),
                        filament_notes=json.dumps('Starting values for tuning; 45 s cooling target can be limited by the minimum print speed.'))
        groups['filament:'+filament_name] = filament
        for ident,machine in machines.items():
            if not machine.get('starter_enabled', True):
                continue
            bounds = (component('config/models', machine['model'])['variants'][machine['geometry_variant']]['axis_max']
                      if 'model' in machine else machine['axis_max'])
            if len(bounds) != 3 or min(bounds) <= 0 or bounds[2] > 1200:
                raise ValueError('Invalid starter build volume')
            name = 'Hjort Creations - '+machine['name']+' - '+variant['label']
            printer = {**read('slicer/common/printer.json'), **tool['settings'], **estimates}
            printer.update(printer_settings_id=name, printer_model=machine['name'], printer_variant=printer['nozzle_diameter'],
                           printer_vendor='', use_relative_e_distances='1', silent_mode='0', variable_layer_height='1',
                           bed_shape=f'0x0,{bounds[0]}x0,{bounds[0]}x{bounds[1]},0x{bounds[1]}', max_print_height=str(bounds[2]),
                           default_print_profile=print_name, default_filament_profile=json.dumps(filament_name),
                           printer_notes=json.dumps(f'HC_PROFILE_FAMILY=MODIX_BIG; HC_TOOLHEAD={tool["head"]}; Single-tool RRF reference; verify actual travel and install required shared macros.'),
                           start_gcode=start_code(process, {'pressure_advance':None}, head).rstrip().replace('\n', r'\n'),
                           end_gcode=text('slicer/gcode/end.gcode').rstrip().replace('\n', r'\n'),
                           before_layer_gcode=text('slicer/gcode/before-layer.gcode').rstrip().replace('\n', r'\n'),
                           host_type='duet', print_host='', printhost_apikey='')
            groups['printer:'+name] = printer
    default_model = machines[selection['default_model']]['name']
    groups['presets'] = {'print':print_name, 'filament':component('slicer/materials',selection['variants'][0]['material'])['name'],
                         'printer':'Hjort Creations - '+default_model+' - '+selection['variants'][0]['label']}
    return groups

def starter_bundle():
    groups = starter_groups()
    value = '# Hjort Creations Modix BIG starter profiles. Import Config Bundle in PrusaSlicer.\n'
    for name,settings in groups.items():
        value += '\n['+name+']\n'+''.join(f'{k} = {v}\n' for k,v in sorted(settings.items()))
    return value.encode('utf-8')

def compose(recipe):
    model = component('config/models', recipe['model'])
    variant = model['variants'][recipe['geometry_variant']]
    hardware = component('config/hardware', recipe['hardware'])
    tool = component('slicer/toolheads', recipe['toolhead'])
    head = component('config/toolheads', tool['head'])
    process = component('slicer/processes', recipe['process'])
    material = component('slicer/materials', recipe['material'])
    motion = component('config/motion', recipe['motion'])
    if hardware['z_motors'] != 4 or hardware['idex']:
        raise ValueError('Only single-tool Cartesian four-Z hardware is supported')
    bounds = recipe.get('axis_max', variant['axis_max'])
    minima = model['axis_min']
    if len(bounds) != 3 or any(b <= a for a, b in zip(minima, bounds)):
        raise ValueError('Invalid work envelope')
    left, front, right, rear = recipe.get('nozzle_insets_mm', head['nozzle_insets_mm'])
    if min(left, front, right, rear) < 2:
        raise ValueError('Nozzle insets must be at least2mm')
    groups = {g: read(f'slicer/common/{g}.json') for g in ['print', 'filament', 'printer']}
    groups['print'].update(process['settings'])
    groups['filament'].update(material['settings'])
    printer = groups['printer']
    printer.update(tool['settings'])
    printer.update(motion['slicer_time_estimates'])
    printer['bed_shape'] = f'{minima[0]}x{minima[1]},{bounds[0]}x{minima[1]},{bounds[0]}x{bounds[1]},{minima[0]}x{bounds[1]}'
    printer['max_print_height'] = str(bounds[2])
    printer['start_gcode'] = start_code(process, material, head, motion['max_feedrate_command'],
                                       [left,front,right,rear]).rstrip().replace('\n', r'\n')
    printer['end_gcode'] = text('slicer/gcode/end.gcode').rstrip().replace('\n', r'\n')
    printer['before_layer_gcode'] = text('slicer/gcode/before-layer.gcode').rstrip().replace('\n', r'\n')
    printer.update(host_type='duet', print_host='', printhost_apikey='')
    names = {'print': 'BIG ' + process['name'], 'filament': 'BIG ' + material['name'],
             'printer': 'BIG ' + recipe['model'] + '-' + recipe['geometry_variant'] + '-' + recipe['toolhead']}
    groups['print']['print_settings_id'] = names['print']
    groups['filament']['filament_settings_id'] = '"' + names['filament'] + '"'
    printer['printer_settings_id'] = names['printer']
    printer['printer_notes'] = '"Requires matching BIG macros and commissioned machine configuration; no calibration included."'
    groups['print']['notes'] = 'Reusable BIG process; shared start G-code controls motion and pressure advance.'
    groups['filament']['filament_notes'] = '"Working material/nozzle settings; maximum throughput is not independently measured."'
    for key in groups['print']:
        if key.endswith('_acceleration'):
            groups['print'][key] = '0'
    flat = {k: v for group in groups.values() for k, v in group.items()}
    files = {'sys/' + name: text('macros/' + name).encode() for name in ['stop.g', 'g32_u.g', 'axis_test.g']}
    files['sys/bed.g'] = bed_wrapper(head,[left,front,right,rear])
    files['sys/adaptive_mesh.g'] = text('macros/adaptive_mesh.g').encode()
    for name in ['homeall.g', 'homez.g', 'homex.g', 'homey.g']:
        home_front = recipe.get('home_front_mm', head['home_front_mm'])
        before_z = ''
        if tool['head'] == 'griffin-ultra':
            before_z = f'G1 X{{move.axes[0].min+5}} Y{{move.axes[1].min+{home_front}}} F5000 ; ULTRA front clearance before probing'
        files['sys/' + name] = template('firmware/hardware/duet2-duex5/' + hardware['homing'] + '/' + name + '.in',
                                         dict(HOME_FRONT=home_front, HOME_BEFORE_Z=before_z)).encode()
    # Geometry is a comparison reference, never an automatically loaded override.
    geometry = '; Reference only: verify actual travel and screw order before applying.\n'
    geometry += 'M208 ' + ' '.join(a+str(v) for a,v in zip('XYZ', minima)) + ' S1\n'
    geometry += 'M208 ' + ' '.join(a+str(v) for a,v in zip('XYZ', bounds)) + ' S0\n'
    geometry += 'M671 X' + ':'.join(map(str, model['screw_x'])) + ' Y' + ':'.join(map(str, model['screw_y'])) + ' S30\n'
    files['reference/config_model.g'] = geometry.encode()
    files['PrusaSlicer.ini'] = ('# Generated configuration; Import Config.\n' + ''.join(f'{k} = {v}\n' for k,v in sorted(flat.items()))).encode()
    bundle = '# Generated presets; Import Config Bundle.\n'
    for group, settings in groups.items():
        bundle += '\n[' + group + ':' + names[group] + ']\n'
        bundle += ''.join(f'{k} = {v}\n' for k,v in sorted(settings.items()))
    files['PrusaSlicer-bundle.ini'] = bundle.encode()
    manifest = {'schema_version':1, 'recipe':recipe,
                'requires':{'RRF_minimum':'3.5.3', 'kinematics':'Cartesian XYZ, BLTouch0, four independent Z motors',
                            'primary_tool_heaters':head['required_primary_tool_heaters'],
                            'base_config':'Existing commissioned Modix config.g with matching M584/M671/G31/PID/tool/fan mapping',
                            'homing':'Matching full/Z homing cache hooks installed with conditional G32'},
                'status':'Offline built; no physical installation or test performed by this build',
                'files':{k:hashlib.sha256(v).hexdigest() for k,v in sorted(files.items())}}
    files['manifest.json'] = (json.dumps(manifest, indent=2)+'\n').encode()
    return files, groups

def build(recipe_path, destination):
    files, _ = compose(json.loads(recipe_path.read_text(encoding='utf-8-sig')))
    destination.mkdir(parents=True, exist_ok=True)
    for name, value in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)
    return files

def archive(name, files):
    destination = ROOT/'dist'/name
    for path,value in files.items():
        target = destination/path
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(value)
    with zipfile.ZipFile(ROOT/'dist'/(name+'.zip'),'w',zipfile.ZIP_DEFLATED) as output:
        for path,value in sorted(files.items()):
            info=zipfile.ZipInfo(path,(2026,10,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            output.writestr(info,value)
    print('Built '+name)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--macros', action='store_true')
    parser.add_argument('--profiles', action='store_true')
    parser.add_argument('--starter', action='store_true')
    args = parser.parse_args()
    if args.all or args.starter:
        destination = ROOT/'dist'/read('slicer/starter.json')['filename']
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(starter_bundle())
        print('Built '+destination.name)
    if args.all or args.macros:
        archive('shared-macros',macro_files())
        for name in ['stop.g','adaptive_mesh.g']:
            (ROOT/'dist'/name).write_bytes((ROOT/'macros'/name).read_bytes())
    if args.all or args.profiles:
        for ident,selection in read('slicer/profiles.json').items():
            archive('profile-'+ident,profile_files(selection))
    if args.all:
        for recipe in sorted((ROOT/'recipes').glob('*.json')):
            files = build(recipe, ROOT/'dist'/recipe.stem)
            archive('example-'+recipe.stem,files)
    elif args.recipe and args.output:
        build(args.recipe.resolve(), args.output.resolve())
    elif not args.macros and not args.profiles and not args.starter:
        parser.error('Use --all, --starter, --profiles, --macros or --recipe FILE --output DIRECTORY')

if __name__ == '__main__':
    main()
