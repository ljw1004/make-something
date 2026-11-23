import type {ImageSize, Point} from '../story/coordinates.ts';

export interface BoardRect {x:number;y:number;width:number;height:number}
export const referenceBoard: BoardRect = {x: 0, y: 0, width: 390, height: 844};
export interface SceneSize extends ImageSize {image?: ImageSize}

/** Convert source-image pixels to the internal scene units used by saved moves. */
export function scenePoint(point: Point, scene: SceneSize): Point {
  return {x: point.x * (scene.width / (scene.image?.width ?? scene.width)), y: point.y * (scene.height / (scene.image?.height ?? scene.height))};
}

/** Internal display geometry; authors use the background's actual pixel dimensions. */
export function sceneSize(image?: ImageSize): SceneSize {
  const usable = image && image.width > 0 && image.height > 0 ? image : undefined;
  return {width: 390, height: usable ? 390 * usable.height / usable.width : 844, ...(usable ? {image: usable} : {})};
}

/** Tall artwork fills portrait panes, with a fit for more nearly square panes. */
export function viewportBoard(width: number, height: number, image?: {width:number;height:number}) {
  const scene = sceneSize(image);
  const cover = scene.height / scene.width >= 16 / 9 && height / width >= 5 / 4;
  const scale = (cover ? Math.max : Math.min)(width / scene.width, height / scene.height);
  const visibleWidth = cover ? width : scene.width * scale;
  const visibleHeight = cover ? height : scene.height * scale;
  const bounds = {x: cover ? (scene.width - visibleWidth / scale) / 2 : 0, y: 0, width: cover ? visibleWidth / scale : scene.width, height: cover ? visibleHeight / scale : scene.height};
  // Movable objects grow with the scene up to twice their reference size.
  // Fixed artwork always keeps the scene scale so painted features stay registered.
  const itemScale = Math.min(1, 2 / scale);
  return {scale, itemScale, scene, cover, width: visibleWidth, height: visibleHeight, left: (width-visibleWidth)/2, top: (height-visibleHeight)/2, bounds,
    labelScale: cover ? 1 / scale : 1, cardScale: Math.min(itemScale, cover ? width / referenceBoard.width / scale : 1)};
}

/** Coordinates remain in the reference scene; only the visible drop bounds change. */
export function fitOnBoard(x: number, y: number, width: number, height: number, bounds = referenceBoard) {
  return {
    x: Math.max(bounds.x, Math.min(bounds.x + Math.max(0, bounds.width - width), x)),
    y: Math.max(bounds.y, Math.min(bounds.y + Math.max(0, bounds.height - height), y)),
  };
}

/** An authored centre is exact: an occupied or out-of-board rectangle falls back. */
export function placeAtCentre(centre: {x:number;y:number}, size: {width:number;height:number}, occupied: BoardRect[], bounds = referenceBoard) {
  const x = centre.x - size.width / 2, y = centre.y - size.height / 2;
  if (![x,y,size.width,size.height].every(Number.isFinite) || x < bounds.x || y < bounds.y || x + size.width > bounds.x + bounds.width || y + size.height > bounds.y + bounds.height) return;
  if (occupied.some(r => x < r.x+r.width && x+size.width > r.x && y < r.y+r.height && y+size.height > r.y)) return;
  return {x,y};
}

function creationCandidates(receiver: BoardRect, result: ImageSize) {
  const x = receiver.x + (receiver.width - result.width) / 2;
  const y = receiver.y + (receiver.height - result.height) / 2;
  const overlapX = .1 * Math.min(receiver.width, result.width);
  const overlapY = .1 * Math.min(receiver.height, result.height);
  const left = receiver.x - result.width + overlapX;
  const right = receiver.x + receiver.width - overlapX;
  const top = receiver.y - result.height + overlapY;
  const bottom = receiver.y + receiver.height - overlapY;
  return {
    centre: {x, y},
    corners: [{x:left,y:top}, {x:right,y:top}, {x:left,y:bottom}, {x:right,y:bottom}],
    sides: [{x:left,y}, {x:right,y}, {x,y:top}, {x,y:bottom}],
  };
}

function overlapArea(position: Point, size: ImageSize, obstacle: BoardRect) {
  const width = Math.max(0, Math.min(position.x + size.width, obstacle.x + obstacle.width) - Math.max(position.x, obstacle.x));
  const height = Math.max(0, Math.min(position.y + size.height, obstacle.y + obstacle.height) - Math.max(position.y, obstacle.y));
  return width * height;
}

/** Fill a retired receiver's space, or overlap a surviving receiver's corner.
 * Occupied rectangles exclude the receiver, whose small overlap is deliberate. */
