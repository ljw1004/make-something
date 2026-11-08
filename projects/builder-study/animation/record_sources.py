"""Consolidate completed frozen exports into the retained source record."""
from pathlib import Path
import argparse
import hashlib
import json

p = argparse.ArgumentParser()
p.add_argument('--input', required=True)
p.add_argument('--output', required=True)
args = p.parse_args()
directory = Path(args.input)
families = {}
for path in sorted(directory.glob('*-manifest.json')):
    record = json.loads(path.read_text())
    if record['probe'] or record['changedSources']:
        raise ValueError('A preview cannot enter the production source record: '+record['identity'])
    for filename, info in record['files'].items():
        if hashlib.sha256((directory/filename).read_bytes()).hexdigest() != info['sha256']:
            raise ValueError('Output changed after export: '+filename)
    families[record['identity']] = {key: record[key] for key in (
        'family', 'frames', 'fps', 'durationMs', 'resolution', 'posterResolution',
        'samples', 'engine', 'view', 'sources', 'crop', 'animationSize', 'posterSize',
        'cssMax', 'quality', 'files', 'cinematic')}
    if 'posterSamples' in record:
        families[record['identity']]['posterSamples'] = record['posterSamples']
output = dict(schemaVersion=1, scope='Completed Builder toy working loops',
              method='Canonical Blender assemblies; scripted physical pose controls; transparent WebP with registered static poster.',
              limits=[
                  'Prescribed kinematics; no force, friction, motor, fluid or contact dynamics simulation.',
                  'Projection uses the source ideal thin-lens chief rays, not measured optical brightness.',
                  'Finite sampling and source-informed visual inspection; this record does not establish human recognition or enjoyment.',
              ], families=families)
Path(args.output).write_text(json.dumps(output, indent=2)+'\n')
print('Recorded', len(families), 'frozen working-loop exports.')
