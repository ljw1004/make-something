"""Export bounded inspection icons and registered workpieces from native artwork.

Pillow only: crop/resize existing model renders, never synthesize geometry.
Inputs come from a fixed Git revision plus explicitly supplied replacement
masters. This makes reruns independent of any previously promoted exports.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
from PIL import Image
from assembly_views import FIXED_REGENERATE


HERE = Path(__file__).resolve().parent


def repository_root():
    return next(p for p in HERE.parents if (p / 'src/story/parser.ts').exists())


def bbox(im):
    box = im.getchannel('A').point(lambda n: 255 if n > policy['alphaThreshold'] else 0).getbbox()
    if box is None:
        raise ValueError('Empty drawing')
    return box


def union(boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def padded(box, size, padding=6):
    return (max(0, box[0]-padding), max(0, box[1]-padding),
            min(size[0], box[2]+padding), min(size[1], box[3]+padding))


def dimensions(box):
    return box[2]-box[0], box[3]-box[1]


def image_from_bytes(data):
    return Image.open(io.BytesIO(data)).convert('RGBA')


def export(im, crop, factor, relative):
    result = im.crop(crop)
    result = result.resize(tuple(max(1, round(n*factor)) for n in result.size), Image.Resampling.LANCZOS)
    padding = [0, 0]
    if relative.startswith('assets/items/'):
        minimum = policy['minimumPortableCanvasCss']*4
        size = tuple(max(minimum, n) for n in result.size)
        if size != result.size:
            canvas = Image.new('RGBA', size)
            padding = [(size[i]-result.size[i])//2 for i in range(2)]
            canvas.alpha_composite(result, tuple(padding))
            result = canvas
    path = out / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    result.save(path, lossless=True, method=4)
    return {'path': relative, 'pixels': result.size, 'paddingPixels': padding,
            'visibleCss': [n/4 for n in dimensions(bbox(result))],
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--story', required=True)
parser.add_argument('--catalogue', required=True)
parser.add_argument('--presentations', default=str(HERE/'part-presentations.json'))
parser.add_argument('--masters', action='append', default=[], help='Standalone master directories, last wins')
parser.add_argument('--fixed-masters', action='append', default=[], help='Registered view directories, last wins; CHAPTER--ID overrides only that chapter')
parser.add_argument('--compound-masters', help='Owner and slot images using one fitted-assembly camera')
parser.add_argument('--paper-masters', help='Four paper-strip states on one shared inspection camera/canvas')
parser.add_argument('--flight-masters', help='Registered labeled flight detail/setup compositions')
parser.add_argument('--output', required=True, help='Candidate directory containing manuscript and assets')
parser.add_argument('--preview', action='store_true', help='Permit unfinished replacement masters; never promote this output')
args = parser.parse_args()
policy = json.loads((HERE/'scale-policy.json').read_text())
catalogue = json.loads(Path(args.catalogue).read_text())
plans = {i['id']: i for i in json.loads(Path(args.presentations).read_text())['items']}
story = Path(args.story).read_text()
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)
archive = subprocess.run(['git', 'archive', policy['baselineRevision'], 'stories/builder/assets', 'stories/builder/icon.png'],
                         cwd=repository_root(), check=True, capture_output=True).stdout
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
    original = {m.name.removeprefix('stories/builder/'): tf.extractfile(m).read() for m in tf.getmembers() if m.isfile()}

# Unchanged scenery/rewards retain their exact selected bytes.
for name, data in original.items():
    if name.startswith(('assets/items/', 'assets/hotspots/', 'assets/overlays/')):
        continue
    (out/name).parent.mkdir(parents=True, exist_ok=True)
    (out/name).write_bytes(data)

masters, metadata = {}, {}
for directory in args.masters:
    directory = Path(directory)
    masters.update({p.stem: p for p in directory.glob('*.png')})
    for manifest in sorted(directory.glob('manifest-*.json')):
        metadata.update({r['id']: r for r in json.loads(manifest.read_text())['images']})
fixed = {}
for directory in args.fixed_masters:
    fixed.update({p.stem: p for p in Path(directory).glob('*.png')})

images, source_records = {}, {}
for item in catalogue['items']:
    identity = item['id']
    plan = plans[identity]
    if plan['status'] == 'requires-author-resolution' and not args.preview:
        raise ValueError('Unresolved depiction: '+identity)
    source = masters.get(identity) or (fixed.get(identity) if plan['role'] == 'fixed-only' else None)
    if source:
        data = source.read_bytes()
        source_name = str(source)
    else:
        # All loose primitive pieces receive sharp new masters; selection/pose
        # changes may never silently fall back to the previous grouped picture.
        needs_master = item['primitive'] and plan['role'] != 'fixed-only'
        needs_master |= bool(plan.get('selection')) or bool(plan.get('pose')) or bool(plan.get('canonical_id')) or bool(plan.get('require_master'))
        if needs_master and not args.preview:
            raise FileNotFoundError('Missing required replacement master: '+identity)
        source_name = 'assets/items/'+identity+'.webp'
        data = original[source_name]
    images[identity] = image_from_bytes(data)
    source_records[identity] = {'source': source_name, 'sourceSha256': hashlib.sha256(data).hexdigest()}

records = []
handled = set()
compound_records = {}
for group in policy['sharedPaperGroups']:
    # Paper states share one physical pose, camera, crop and magnification.
    # New strip masters can use a developable loose coil for readable figures;
    # the banner pair retains its original common flat inspection view.
    use_paper = bool(args.paper_masters) and group[0] == 'film-blank-strip'
    ims = {identity: (Image.open(Path(args.paper_masters)/(identity+'.png')).convert('RGBA')
                      if use_paper else image_from_bytes(original['assets/items/'+identity+'.webp']))
           for identity in group}
    if len({im.size for im in ims.values()}) != 1:
        raise ValueError('Paper group canvas mismatch')
    bounds = union([bbox(im) for im in ims.values()])
    crop = padded(bounds, next(iter(ims.values())).size)
    factor = policy['sharedPaperCss']*4/max(dimensions(bounds))
    for identity, im in ims.items():
        records.append({'id': identity, 'family': 'shared-paper', 'crop': crop, 'factor': factor,
                        **export(im, crop, factor, 'assets/items/'+identity+'.webp')})
        handled.add(identity)

for item in catalogue['items']:
    identity = item['id']
    if identity in handled:
        continue
    im = images[identity]
    plan = plans[identity]
    family = plan['scale_family']
    bounds = bbox(im)
    crop = padded(bounds, im.size)
    if item['slots']:
        compound = Path(args.compound_masters) if args.compound_masters else None
        source_im = Image.open(compound/(identity+'.png')).convert('RGBA') if compound else image_from_bytes(original['assets/items/'+identity+'.webp'])
        overlays = {}
        for slot in item['slots']:
            name = identity+'--'+slot['accepts']
            overlays[name] = Image.open(compound/(name+'.png')).convert('RGBA') if compound else image_from_bytes(original['assets/overlays/'+name+'.webp'])
        if not compound and not args.preview:
            raise ValueError('Compound owner needs its updated registered view')
        if any(overlay.size != source_im.size for overlay in overlays.values()):
            raise ValueError('Compound overlays do not match owner canvas')
        bounds = union([bbox(source_im)]+[bbox(overlay) for overlay in overlays.values()])
        crop = padded(bounds, source_im.size)
        factor = policy['compoundCss']*4/max(dimensions(bounds))
        for name, overlay in overlays.items():
            export(overlay, crop, factor, 'assets/overlays/'+name+'.webp')
        im = source_im
        target = policy['compoundCss']
    else:
        limits = policy['families'][family]
        spans = metadata.get(identity, {}).get('view', {}).get('projectedSpans')
        if spans:
            physical = max(spans[:2])
            target = limits['referenceCss']*(physical/limits['referenceMetres'])**policy['compressionExponent']
        else:
            # Unchanged selected raster art has no new mesh measurement.
            # Compress its previous visible drawing size monotonically; do
            # not falsely label old pixel dimensions as physical metres.
            previous_css = max(dimensions(bounds))/4
            target = limits['referenceCss']*(previous_css/200)**.4
        target = max(limits['min'], min(limits['max'], target))
        if identity in policy['thinParts']:
            target = policy['thinPartCss']
        factor = target*4/max(dimensions(bounds))
    record = {'id': identity, 'family': family, 'crop': crop, 'factor': factor,
              'targetVisibleCss': target, **source_records[identity],
              **export(im, crop, factor, 'assets/items/'+identity+'.webp')}
    records.append(record)
    if item['slots']:
        compound_records[identity] = record

# Read authored fixed views (including garden variants), retaining their exact
# logical declarations while changing only art paths/registration metadata.
chapter_re = re.compile(r'(?m)^## `([^`]+)`[^\n]*\n')
chapters = list(chapter_re.finditer(story))
layout = {}
hotspot_re = re.compile(r'(?m)^- `([^`]+)` \(center ([\d.]+)px, ([\d.]+)px\)\n  - icon: !\[([^\]]*)\]\(([^)]+)\)(?:\n  - hitbox: \(center ([\d.]+)px, ([\d.]+)px\) \(size ([\d.]+)px, ([\d.]+)px\))?')
for number, chapter in enumerate(chapters):
    chapter_id = chapter.group(1)
    section = story[chapter.end():chapters[number+1].start() if number+1 < len(chapters) else len(story)]
    entries = list(hotspot_re.finditer(section))
    if not entries:
        continue
    source_images = {}
    for entry in entries:
        identity, path = entry.group(1), entry.group(5)
        if identity in compound_records:
            continue
        flight_source = Path(args.flight_masters)/(identity+'.png') if args.flight_masters and chapter_id in policy['contextChapters'] else None
        if flight_source is not None and not flight_source.is_file():
            raise FileNotFoundError('Missing flight composition: '+str(flight_source))
        if chapter_id in policy.get('inspectionChapters', []) and chapter_id+'--'+identity not in fixed and not args.preview:
            raise FileNotFoundError('Missing chapter inspection composition: '+chapter_id+'--'+identity)
        source = flight_source or fixed.get(chapter_id+'--'+identity) or fixed.get(identity)
        if identity in FIXED_REGENERATE and source is None and not args.preview:
            raise FileNotFoundError('Missing required fixed replacement master: '+identity)
        data = source.read_bytes() if source else original.get(path)
        if data is None:
            raise FileNotFoundError('Missing registered hotspot master: '+identity)
        source_images[identity] = image_from_bytes(data)
    sizes = {im.size for im in source_images.values()}
    if len(sizes) != 1:
        raise ValueError('Registered hotspot canvas mismatch in '+chapter_id+': '+str(sizes))
    size = next(iter(sizes))
    context = chapter_id in policy['contextChapters']
    if chapter_id in policy.get('inspectionChapters', []):
        crop = (0, 0, *size)
        factor = policy['fixedStageCss']*4/size[0]
    elif context:
        crop = (0, 0, *size)
        factor = policy['flightCanvasCss']*4/size[0] if args.flight_masters else 1.
    else:
        bounds = union([bbox(im) for im in source_images.values()])
        crop = padded(bounds, size)
        factor = policy['fixedStageCss']*4/max(dimensions(bounds))
    layout[chapter_id] = {}
    for entry in entries:
        identity = entry.group(1)
        if identity in compound_records:
            # A fixed compound uses the hotspot image as its owner beneath
            # the same slot overlays. It must use the identical export. The
            # rover's later upright view is an explicitly authored turn-over.
            record = compound_records[identity]
            path = 'assets/hotspots/'+chapter_id+'--'+identity+'.webp'
            (out/path).parent.mkdir(parents=True, exist_ok=True)
            (out/path).write_bytes((out/record['path']).read_bytes())
            layout[chapter_id][identity] = {**record, 'path': path,
                'center': policy['fixedCenterBackgroundPixels'], 'registeredCompound': True}
            continue
        center = (policy['flightCenterBackgroundPixels'] if args.flight_masters else [float(entry.group(2)), float(entry.group(3))]) if context else policy['fixedCenterBackgroundPixels']
        path = 'assets/hotspots/'+chapter_id+'--'+identity+'.webp'
        spec = {'center': center, 'crop': crop, 'factor': factor,
                **export(source_images[identity], crop, factor, path)}
        # The new flight compositions reserve their complete labeled canvas,
        # including setup and service panels, against arriving loose pieces.
        # A newly framed chapter-specific view has no valid correspondence
        # with the old camera's authored receiving box. Reserve its full image.
        if entry.group(6) and not (context and args.flight_masters) and chapter_id+'--'+identity not in fixed:
            old_center = [float(entry.group(2)), float(entry.group(3))]
            old_hit = [float(entry.group(6)), float(entry.group(7))]
            crop_center = [(crop[0]+crop[2])/2, (crop[1]+crop[3])/2]
            # Background coordinates are twice CSS; source pixels are four
            # times CSS. Apply the identical image crop/scale to the hitbox.
            spec['hitbox'] = {'center': [center[i]+factor*(old_hit[i]-old_center[i])+
                                        .5*factor*(size[i]/2-crop_center[i]) for i in range(2)],
                              'size': [factor*float(entry.group(i)) for i in (8, 9)]}
        layout[chapter_id][identity] = spec

def rewrite_chapter(match, section):
    chapter_id = match.group(1)
    def replace(entry):
        spec = layout[chapter_id][entry.group(1)]
        center = spec['center']
        result = f'- `{entry.group(1)}` (center {center[0]:g}px, {center[1]:g}px)\n  - icon: ![{entry.group(4)}]({spec["path"]})'
        if 'hitbox' in spec:
            hc, hs = spec['hitbox']['center'], spec['hitbox']['size']
            result += f'\n  - hitbox: (center {hc[0]:.3f}px, {hc[1]:.3f}px) (size {hs[0]:.3f}px, {hs[1]:.3f}px)'
        return result
    return match.group(0)+hotspot_re.sub(replace, section)

parts = [story[:chapters[0].start()]]
for number, chapter in enumerate(chapters):
    section = story[chapter.end():chapters[number+1].start() if number+1 < len(chapters) else len(story)]
    parts.append(rewrite_chapter(chapter, section))
(out/'builder.md').write_text(''.join(parts))
(out/'export-manifest.json').write_text(json.dumps({'previewOnly': args.preview, 'policy': policy,
    'storySha256': hashlib.sha256(story.encode()).hexdigest(), 'items': records, 'hotspots': layout}, indent=2)+'\n')
print(f'Exported {len(records)} item icons and {sum(map(len, layout.values()))} registered chapter views; previewOnly={args.preview}')
