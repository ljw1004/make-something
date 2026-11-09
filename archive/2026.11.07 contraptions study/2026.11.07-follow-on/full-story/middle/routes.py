"""Small manuscript builder shared only by the three middle toy families."""
from pathlib import Path


class Route:
    def __init__(self):
        self.plan = {}
        self.items = {}
        self.pages = []

    def item(self, identity, name, parts, group=None, css=110, explanation=''):
        self.plan[identity] = dict(parts=list(parts), group=group or identity, css=css)
        self.items[identity] = (name, explanation)
        return identity

    def page(self, identity, name, reference, items, goals, recipes, processes=None):
        self.pages.append((identity, name, reference, items, goals, recipes, processes or {}))

    def markdown(self):
        declared=set(); pages=[]
        for identity,name,reference,items,goals,recipes,processes in self.pages:
            lines=[f'## `{identity}` {name}', 'background: ![White instruction page](assets/backgrounds/white.svg)',
                   f'reference: ![{self.items[reference][0]}](assets/items/{reference}.webp)', '', '**Goals**']
            for index,(instruction,conditions) in enumerate(goals):
                prefix='- '+('next: ' if index else '')+instruction
                if isinstance(conditions,str): lines.append(prefix+f' -- `{conditions}`')
                else:
                    lines.append(prefix)
                    lines += ['  - '+('either: ' if j==0 else 'or: ')+f'`{condition}`' for j,condition in enumerate(conditions)]
            if processes:
                lines += ['', '**Hotspots**']
                for index,(process,action) in enumerate(processes.items()):
                    x=390 if len(processes)==1 else 130+260*index
                    lines += [f'- `{process}` (center {x}px, 216px)',
                              f'  - icon: ![{action.title()}](assets/actions/{action}.svg)',
                              f'  - hitbox: (center {x}px, 216px) (size 236px, 248px)']
            lines += ['', '**Items**']
            for item in items:
                if item in declared:continue
                declared.add(item); label,explanation=self.items[item]
                lines += [f'- `{item}` {label}', f'  - icon: ![{label}](assets/items/{self.plan[item].get("image",item)}.webp)']
                if explanation:lines += ['', '  ---', '', '  '+explanation, '']
            for process,action in processes.items():
                if process not in declared:
                    declared.add(process);lines.append(f'- `{process}` {action.title()}')
            lines += ['', '**Combinations**']
            for a,b,result in recipes:
                lines.append(f'- `{a}` [transform] @ `{b}` -> `{result}`' if b in processes else f'- `{a}` [transform] + `{b}` [consume] -> `{result}`')
            pages.append('\n'.join(lines))
        unused=set(self.items)-declared
        if unused:raise ValueError(f'Undeclared items: {unused}')
        return '\n\n'.join(pages)+'\n'

    def write(self, source):
        Path(source).with_suffix('.md').write_text(self.markdown())
