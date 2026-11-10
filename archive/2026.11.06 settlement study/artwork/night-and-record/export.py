"""Export the selected bowl, printed book and noninteractive ending masters.

Run from the repository root: uv run --with pillow python 'archive/2026.11.06 settlement study/artwork/night-and-record/export.py'
The ending deliberately has no cream veil; playable backgrounds use their own export.
"""
from pathlib import Path
from PIL import Image

masters = Path(__file__).resolve().parent
assets = masters.parents[3] / 'stories/settlement/assets'
for name, size in [('pond-water-v3', (288, 224)), ('encyclopedia-v3', (640, 426))]:
    Image.open(masters / f'{name}.master.png').convert('RGBA').resize(size, Image.Resampling.LANCZOS).save(assets / 'icons' / f'{name}.png')
Image.open(masters / 'settlement-record-v4.master.png').convert('RGB').resize((780, 1688), Image.Resampling.LANCZOS).save(assets / 'backgrounds/settlement-record-v4.webp', quality=95)
