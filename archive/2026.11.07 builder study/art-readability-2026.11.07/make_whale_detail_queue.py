"""Generate the selected c20/c21 production requests from the retained config.

Main cameras render at 960 px; close cameras render at 640 px. Both use the
approved +Y studio orientation. Only c21 close views add the configured
exterior inspection lamp. The output is disposable input for Blender.
"""
import argparse
import json
from pathlib import Path


def production_requests(config):
    requests = []
    for chapter, settings in config['chapters'].items():
        for identity in settings['ids']:
            for mode, resolution in [('main', 960), ('detail', 640)]:
                request = {
                    'name': f'{chapter}--{identity}--{mode}',
                    'id': identity,
                    'chapter': chapter,
                    'view': config['main']['view'] if mode == 'main' else settings['detail_view'],
                    'resolution': resolution,
                    'light_side': '+Y',
                    'hatch_degrees': settings['hatch_degrees'][identity],
                }
                if mode == 'detail' and 'detail_inspection_light' in settings:
                    request['inspection_light'] = settings['detail_inspection_light']
                requests.append(request)
    if len({request['name'] for request in requests}) != len(requests):
        raise ValueError('Production render names must be unique')
    return requests


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default=str(Path(__file__).with_name('fitted-chapter-views.json')))
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text())
    queue = {'requests': production_requests(config), 'finish': True}
    Path(args.output).write_text(json.dumps(queue, indent=2)+'\n')
