"""Flat linear-RGB materials for the vintage school-workshop direction.

No image textures, procedural grain or external material dependencies.
"""
PALETTE = {
    'paper_reverse': (.55,.16,.10,1),
    'birch': (.58, .34, .14, 1),
    'card': (.62, .43, .22, 1),
    'teal': (.045, .15, .075, 1),
    'orange': (.38, .075, .04, 1),
    'ink': (.035, .035, .030, 1),
    'paper': (.78, .73, .60, 1),
}


def apply(scene_parts):
    scene_parts.PALETTE.update(PALETTE)
