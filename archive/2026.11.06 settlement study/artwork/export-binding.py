"""Export selected binding illustrations and pad existing record art for fitting.
Run from repository root: uv run --with pillow python 'archive/2026.11.06 settlement study/artwork/export-binding.py'
No drawing/content changes: scale and transparent registration only.
The current printed encyclopedia-v3 is exported separately by night-and-record/export.py.
The v2 encyclopedia below is retained only as that edit's reference.
"""
from PIL import Image
from pathlib import Path
root=Path('stories/settlement/assets/icons')
masters=Path('archive/2026.11.06 settlement study/artwork/binding')
for name in ['binding-boards','encyclopedia']:
 Image.open(masters/(name+'-master.png')).convert('RGBA').resize((640,426),Image.Resampling.LANCZOS).save(root/(name+'-v2.png'))
entries=[('art','printed-pages-v3.png',60,68),('specimen','pressed-plant-specimen.png',70,105),('plants','botanical-drawing.png',80,142),('pond','pond-life-study.png',90,179),('rain','rain-record.png',345,68),('wind','wind-record.png',355,125),('stars','star-chart.png',365,182)]
for name,source,x,y in entries:
 image=Image.open(root/source).convert('RGBA');image.thumbnail((190,180),Image.Resampling.LANCZOS)
 canvas=Image.new('RGBA',(640,426));canvas.alpha_composite(image,(x,y));canvas.save(root/('binding-'+name+'.png'))
Image.new('RGBA',(400,180)).save('stories/settlement/assets/hotspots/binding-table.png')
