"""Structural, privacy and numeric regression checks; no printer access."""
import configparser
import hashlib
import json
from pathlib import Path
import re
import subprocess
from types import SimpleNamespace as NS
from build import ROOT, compose, read, text, macro_files, profile_files, starter_groups, starter_bundle

def expression(source, variables, axes, offsets, params=None):
    for index, axis in enumerate(axes):
        for field,value in axis.items():
            source = source.replace(f'move.axes[{index}].{field}', str(value))
    for index,value in enumerate(offsets):
        source = source.replace(f'sensors.probes[0].offsets[{index}]', str(value))
    for key,value in (params or {}).items():
        source = source.replace('param.'+key, str(value))
    source = re.sub(r'var\.(\w+)', lambda m: str(variables[m[1]]), source)
    return eval(source, {'__builtins__':{}}, {'min':min, 'max':max, 'abs':abs})

def variable(source, name, variables, axes, offsets, params=None):
    line = re.search(r'^var '+name+r' = (.+)$', source, re.M)[1]
    variables[name] = expression(line, variables, axes, offsets, params)

def composition():
    recipes = sorted((ROOT/'recipes').glob('*.json'))
    assert recipes
    for path in recipes:
        recipe = json.loads(path.read_text())
        files, groups = compose(recipe)
        assert 'sys/config.g' not in files
        assert len([k for k in files if k.startswith('sys/')]) == 9
        assert files['sys/stop.g'] == (ROOT/'macros/stop.g').read_bytes()
        assert files['sys/g32_u.g'] == (ROOT/'macros/g32_u.g').read_bytes()
        assert files['sys/adaptive_mesh.g'] == (ROOT/'macros/adaptive_mesh.g').read_bytes()
        assert all(not re.search(rb'@[A-Z_]+@', data) for data in files.values())
        manifest = json.loads(files['manifest.json'])
        assert all(hashlib.sha256(files[k]).hexdigest()==sha for k,sha in manifest['files'].items())
        assert all(v == '0' for k,v in groups['print'].items() if k.endswith('_acceleration'))
        printer = groups['printer']
        assert printer['print_host'] == printer['printhost_apikey'] == ''
        assert groups['filament']['bed_temperature'] == groups['filament']['first_layer_bed_temperature'] == '0'
        start = printer['start_gcode']
        assert start.index('M104') < start.index('G28') < start.index('G32') < start.index('adaptive_mesh.g') < start.index('T0') < start.index('M109')
        assert '{"if !move.axes[2].homed"}' in start and 'G28 X Y' in start
        assert [c.split(';')[0].strip() for c in printer['end_gcode'].split(r'\n')] == ['M400','M300 S222 P1111','M0']
        for name in ['homeall.g','homez.g']:
            homing = files['sys/'+name].decode()
            assert homing.index('set global.bigUTiltValid = false') < homing.index('G30')
            assert homing.index('M99') < homing.index('M98 P"config_probe.g"')
        bundle = configparser.ConfigParser(interpolation=None)
        bundle.read_string(files['PrusaSlicer-bundle.ini'].decode())
        assert len(bundle.sections()) == 3
        for group, settings in groups.items():
            name = next(s for s in bundle.sections() if s.startswith(group+':'))
            assert dict(bundle[name]) == settings
    main = read('recipes/big-meter-ultra-1.8.json')
    other = read('examples/big-120z-ultra-1.8.json')
    files,a = compose(main)
    _,b = compose(other)
    assert a['print'] == b['print'] and a['filament'] == b['filament']
    assert a['printer']['bed_shape'] != b['printer']['bed_shape']
    bad = dict(main, axis_max=[0,100,100])
    try:
        compose(bad)
        raise AssertionError('Invalid envelope accepted')
    except ValueError:
        pass
    return len(recipes)

