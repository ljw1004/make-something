"""Regenerate only the five early-family chapter fragments from their route data."""
import importlib
from early_common import write_fragment

if __name__ == '__main__':
    for name in ('pinball','dragon','periscope','kaleidoscope','drum'):
        family=importlib.import_module(name)
        write_fragment(family)
        print(name, sum(len(chapter['steps']) for chapter in family.CHAPTERS), 'operations')