export function placeCreation(receiver:BoardRect,result:{width:number;height:number},replace:boolean,bounds=referenceBoard,occupied:BoardRect[]=[]){
  const {centre,corners,sides}=creationCandidates(receiver,result);
  const fit=(position:{x:number;y:number})=>fitOnBoard(position.x,position.y,result.width,result.height,bounds);
  if(replace)return fit(centre);
  const centrality=(p:{x:number;y:number})=>(p.x+result.width/2-bounds.x-bounds.width/2)**2+(p.y+result.height/2-bounds.y-bounds.height/2)**2;
  const inward=(a:{x:number;y:number},b:{x:number;y:number})=>centrality(a)-centrality(b);
  corners.sort(inward); sides.sort(inward);
  const overlap=(p:Point,r:BoardRect)=>overlapArea(p,result,r);
  const clear=(p:{x:number;y:number})=>p.x>=bounds.x&&p.y>=bounds.y&&p.x+result.width<=bounds.x+bounds.width&&p.y+result.height<=bounds.y+bounds.height&&occupied.every(r=>overlap(p,r)<=1e-6);
  const neighbour=corners.find(clear)??sides.find(clear);
  if(neighbour)return neighbour;
  // In a crowded scene, compare all eight positions by total intersected area,
  // including the parent. Fit only here: clamping can enlarge its 10% overlap.
  const crowded=[...corners,...sides].map(fit).map(position=>({position,area:[receiver,...occupied].reduce((sum,r)=>sum+overlap(position,r),0)}));
  crowded.sort((a,b)=>a.area-b.area||inward(a.position,b.position));
  return crowded[0].position;
}

interface HotspotCreationSpace {
  board: BoardRect;
  bounds: BoardRect;
  items: readonly BoardRect[];
  otherHotspots: readonly BoardRect[];
}

/** At a hotspot, a little overlap can keep a result away from the outer bands. */
export function placeHotspotCreation(receiver: BoardRect, result: ImageSize, {board, bounds, items, otherHotspots}: HotspotCreationSpace): Point {
  const epsilon = 1e-6;
  const {corners, sides} = creationCandidates(receiver, result);
  const area = Math.max(1, result.width * result.height);
  const margin = Math.max(epsilon, board.height / 10);
  const badge = bounds.y - board.y;
  const compare = (a: number, b: number) => Math.abs(a - b) > epsilon ? a - b : 0;

  const candidates = [...corners, ...sides].map((raw, index) => {
    const position = fitOnBoard(raw.x, raw.y, result.width, result.height, bounds);
    const fits = compare(raw.x, position.x) === 0 && compare(raw.y, position.y) === 0;
    const edge = Math.max(0, board.y + margin - (position.y - badge), position.y + result.height - (board.y + board.height - margin)) / margin;
    let itemOverlap = 0, mostCoveredItem = 0;
    for (const item of items) {
      const overlap = overlapArea(position, result, item);
      if (overlap <= epsilon) continue;
      itemOverlap += overlap / area;
      mostCoveredItem = Math.max(mostCoveredItem, overlap / (item.width * item.height));
    }
    const hotspotOverlap = otherHotspots.reduce((sum, hotspot) => {
      const overlap = overlapArea(position, result, hotspot);
      return sum + (overlap > epsilon ? overlap : 0);
    }, 0);
    const cornerPreference = index < corners.length ? 0 : .07;
    const receiverOverlap = overlapArea(position, result, receiver) / area;
    const score = .60 * edge + itemOverlap + .40 * mostCoveredItem + cornerPreference + hotspotOverlap / area + .5 * receiverOverlap;
    const horizontal = Math.abs(position.x + result.width / 2 - (board.x + board.width / 2)) / Math.max(epsilon, board.width / 2);
    const vertical = Math.abs(position.y + result.height / 2 - (board.y + board.height / 2)) / Math.max(epsilon, board.height / 2);
    return {position, fits, itemOverlap, mostCoveredItem, hotspotOverlap, score, horizontal, vertical};
  });

  const fitting = candidates.filter(candidate => candidate.fits);
  const local = fitting.length ? fitting : candidates;
  const clearOfHotspots = local.filter(candidate => candidate.hotspotOverlap === 0);
  const available = clearOfHotspots.length ? clearOfHotspots : local;
  // Cap the total cover and the share of any one item when a lower-cover option exists.
  const modest = available.filter(candidate => candidate.itemOverlap <= .20 && candidate.mostCoveredItem <= .30);
  const shortlist = modest.length ? modest : available;
  shortlist.sort((a, b) => compare(a.score, b.score) || compare(a.horizontal, b.horizontal) || compare(a.vertical, b.vertical));
  return shortlist[0].position;
}
