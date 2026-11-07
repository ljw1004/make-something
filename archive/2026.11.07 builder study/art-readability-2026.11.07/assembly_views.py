"""Visibility and supply ownership for Builder's connected-part recipe splits.

Canonical geometry, fitted transforms and motion functions remain unchanged.
Call stage AFTER canonical presentation.stage and BEFORE loose-icon selection.
A fixed render uses the canonical camera returned before this adapter. Groups
name real source components; they never manufacture joins or stretch a mesh.
"""


def geometry(model):
    return list(dict.fromkeys(o for group in model['parts'].values() for o in group
                             if o.type in {'MESH', 'CURVE', 'FONT'}))


def under(obj, parent):
    while obj:
        if obj == parent:
            return True
        obj = obj.parent
    return False


def prepare(model):
    """Assign existing stationary pen hardware to the prepared rover deck.

    Run once immediately after model construction, before canonical staging or
    owner/slot holdouts. This changes in-memory ownership only. The canonical
    state and overlay functions then expose/occlude this hardware with the deck
    automatically, including every partial slot configuration.
    """
    if 'carriage' not in model or 'rover-deck' not in model.get('parts', {}):
        return
    if model.get('_builder_pen_ownership_prepared'):
        return
    moving, stationary = [], []
    for obj in model['parts']['rover-pen-clip']:
        (moving if under(obj, model['carriage']) else stationary).append(obj)
    model['parts']['rover-pen-clip'] = moving
    model['parts']['rover-deck'].extend(stationary)
    for obj in stationary:
        obj['_builder_original_part_id'] = obj.get('part_id', '')
        obj['part_id'] = 'rover-deck'
    model['_builder_pen_ownership_prepared'] = True


def belongs(group, obj, model):
    name = obj.name
    part = obj.get('_builder_original_part_id', obj.get('part_id', ''))
    if group == 'pb.catch':
        return part == 'pb-rails' and name.startswith(('catch apron', 'marble storage cup', 'storage cup closed', 'apron push-fit'))
    if group == 'pb.rails':
        return part == 'pb-rails' and not belongs('pb.catch', obj, model)
    if group == 'pb.score':
        return part == 'pb-targets' and name.startswith(('score ', 'manual numbered score', 'actual score numeral'))
    if group == 'pb.arches':
        return part == 'pb-targets' and not belongs('pb.score', obj, model)
    if group == 'cd.wings':
        return part == 'cd-cutouts' and ('card wing' in name or 'graphic wing' in name)
    if group == 'cd.tail':
        return name.startswith(('fixed decorative card tail', 'tail attachment'))
    if group == 'cd.body':
        return part == 'cd-cutouts' and not belongs('cd.wings', obj, model) and not belongs('cd.tail', obj, model)
    if group == 'cd.wing-hinges':
        return part == 'cd-hinge-pins' and not name.startswith('tail attachment')
    if group == 'air.plunger-clip':
        return part == 'air-cradle' and name.startswith(('plunger end clip', 'plunger clip'))
    if group == 'air.cups':
        return part == 'air-cradle' and not belongs('air.plunger-clip', obj, model)
    if group == 'air.hand-holders':
        return part == 'air-tube-clips' and name.startswith(('hand holder', 'hand barrel holder'))
    if group == 'air.tube-clips':
        return part == 'air-tube-clips' and not belongs('air.hand-holders', obj, model)
    if group == 'whale.extensions':
        return part == 'whale-module-mount' and name.startswith(('supplied 366 mm extension strut', 'locked support extension sleeve', 'sleeve transverse retaining pin'))
    if group == 'whale.harness-extension':
        return part == 'whale-module-mount' and name.startswith(('supplied 366 mm harness extension', 'harness extension insulated'))
    if group == 'whale.forks':
        return part == 'whale-module-mount' and name.startswith(('cradle-to-spar compression fork', 'compression fork crosshead'))
    if group == 'whale.straps':
        return part == 'whale-module-mount' and name.startswith('upper module retaining strap')
    if group == 'whale.stop-guide':
        return part == 'whale-hatch' and name.startswith(('fixed button bezel', 'stop pushrod guide', 'fixed stop-button support flange'))
    if group == 'whale.stop-button':
        return part == 'whale-hatch' and name.startswith('exterior red stop button')
    if group == 'whale.hatch':
        return part == 'whale-hatch' and not belongs('whale.stop-guide', obj, model) and not belongs('whale.stop-button', obj, model)
    if group == 'whale.pushrod':
        return part == 'whale-stop-extension'
    if group == 'fair.switch-dock':
        return part == 'fair-power-divider' and name.startswith(('wired-switch storage dock', 'switch dock attached below deck'))
    if group == 'fair.power-system':
        return part == 'fair-power-divider' and not belongs('fair.switch-dock', obj, model)
    if group == 'lift.extended-module':
        return under(obj, model['lift']['module_root'])
    if group == 'lift.guide-posts':
        return part == 'lift-posts' and name.startswith('loose-clearance guide post')
    if group == 'lift.post-nuts':
        return part == 'lift-posts' and name.startswith('guide-post captive wingnut')
    if group == 'lift.guide-crossbars':
        return part == 'lift-posts' and name.startswith(('removable guide crossbar', 'guide crossbar removable frame clamp', 'loose sliding post guide'))
    if group == 'rover.moving-carriage':
        return part == 'rover-pen-clip' and under(obj, model['carriage'])
    if group == 'rover.prepared-pen-support':
        return part == 'rover-pen-clip' and not under(obj, model['carriage'])
    raise ValueError('Unknown connected-component group: '+group)