def geometry():
    u = text('macros/g32_u.g')
    assert '#move.axes[2].drivers != 4' in u
    assert 'sensors.probes[0].type != 9' in u
    assert 'global.bigUTiltValid && move.axes[2].homed && global.bigUTiltHead = param.H' in u
    assert u.index('set global.bigUTiltValid = false') < u.index('while true')
    assert u.rindex('set global.bigUTiltValid = true') > u.index('abort "BIG U tilt did not reach')
    assert re.findall(r'G30 P(\d)',u) == list('01233210')
    assert not re.search(r'^\s*(?:G\d+|M\d+|T-?\d+)\b',u.split('        M99',1)[0],re.M)
    count=0
    for width,depth in [(600,600),(965,980),(980,1000),(1200,600),(1800,600)]:
        for offsets in [[0,32],[8,-20],[-25,-15],[100,80],[-100,-80]]:
            for head in ['griffin','griffin-ultra']:
                insets = read('config/toolheads/'+head+'.json')['nozzle_insets_mm']
                axes=[{'min':0,'max':width},{'min':0,'max':depth}]
                v=dict(zip(['inset_left','inset_front','inset_right','inset_rear'],insets))
                for name in ['edge_margin','probe_left','probe_right','probe_front','probe_rear']:
                    variable(u,name,v,axes,offsets)
                for axis,size,low,high in [(0,width,'probe_left','probe_right'),(1,depth,'probe_front','probe_rear')]:
                    assert 2 <= v[low] < v[high] <= size-2
                    assert insets[axis] <= v[low]-offsets[axis] <= v[high]-offsets[axis] <= size-insets[axis+2]
                recipe=dict(read('recipes/big-meter-ultra-1.8.json'),toolhead='ultra-1.8' if head=='griffin-ultra' else 'griffin-0.8')
                files,_=compose(recipe)
                mesh=files['sys/adaptive_mesh.g'].decode()
                for bounds in [(0,0,10,10),(width-10,depth-10,width,depth),(100,100,150,150),(0,0,width,depth)]:
                    params=dict(zip('XYAB',bounds));m=dict(zip(['inset_left','inset_front','inset_right','inset_rear'],insets))
                    for name in ['ox','oy','safe_min_x','safe_max_x','safe_min_y','safe_max_y','mesh_min_x','mesh_max_x','mesh_min_y','mesh_max_y']:
                        variable(mesh,name,m,axes,offsets,params)
                    assert m['safe_min_x'] <= m['mesh_min_x'] < m['mesh_max_x'] <= m['safe_max_x']
                    assert m['safe_min_y'] <= m['mesh_min_y'] < m['mesh_max_y'] <= m['safe_max_y']
                    assert m['mesh_max_x']-m['mesh_min_x'] >= 59.999
                    assert m['mesh_max_y']-m['mesh_min_y'] >= 59.999
                    count += 1
    return count

def stop_checks():
    stop=text('macros/stop.g')
    e=re.findall(r'^\s*set var.parkDeltaZ = (max\(.+)$',stop,re.M)[-1]
    count=0
    for maximum in [250,1000,1200]:
        for z in [0,245,295,300,600,maximum-1,maximum,maximum+1]:
            d=expression(e,{},[{}, {}, {'max':maximum,'machinePosition':z}],[])
            assert d >= 0
            assert z >= maximum or z+d <= maximum
            assert z >= min(300,maximum) or z+d >= min(300,maximum)
            count += 1
    assert 'G53 G1 X1 Y1 F6000' in stop and 'M84 X Y E0:1' in stop
    assert not re.search(r'^\s*(?:G28|M18)\b',stop,re.M)
    prefix=stop.split('var parkDeltaZ')[0];translated=[]
    for line in prefix.splitlines():
        if not line.strip() or line.lstrip().startswith(';'):continue
        line=re.sub(r'#(tools\[state.currentTool\]\.(?:extruders|heaters))',r'len(\1)',line)
        line=re.sub(r'\bvar (\w+) =',r'v.\1 =',line)
        line=line.replace('set var.','v.').replace('var.','v.').replace('false','False').replace('true','True').replace('&&',' and ')
        if line.lstrip().startswith(('if ','while ')):line+=':'
        translated.append(line)
    guard=compile('\n'.join(translated),'actual stop guard','exec')
    for tool,heaters,temperatures,expect in [(-1,[],[25],False),(0,[],[200],False),(0,[0],[25],False),(0,[0],[200],True),(0,[0,2],[200,0,25],False),(0,[0,2],[200,0,200],True)]:
        v=NS()
        exec(guard,{'__builtins__':{'len':len},'v':v,'state':NS(currentTool=tool),'tools':[NS(extruders=[0],heaters=heaters)],'heat':NS(coldRetractTemperature=90,heaters=[NS(current=t) for t in temperatures])})
        assert v.canRetract is expect
    return count

