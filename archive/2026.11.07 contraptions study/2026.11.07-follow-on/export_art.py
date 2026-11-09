"""Tight current-stage exports at a shared physical pixel scale.

A family's union determines only pixels per projected model unit. Each current
stage has its own actual alpha bounds; future fittings never reserve blank canvas.
"""
from PIL import Image

DENSITY = 4
MARGIN = 3 * DENSITY


def bounds(image):
    box = image.getchannel('A').point(lambda a: 255 if a >= 24 else 0).getbbox()
    if not box:
        raise ValueError('Empty artwork')
    return box


def union(boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def export(image, ratio, path):
    crop = bounds(image)
    part = image.crop(crop)
    size = (max(1, round(part.width * ratio)), max(1, round(part.height * ratio)))
    if size != part.size:
        part = part.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (part.width + 2*MARGIN, part.height + 2*MARGIN))
    canvas.alpha_composite(part, (MARGIN, MARGIN))
    canvas.save(path, quality=94, method=6)
    return dict(crop=list(crop), size=list(canvas.size), pixelsPerSourcePixel=ratio,
                marginCss=MARGIN/DENSITY)
