const normalTextContrast = 4.5;
const linear = Float64Array.from({length: 256}, (_, byte) => {
  const value = byte / 255;
  return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
});

interface Box { left: number; top: number; right: number; bottom: number }
interface TextBox extends Box { node: Text; lineBottom: number; wraps: boolean }

function visibleText(element: HTMLElement, clip: DOMRect, image: DOMRect): TextBox[] {
  const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
  const range = document.createRange();
  const boxes: TextBox[] = [];
  for (let node = walker.nextNode() as Text | null; node; node = walker.nextNode() as Text | null) {
    if (!node.data.trim()) continue;
    range.selectNodeContents(node);
    const rects = range.getClientRects();
    for (const rect of rects) {
      const left = Math.max(rect.left, clip.left, image.left) - image.left;
      const top = Math.max(rect.top, clip.top, image.top) - image.top;
      const right = Math.min(rect.right, clip.right, image.right) - image.left;
      const bottom = Math.min(rect.bottom, clip.bottom, image.bottom) - image.top;
      if (right > left && bottom > top) boxes.push({left, top, right, bottom, node, lineBottom: rect.bottom, wraps: rects.length > 1});
    }
  }
  return boxes;
}

function lineText({node, lineBottom, wraps}: TextBox): string {
  if (!wraps) return node.data;
  const range = document.createRange();
  // Find the text offsets at either edge of this wrapped line.
  const startOfLine = (bottom: number) => {
    let first = 0, end = node.data.trimEnd().length;
    while (first < end) {
      const offset = Math.floor((first + end) / 2);
      range.setStart(node, offset);
      range.setEnd(node, offset + 1);
      if (range.getBoundingClientRect().bottom < bottom) first = offset + 1;
      else end = offset;
    }
    return first;
  };
  return node.data.slice(startOfLine(lineBottom - 0.5), startOfLine(lineBottom + 0.5));
}