FIXED_REGENERATE = [
    'pb-rail-frame', 'pb-arched-table', 'air-clip-ready', 'air-held',
    'whale-mounted', 'whale-lift-resting', 'whale-hatched', 'whale-stop-guided',
    'rover-deck', 'guarded-rover', 'rover-tested', 'lift-guided-base', 'lift-seated', 'whale-switch-docked',
]


def stage(model, item, key, plan, canonical_item=None):
    """Apply explicit component subsets, retaining all prior fitted geometry.

    ``assembly_only_groups`` limits the visible canonical state to named real
    components. ``assembly_hide_groups`` removes not-yet-added components.
    ``assembly_show_groups`` exposes previously co-owned source components.
    None of these methods modifies canonical part tags or object transforms.
    """
    prepare(model)
    objects = geometry(model)
    before = {o for o in objects if not o.hide_render}
    shown = set(before)
    # The actual stationary cam, guide rods, return spring and stops are now
    # prepared deck hardware. The connected sliding carriage remains separate.
    # This affects every supplied/assembled deck state, including slot previews.
    deck_visible = key == 'rover' and any(o.get('part_id') == 'rover-deck' and o in before for o in objects)
    if deck_visible:
        shown.update(o for o in objects if belongs('rover.prepared-pen-support', o, model))
    for group in plan.get('assembly_show_groups', []):
        chosen = {o for o in objects if belongs(group, o, model)}
        if not chosen:
            raise ValueError(f'{item["id"]}: no source objects in show group {group}')
        shown.update(chosen)
    only = plan.get('assembly_only_groups')
    if only:
        selected = {o for o in objects if any(belongs(group, o, model) for group in only)}
        if not selected:
            raise ValueError(f'{item["id"]}: no source objects in only groups {only}')
        shown.intersection_update(selected)
    for group in plan.get('assembly_hide_groups', []):
        shown.difference_update(o for o in objects if belongs(group, o, model))
    hidden_parts = set(plan.get('assembly_hide_parts', []))
    shown.difference_update(o for o in objects if o.get('part_id') in hidden_parts)
    if not shown:
        raise ValueError(f'{item["id"]}: assembly selection removed all geometry')
    for obj in objects:
        obj.hide_render = obj not in shown
        obj.hide_set(obj not in shown)
    record = {'canonical_id': plan.get('canonical_id', item['id']),
              'beforeObjects': len(before), 'afterObjects': len(shown),
              'preparedDeckPenSupport': deck_visible,
              'onlyGroups': only or [], 'hideGroups': plan.get('assembly_hide_groups', []),
              'showGroups': plan.get('assembly_show_groups', [])}
    model['_builder_assembly_record'] = record
    return record
