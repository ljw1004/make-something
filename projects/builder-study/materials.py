"""Flat linear-RGB materials for the vintage school-workshop direction.

No image textures, procedural grain or external material dependencies.
"""
PALETTE = {
    'paper_reverse': (.64,.23,.15,1),
    'birch': (.58, .34, .14, 1),
    'card': (.62, .43, .22, 1),
    'teal': (.085, .24, .13, 1),
    'orange': (.52, .13, .08, 1),
    'ink': (.035, .035, .030, 1),
    'paper': (.78, .73, .60, 1),
    'battery': (.12, .34, .58, 1),
    'future': (.74, .22, .43, 1),
}


def apply(scene_parts):
    scene_parts.PALETTE.update(PALETTE)
