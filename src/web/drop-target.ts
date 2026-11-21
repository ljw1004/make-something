import type {Story} from '../story/types.ts';
import type {State, Action} from '../engine/types.ts';
import {legalActions} from '../engine/game.ts';
import {placementHints} from '../engine/placement-hints.ts';
import {hotspotDrop} from '../engine/hotspot-drop.ts';
import {containsPoint, type Rect, type HotspotRegion} from './hotspot-view.ts';

export interface DropTarget<T> {
  value: T;
  item?: string;
  hotspot?: string;
  chapter: number;
  region: HotspotRegion;
  zIndex: number;
}
export interface DropResolution<T> {
  target?: T;
  action?: Extract<Action, {type: 'combine'}>;
  usefulPlacement?: boolean;
  ambiguous: string[];
}

function intersectsTarget(rectangle: Rect, target: HotspotRegion): boolean {
  // The nearest point to the target's centre works for circles and rectangles,
  // including boundary contact and a drag region collapsed to a line or point.
  return containsPoint(target, {
    x: Math.max(rectangle.x, Math.min(rectangle.x + rectangle.width, target.x + target.width / 2)),
    y: Math.max(rectangle.y, Math.min(rectangle.y + rectangle.height, target.y + target.height / 2)),
  });
}

/** Snapshot legal choices once per gesture; geometry remains live during scrolling. */
export function createDropResolver(story: Story, state: State, item: string) {
  const actions = legalActions(story, state).filter(action => action.a === item);
  const placements = new Set(placementHints(story, state).filter(hint => hint.item === item).map(hint => hint.hotspot));
  return <T>(point: {x: number; y: number}, rectangle: Rect, targets: DropTarget<T>[], clip?: Rect): DropResolution<T> => {
    const centre = {x: rectangle.x + rectangle.width / 2, y: rectangle.y + rectangle.height / 2};
    const x = Math.max(Math.min(point.x, centre.x), clip?.x ?? -Infinity);
    const y = Math.max(Math.min(point.y, centre.y), clip?.y ?? -Infinity);
    const right = Math.min(Math.max(point.x, centre.x), clip ? clip.x + clip.width : Infinity);
    const bottom = Math.min(Math.max(point.y, centre.y), clip ? clip.y + clip.height : Infinity);
    if (right < x || bottom < y || (clip && (!clip.width || !clip.height))) return {ambiguous:[]};
    const intent = {x, y, width:right - x, height:bottom - y};
    const pointerVisible = !clip || containsPoint(clip, point);
    const ranked = targets.filter(target => target.item !== item).map((target, order) => ({
      ...target, order, underPointer: pointerVisible && containsPoint(target.region, point),
    })).filter(target => intersectsTarget(intent, target.region))
      .sort((a,b) => Number(b.underPointer) - Number(a.underPointer) || b.zIndex - a.zIndex || b.order - a.order);
    const resolved = ranked.map<DropResolution<T>>(target => {
      if (target.item) return {target: target.value, action: actions.find(action => action.b === target.item), ambiguous: []};
      const result = hotspotDrop(story, state, item, target.hotspot!, target.chapter, actions);
      return {target: target.value, ...result, usefulPlacement: placements.has(target.hotspot!)};
    });
    // Incompatible objects and unresolved stations cannot mask an unambiguous useful drop.
    return resolved.find(result => result.action || (result.usefulPlacement && !result.ambiguous.length))
      ?? resolved.find(result => result.ambiguous.length)
      ?? resolved.find((_, index) => ranked[index].hotspot)
      ?? {ambiguous: []};
  };
}
