"""Combine frozen still-render passes without inventing common source provenance.

The supplied view record comes from a current Blender build/stage pass. Reused
images must have the same camera and visible part membership as that record.
The caller must also identify geometry/material changes that require patches;
camera equality does not establish those. The combined manifest remains
compatible with full-story/export.py. An export-only regrouping or magnification
change can use a baseline without a patch pass.
"""
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import shutil
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path / 'src/story/parser.ts').is_file())
sys.path.insert(0, str(HERE / 'full-story'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return str(path.resolve().relative_to(ROOT))


p = argparse.ArgumentParser()
p.add_argument('--family', required=True)
p.add_argument('--baseline', required=True)
p.add_argument('--patch', action='append', default=[])
p.add_argument('--views', required=True)
p.add_argument('--output', required=True)
args = p.parse_args()
module = importlib.import_module(args.family)
view_path = Path(args.views)
current = json.loads(view_path.read_text())[args.family]
if sha(Path(module.__file__)) != current['sha256']:
    raise ValueError('Current PLAN changed after the Blender camera check')
if set(module.PLAN) != set(current['rows']):
    raise ValueError('Camera check does not cover the current PLAN')

passes = []
for index, directory in enumerate([args.baseline] + args.patch):
    folder = Path(directory)
    path = folder / (args.family + '-manifest.json')
    record = json.loads(path.read_text())
    if record.get('changedSources') or not record.get('sources'):
        raise ValueError('Expected an original frozen render pass: ' + str(path))
    passes.append(dict(name='baseline' if index == 0 else 'patch-' + str(index),
                       folder=folder, manifest=path, record=record,
                       by_image={row['image']: row for row in record['images']}, used=[]))

selected = []
seen = set()
group_views = {}
for identity, info in module.PLAN.items():
    filename = info.get('image', identity)
    if filename in seen:
        continue
    seen.add(filename)
    source = next((entry for entry in reversed(passes) if filename in entry['by_image']), None)
    if source is None:
        raise ValueError('Missing current image: ' + filename)
    previous = source['by_image'][filename]
    view = current['rows'][identity]['view']
    if previous['view'] != view:
        raise ValueError('Rerender changed camera: ' + identity)
    if set(previous['parts']) != set(info['parts']):
        raise ValueError('Rerender changed part membership: ' + identity)
    signature = json.dumps(view, sort_keys=True)
    if info['group'] in group_views and group_views[info['group']] != signature:
        raise ValueError('Shared crop group changes camera: ' + info['group'])
    group_views[info['group']] = signature
    png = source['folder'] / (filename + '.png')
    if sha(png) != previous['sha256']:
        raise ValueError('Rendered PNG differs from source manifest: ' + str(png))
    row = dict(previous, id=identity, image=filename, group=info['group'],
               css=info['css'], parts=info['parts'], view=view,
               sourcePass=source['name'], sourceId=previous['id'])
    selected.append((png, row))
    source['used'].append(identity)

out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
for png, row in selected:
    shutil.copy2(png, out / png.name)
record = dict(family=args.family, composite=True, changedSources=[],
              mergeSource=dict(path=relative(Path(__file__)), sha256=sha(Path(__file__))),
              currentPlanSource=dict(path=relative(Path(module.__file__)), sha256=current['sha256']),
              cameraVerification=dict(path=relative(view_path), sha256=sha(view_path),
                                      exactMatches=len(selected)),
              sourcePasses=[dict(id=entry['name'], manifest=relative(entry['manifest']),
                                 manifestSha256=sha(entry['manifest']),
                                 sources=entry['record']['sources'], usedIds=entry['used'])
                            for entry in passes if entry['used']],
              images=[row for _, row in selected])
(out / (args.family + '-manifest.json')).write_text(json.dumps(record, indent=2) + '\n')
print(args.family, len(selected), 'images; source passes:',
      {entry['name']: len(entry['used']) for entry in passes})
