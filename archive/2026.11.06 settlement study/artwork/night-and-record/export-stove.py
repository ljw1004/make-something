"""Register the complete pot above the unchanged stove; run with uv --with pillow."""
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[4]
art = Path(__file__).resolve().parent
icons = root / 'stories/settlement/assets/icons'
base = Image.open(icons / 'stove-base-v2.png').convert('RGBA')
canvas_size = (224, 320)
base_y = 96
padded = Image.new('RGBA', canvas_size)
padded.alpha_composite(base, (0, base_y))

pot = Image.open(art / 'stove-pot-v3.master.png').convert('RGBA')
pot = pot.crop(pot.getchannel('A').point(lambda value: 255 if value > 8 else 0).getbbox())
pot.thumbnail((134, 124), Image.Resampling.LANCZOS)
overlay = Image.new('RGBA', canvas_size)
overlay.alpha_composite(pot, (114 - pot.width // 2, base_y + 65 - pot.height))
complete = padded.copy()
complete.alpha_composite(overlay)
complete.save(icons / 'cooking-stove.png')
assert padded.crop((0, base_y, 224, 320)).tobytes() == base.tobytes()
print(f'Stove base unchanged: 224x224, padded to {canvas_size}; pot {pot.size}, base shift {base_y}px.')