def privacy():
    patterns=[r'\b(?:\d{1,3}\.){3}\d{1,3}\b',r'\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b',
              r'(?m)^\s*M(?:551|587)\b',r'(?m)^\s*(?:printhost_apikey|print_host)\s*=\s*\S+',
              r'\bgh[pousr]_[A-Za-z0-9]{20,}\b',r'\b[A-Z0-9]{5}(?:-[A-Z0-9]{5}){5}\b']
    allowed={'macros','firmware','config','slicer','recipes','examples','tools','docs','.github'}
    tracked = set()
    if (ROOT/'.git').exists():
        tracked = set(subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0'))
    for path in ROOT.rglob('*'):
        if not path.is_file():continue
        rel=path.relative_to(ROOT)
        if '.git' in rel.parts:continue
        if rel.as_posix() not in tracked and any(p in {'dist','__pycache__','local','private','validation-local'} for p in rel.parts):continue
        if len(rel.parts)>1:assert rel.parts[0] in allowed,rel
        value=path.read_text(encoding='utf-8-sig')
        # Catch UTF-8 text accidentally decoded as Windows-1252 before saving.
        for broken in ['\ufffd', '\u00c2', '\u00c3', '\u00e2\u20ac', '\u00e2\u2020']:
            assert broken not in value, ('Broken text encoding', rel, ascii(broken))
        for pattern in patterns:assert not re.search(pattern,value),('Sensitive data pattern',rel)
        if rel.parts[0] in {'macros','slicer','config','recipes','examples','firmware'}:
            assert not re.search(r'(?m)^\s*(?:G31\b|M556\b|M307\b|M593\b)',value),('Local calibration',rel)
    for folder in ['slicer/materials','slicer/processes','slicer/toolheads']:
        for path in (ROOT/folder).glob('*.json'):
            obj=json.loads(path.read_text())
            assert not {'bed_shape','max_print_height','axis_max','screw_x','screw_y'} & set(obj.get('settings',{})),path

def independence():
    import build as builder
    original=builder.read
    def without_machine(path):
        assert not str(path).startswith(('config/models/','config/hardware/','config/motion/','recipes/'))
        return original(path)
    selections=read('slicer/profiles.json')
    builder.read=without_machine
    try:
        macros=macro_files()
        assert macros['stop.g']==(ROOT/'macros/stop.g').read_bytes()
        assert macros['adaptive_mesh.g']==(ROOT/'macros/adaptive_mesh.g').read_bytes()
        for selection in selections.values():
            files=profile_files(selection)
            assert not any(k.startswith(('sys/','reference/')) for k in files)
            bundle=configparser.ConfigParser(interpolation=None)
            bundle.read_string(files['PrusaSlicer-process-material.ini'].decode())
            assert {s.split(':')[0] for s in bundle.sections()}=={'print','filament'}
            assert not any(key in files['PrusaSlicer-process-material.ini'].decode()
                           for key in ['bed_shape','max_print_height','BIG-Meter','BIG-120Z'])
            assert not re.search(r'^M203\b',files['gcode/start.gcode'].decode(),re.M)
    finally:
        builder.read=original
    return len(selections)

def starter_checks():
    groups=starter_groups()
    bundle=configparser.ConfigParser(interpolation=None)
    bundle.read_string(starter_bundle().decode('utf-8'))
    assert {name:dict(bundle[name]) for name in bundle.sections()}==groups
    printers={name:value for name,value in groups.items() if name.startswith('printer:')}
    filaments={name:value for name,value in groups.items() if name.startswith('filament:')}
    processes=[value for name,value in groups.items() if name.startswith('print:')]
    assert len(processes)==1 and len(filaments)==3
    enabled=[m for m in read('slicer/machines.json')['models'].values() if m.get('starter_enabled',True)]
    assert len(printers)==len(enabled)*3
    process=processes[0]
    assert process['automatic_extrusion_widths']=='1'
    assert all(v=='0' for k,v in process.items() if k.endswith(('_extrusion_width','_acceleration')))
    assert process['max_volumetric_speed']=='0'
    assert sorted(float(v['filament_max_volumetric_speed']) for v in filaments.values())==[30,40,80]
    for value in filaments.values():
        assert value['slowdown_below_layer_time']=='45' and value['min_print_speed']=='5'
        assert value['bed_temperature']==value['first_layer_bed_temperature']=='0'
        assert 'M572 S' in value['start_filament_gcode']
        assert 'HC_TOOLHEAD=' in value['compatible_printers_condition']
    for name,value in printers.items():
        assert value['default_filament_profile'].strip('"') in [n.split(':',1)[1] for n in filaments]
        assert not re.search(r'\bM(?:203|572)\b',value['start_gcode'])
        assert value['use_relative_e_distances']=='1' and value['machine_limits_usage']=='time_estimate_only'
        assert float(value['min_layer_height']) <= float(process['layer_height']) <= float(value['max_layer_height'])
        assert 'M204 P250 T800' in value['start_gcode']
        assert value['end_gcode']==text('slicer/gcode/end.gcode').rstrip().replace('\n',r'\n')
        assert value['print_host']==value['printhost_apikey']==''
    return len(printers)

if __name__=='__main__':
    privacy()
    print(f'PASS: {starter_checks()} starter printer presets; {independence()} machine-independent profiles; {composition()} example recipes; {geometry()} actual U/mesh geometry cases; {stop_checks()} bounded Z cases; shared macro identity, warm retract, cache and privacy')
