"""Slice generated presets with an existing local PrusaSlicer; no printer access."""
import argparse
import configparser
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from build import ROOT, build, compose, read, profile_files

def box(path):
    vertices=[(x,y,z) for z in [0,10] for y in [0,100] for x in [0,250]]
    triangles=[(0,2,1),(1,2,3),(4,5,6),(5,7,6),(0,1,4),(1,5,4),
               (2,6,3),(3,6,7),(0,4,2),(2,4,6),(1,3,5),(3,7,5)]
    stl='solid slicer_validation\n'
    for tri in triangles:
        stl+='facet normal 0 0 0\nouter loop\n'
        stl+=''.join('vertex %g %g %g\n'%vertices[i] for i in tri)
        stl+='endloop\nendfacet\n'
    path.write_text(stl+'endsolid slicer_validation\n')

def commands(value):
    return [c for line in value.splitlines() if (c:=line.split(';',1)[0].strip())]

def flow(text, diameter):
    pos=dict(X=0.,Y=0.,Z=0.);feed=0.;qmax=0.;paths=0;e=0.;relative=False
    area=math.pi*(float(diameter)/2)**2
    for line in commands(text):
        if line=='M83':relative=True
        if line=='M82':relative=False
        if line.startswith('G92 E'):e=float(line.split('E',1)[1])
        if not re.match(r'G[0123]\b',line):continue
        words={k:float(v) for k,v in re.findall(r'([XYZEFIJ])(-?(?:\d+(?:\.\d*)?|\.\d+))',line)}
        de=words.get('E',0) if relative else words.get('E',e)-e
        if 'E' in words:e=e+words['E'] if relative else words['E']
        feed=words.get('F',feed*60)/60
        end={k:words.get(k,v) for k,v in pos.items()}
        distance=math.sqrt(sum((end[k]-pos[k])**2 for k in pos))
        if line.startswith(('G2 ','G3 ')):
            cx,cy=pos['X']+words.get('I',0),pos['Y']+words.get('J',0)
            radius=math.hypot(pos['X']-cx,pos['Y']-cy)
            t0,t1=math.atan2(pos['Y']-cy,pos['X']-cx),math.atan2(end['Y']-cy,end['X']-cx)
            angle=((t0-t1) if line.startswith('G2 ') else (t1-t0))%(2*math.pi)
            distance=math.hypot(radius*(angle or 2*math.pi),end['Z']-pos['Z'])
        if distance>.01 and de>0:
            qmax=max(qmax,de*area*feed/distance);paths+=1
        pos=end
    return paths,qmax

def validate(slicer, work):
    work.mkdir(parents=True,exist_ok=True)
    model=work/'validation-box.stl';box(model)
    results=[]
    for recipe in sorted((ROOT/'recipes').glob('*.json')):
        dest=work/recipe.stem;build(recipe,dest)
        _,groups=compose(read('recipes/'+recipe.name))
        cfg={k:v for g in groups.values() for k,v in g.items()}
        output=dest/'validation.gcode'
        subprocess.run([str(slicer),'--load',str(dest/'PrusaSlicer.ini'),'--save',str(dest/'normalized.ini'),
                        '--export-gcode','--center','300,300','--output',str(output),str(model)],check=True)
        generated=output.read_text(encoding='utf-8')
        actual=commands(generated)
        startup=commands(cfg['start_gcode'].replace(r'\n','\n'))
        for c in startup:
            if c.startswith('M98 P"adaptive_mesh.g"'):
                assert any(x.startswith('M98 P"adaptive_mesh.g"') for x in actual)
            elif c=='M104 S[first_layer_temperature]':
                assert 'M104 S'+cfg['first_layer_temperature'] in actual
            elif c=='M109 S[first_layer_temperature]':
                assert 'M109 S'+cfg['first_layer_temperature'] in actual
            elif c=='{"if !move.axes[2].homed"}':
                assert 'if !move.axes[2].homed' in actual
            else:assert c in actual,c
        assert actual[-3:]==['M400','M300 S222 P1111','M0']
        assert actual.count(next(c for c in startup if c.startswith('M204 ')))==1
        assert actual.count(next(c for c in startup if c.startswith('M572 ')))==1
        assert 'M104 S'+cfg['temperature'] in actual
        assert not any(re.match(r'M(?:140|190)\b',c) for c in actual)
        assert not any(re.search(r'[{}\[\]]',c) for c in actual if c!='if !move.axes[2].homed')
        paths,qmax=flow(generated,cfg['filament_diameter'])
        caps=[float(cfg[k]) for k in ['max_volumetric_speed','filament_max_volumetric_speed'] if float(cfg.get(k,0))>0]
        assert paths>100
        if caps:assert qmax<=min(caps)*1.01,(recipe.name,qmax,caps)
        # Use the independent print/material bundle with an existing printer preset.
        standalone=profile_files(read('recipes/'+recipe.name))
        bundle=configparser.ConfigParser(interpolation=None)
        bundle.read_string(standalone['PrusaSlicer-process-material.ini'].decode())
        selected=dict(groups['printer'])
        for name in bundle.sections():selected.update(dict(bundle[name]))
        for key,name in [('start_gcode','start'),('end_gcode','end'),('before_layer_gcode','before-layer')]:
            selected[key]=standalone['gcode/'+name+'.gcode'].decode().rstrip().replace('\n',r'\n')
        independent=dest/'independent-profile.ini'
        independent.write_text(''.join(f'{k} = {v}\n' for k,v in sorted(selected.items())))
        independent_output=dest/'independent-profile.gcode'
        subprocess.run([str(slicer),'--load',str(independent),'--export-gcode','--center','300,300',
                        '--output',str(independent_output),str(model)],check=True)
        independent_commands=commands(independent_output.read_text())
        assert not any(c.startswith('M203 ') for c in independent_commands)
        assert next(c for c in startup if c.startswith('M204 ')) in independent_commands
        assert next(c for c in startup if c.startswith('M572 ')) in independent_commands
        assert independent_commands[-3:]==['M400','M300 S222 P1111','M0']
        mesh=next(c for c in independent_commands if c.startswith('M98 P"adaptive_mesh.g"'))
        assert re.search(r' L\d+ F\d+ R\d+ E\d+$',mesh)
        independent_paths,independent_flow=flow(independent_output.read_text(),cfg['filament_diameter'])
        assert independent_paths>100
        if caps:assert independent_flow<=min(caps)*1.01
        results.append({'recipe':recipe.stem,'extruding_paths_checked':paths,'maximum_nominal_flow_mm3_s':qmax,
                        'independent_profile_sliced_with_existing_printer':True,
                        'independent_profile_retains_machine_speed_limits':True,
                        'configured_volumetric_caps':caps,'gcode_sha256':hashlib.sha256(output.read_bytes()).hexdigest()})
    report={'slicer':str(slicer),'status':'Offline generated G-code checks passed',
            'recipes':results,'physical_test':False,'printer_files_written':False,'GUI_bundle_import_verified':False}
    (work/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--slicer',type=Path,required=True)
    p.add_argument('--workdir',type=Path,required=True)
    args=p.parse_args()
    validate(args.slicer.resolve(),args.workdir.resolve())