function trimBlur(context: CanvasRenderingContext2D, backdrop: HTMLElement, text: TextBox[], clipBottom: number) {
  if (!text.length) {
    backdrop.style.setProperty('--carousel-blur-bottom', '100%');
    return;
  }
  const lastLine = Math.max(...text.map(box => box.bottom));
  let edge = lastLine;
  if (lastLine < clipBottom) {
    edge = Math.max(...text.filter(box => box.bottom === lastLine).map(box => {
      const style = getComputedStyle(box.node.parentElement!);
      context.font = `${style.fontStyle} ${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
      const metrics = context.measureText(lineText(box));
      const margin = 0.2 * context.measureText('x').actualBoundingBoxAscent;
      return lastLine - metrics.fontBoundingBoxDescent + metrics.actualBoundingBoxDescent + margin;
    }));
  }
  backdrop.style.setProperty('--carousel-blur-bottom', `${Math.max(0, clipBottom - edge)}px`);
}

// A summed-area table lets every background pixel contribute to the blur
// estimate while keeping the cost per text pixel independent of blur radius.
function colorSums(pixels: ImageData): Uint32Array {
  const {data, width, height} = pixels;
  const stride = (width + 1) * 3;
  const sums = new Uint32Array(stride * (height + 1));
  for (let y = 0; y < height; y++) {
    let red = 0, green = 0, blue = 0;
    for (let x = 0; x < width; x++) {
      const source = (y * width + x) * 4;
      const target = (y + 1) * stride + (x + 1) * 3;
      red += data[source]; green += data[source + 1]; blue += data[source + 2];
      sums[target] = red + sums[target - stride];
      sums[target + 1] = green + sums[target + 1 - stride];
      sums[target + 2] = blue + sums[target + 2 - stride];
    }
  }
  return sums;
}

function chooseInk(pixels: ImageData, lines: Box[], radius: number): 'dark' | 'light' {
  const {width, height} = pixels;
  const sums = colorSums(pixels);
  const stride = (width + 1) * 3;
  let dark = 0, light = 0, luminance = 0, count = 0;
  for (const line of lines) {
    for (let y = line.top; y < line.bottom; y++) {
      const top = Math.max(0, y - radius), bottom = Math.min(height, y + radius + 1);
      for (let x = line.left; x < line.right; x++) {
        const left = Math.max(0, x - radius), right = Math.min(width, x + radius + 1);
        const area = (bottom - top) * (right - left);
        const start = top * stride + left * 3, end = bottom * stride + right * 3;
        const upperRight = top * stride + right * 3, lowerLeft = bottom * stride + left * 3;
        const channel = (offset: number) => linear[Math.round((sums[end + offset] + sums[start + offset] -
          sums[upperRight + offset] - sums[lowerLeft + offset]) / area)];
        const value = 0.2126 * channel(0) + 0.7152 * channel(1) + 0.0722 * channel(2);
        if ((value + 0.05) / 0.05 >= normalTextContrast) dark++;
        if (1.05 / (value + 0.05) >= normalTextContrast) light++;
        luminance += value;
        count++;
      }
    }
  }
  // Prefer the color that reaches the target across more of the lettering.
  // If the counts tie, use the color with greater contrast at mean luminance.
  const equalContrast = Math.sqrt(1.05 * 0.05) - 0.05;
  return dark > light || dark === light && luminance > equalContrast * count ? 'dark' : 'light';
}

function sample(context: CanvasRenderingContext2D, art: HTMLImageElement, image: DOMRect, backdrop: HTMLElement, text: Box[]) {
  const scale = Math.max(image.width / art.naturalWidth, image.height / art.naturalHeight);
  const cropX = (art.naturalWidth - image.width / scale) / 2;
  // Read every pixel in the occupied region at CSS resolution. Cap the
  // resolution of unusually wide layouts while keeping the full footprint.
  const resolution = Math.min(1, 800 / image.width);
  const layer = getComputedStyle(backdrop, '::before');
  const blur = (layer.backdropFilter || layer.getPropertyValue('-webkit-backdrop-filter')).match(/blur\(([\d.]+)px\)/);
  // Estimate the rendered Gaussian blur with a box of comparable variance.
  const radius = blur ? Math.round(Number(blur[1]) * Math.sqrt(3) * resolution) : 0;
  const lines = text.map(({left, top, right, bottom}) => ({
    left: Math.floor(left * resolution), top: Math.floor(top * resolution),
    right: Math.ceil(right * resolution), bottom: Math.ceil(bottom * resolution),
  }));
  const left = Math.max(0, Math.min(...lines.map(rect => rect.left)) - radius);
  const top = Math.max(0, Math.min(...lines.map(rect => rect.top)) - radius);
  const right = Math.min(Math.ceil(image.width * resolution), Math.max(...lines.map(rect => rect.right)) + radius);
  const bottom = Math.min(Math.ceil(image.height * resolution), Math.max(...lines.map(rect => rect.bottom)) + radius);
  const width = right - left, height = bottom - top;
  context.canvas.width = width;
  context.canvas.height = height;
  // Match the cover's center/top object positioning and include enough
  // surrounding art to estimate the blur at every line edge.
  const factor = resolution * scale;
  context.drawImage(art, cropX + left / factor, top / factor, width / factor, height / factor, 0, 0, width, height);
  const pixels = context.getImageData(0, 0, width, height);
  return chooseInk(pixels, lines.map(box => ({
    left: box.left - left, top: box.top - top, right: box.right - left, bottom: box.bottom - top,
  })), radius);
}

export function watchCarouselContrast(frame: HTMLElement) {
  const context = document.createElement('canvas').getContext('2d', {willReadFrequently: true, alpha: false});
  if (!context) return {refresh() {}, schedule() {}};

  const blocked = new WeakMap<HTMLImageElement, string>();
  const refresh = () => {
    // Rectangles during a story's 3D turn are projected out of scene space.
    if (frame.dataset.storyFlip && frame.dataset.storyFlip !== 'waiting') return;
    for (const slide of frame.querySelectorAll<HTMLElement>('.carousel-slide:not([hidden])')) {
      const art = slide.querySelector<HTMLImageElement>('.carousel-art');
      const description = slide.querySelector<HTMLElement>('.carousel-description');
      if (!description) continue;
      const backdrop = description.parentElement!;
      const clip = description.getBoundingClientRect();
      const image = art?.getBoundingClientRect() ?? clip;
      const text = visibleText(description, clip, image);
      trimBlur(context, backdrop, text, clip.bottom - image.top);
      if (!text.length || !art?.complete || !art.naturalWidth || blocked.get(art) === art.currentSrc) {
        delete slide.dataset.ink;
        continue;
      }
      try {
        slide.dataset.ink = sample(context, art, image, backdrop, text);
      } catch (error) {
        // A remote cover without pixel-read permission still displays normally.
        if (!(error instanceof DOMException) || error.name !== 'SecurityError') throw error;
        blocked.set(art, art.currentSrc);
        delete slide.dataset.ink;
      }
    }
  };

  let pending = 0;
  function schedule() {
    if (pending) return;
    pending = requestAnimationFrame(() => { pending = 0; refresh(); });
  }
  const resize = new ResizeObserver(schedule);
  resize.observe(frame);
  frame.querySelectorAll('.carousel-description').forEach(label => resize.observe(label));
  frame.addEventListener('load', schedule, true);
  frame.addEventListener('scroll', schedule, true);
  return {refresh, schedule};
}
