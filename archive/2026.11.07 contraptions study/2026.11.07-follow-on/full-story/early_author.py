"""Regenerate the retained early-family chapter fragments from their route data."""
import importlib
from early_common import write_fragment

if __name__ == '__main__':
    for name in ('pinball','dragon','drum'):
        family=importlib.import_module(name)
        if hasattr(family,'write'):family.write()
        else:write_fragment(family)
        print(name, sum(len(chapter['steps']) for chapter in family.CHAPTERS), 'operations')
