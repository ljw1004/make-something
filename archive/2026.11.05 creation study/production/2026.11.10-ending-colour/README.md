# Richer colour for the final painting

Accepted 10 November 2026. The user requested a preview with a little more saturation, then approved that preview unchanged for the full-page Song of creation ending. The [live brief](../../../../stories/creation/design-brief.md#visual-intent) owns the adopted colour direction.

- [ending-song.png](ending-song.png): the selected 854 × 1842 master, copied byte for byte from the built-in image tool's preview.
- [request.json](request.json): exact image-tool request, original output location, preserved input, hashes and export geometry. The prompt asks for approximately 20 percent more saturation; that is a creative instruction, not a measured uniform numerical adjustment.
- [Runtime painting](../../../../stories/creation/assets/backgrounds/ending-song.webp): 780 × 1688 WebP, using the previous source crop, LANCZOS reduction, quality 92 and method 6. Preserving the framing avoids changing the page composition during this colour revision.
- [Previous master](../2026.11.05-revision/background-masters/ending-song.png) and [previous runtime](../../assets/backgrounds/ending-song.webp): unchanged. The archived runtime is byte-identical to the file replaced by this revision.

The richer blues, greens, ochres and muted reds retain the interwoven abstract forms and soft watercolour character. The separate circular item and simplified catalogue/home-screen icon keep their selected artwork. No new generation followed acceptance.

## Reproduce the runtime export

From the repository root:

```sh
uv run --quiet --with pillow python - <<'PY'
from pathlib import Path
from PIL import Image
import json

folder = Path('archive/2026.11.05 creation study/production/2026.11.10-ending-colour')
record = json.loads((folder / 'request.json').read_text())
settings = record['export']
with Image.open(folder / record['master']) as image:
    image.convert('RGB').resize(
        tuple(settings['size']), Image.Resampling.LANCZOS,
        box=tuple(settings['source_box']),
    ).save(folder / settings['runtime'], 'WEBP', **settings['webp'])
PY
```

## Verification outcome

The retained master matches the approved preview byte for byte. In Chromium at 390 × 844, jumped to The End, opened the chapter, decoded the new 780 × 1688 background and confirmed it displays at 390 × 844 with no page errors. Visually inspected the final full-page presentation. The previous runtime's archived hash matches the replaced file. This verifies the export and browser presentation, not native-device colour reproduction.

Creation lint passed with zero errors and the same eight reviewed warnings: seven mixed-fate cases and the 20,000-state fixed-analysis limit. Whitespace and archive-link checks passed.

No application build is needed for this artwork-only replacement at its existing URL. No hosted publication was performed. Temporary screenshots and logs are discarded after recording the final outcome.
