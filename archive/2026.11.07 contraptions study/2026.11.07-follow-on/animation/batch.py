"""Sequential two-thread Blender rendering and compact registered WebP export.

Run from the repository root with the Pillow environment. The script never
copies its output to the live story; review and promotion are separate steps.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(path for path in HERE.parents if (path/'src/story/parser.ts').is_file())
FAMILIES = {
    'pinwheel': ('pinwheel', 400), 'racer': ('wind-racer', 350),
    'pinball': ('pinball-table', 350), 'dragon': ('crank-dragon', 350),
    'gantry': ('gantry-hoist', 345), 'carousel': ('electric-carousel', 345),
    'claw': ('pneumatic-claw', 345), 'drum': ('animation-drum', 350),
    'rover': ('drawing-rover', 340), 'projector': ('star-projector', 340),
    'carrier': ('flying-whale', 350),
    'window': ('open-window', 350), 'spinner': ('ribbon-spinner', 350),
}
p = argparse.ArgumentParser()
p.add_argument('--families', default=','.join(FAMILIES))
p.add_argument('--output', required=True)
p.add_argument('--blender', default='/Applications/Blender.app/Contents/MacOS/Blender')
p.add_argument('--samples', type=int, default=8)
p.add_argument('--size', type=int, help='Animation maximum pixels; defaults to 560 for Spinner, 640 otherwise')
p.add_argument('--quality', type=int, help='WebP quality; defaults to 80 for Spinner, 82 otherwise')
p.add_argument('--resume', action='store_true')
args = p.parse_args()
out = Path(args.output).resolve()
out.mkdir(parents=True, exist_ok=True)
for family in args.families.split(','):
    identity, css = FAMILIES[family]
    raw = out/family
    manifest = raw/'render-manifest.json'
    reusable = False
    if args.resume and manifest.exists():
        record = json.loads(manifest.read_text())
        reusable = not record['probe'] and not record['changedSources']
        reusable = reusable and all((raw/f'{i:04d}.png').is_file() for i in range(record['frames']))
        reusable = reusable and all((ROOT/path).is_file() and hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest
                                     for path, digest in record['sources'].items())
    if not reusable:
        # A failed rerender must not inherit the previous run's success marker.
        manifest.unlink(missing_ok=True)
        glass = family in {'carousel', 'spinner', 'carrier'}
        with (out/(family+'.log')).open('w') as log:
            subprocess.run([args.blender, '--background', '--factory-startup', '--threads', '2',
                            '--python', str(HERE/'render.py'), '--', '--family', family,
                            '--output', str(raw), '--samples', str(max(args.samples, 24) if glass else args.samples),
                            '--poster-samples', '48' if glass else '24',
                            '--frames', '120' if family == 'projector' else '96'],
                           stdout=log, stderr=subprocess.STDOUT, check=True)
        # Blender can exit zero after a Python error. Require its completed
        # frozen manifest, then let export reject partial or stale sequences.
        if not manifest.exists():
            raise RuntimeError('Incomplete Blender render: '+family)
    export_size = args.size if args.size is not None else (560 if family == 'spinner' else 640)
    export_quality = args.quality if args.quality is not None else (80 if family == 'spinner' else 82)
    subprocess.run([sys.executable, str(HERE/'export.py'), '--input', str(raw),
                    '--output', str(out/'export'), '--size', str(export_size),
                    '--css', str(css), '--quality', str(export_quality)], check=True)
    print('COMPLETE', family, flush=True)
