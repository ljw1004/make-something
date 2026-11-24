import {previewScale} from './device-preview.ts';

const normalTextContrast = 4.5;
const linear = Float64Array.from({length: 256}, (_, byte) => {
  const value = byte / 255;
  return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
});

interface Box { left: number; top: number; right: number; bottom: number }
type Ink = 'dark' | 'light';

function visibleText(element: HTMLElement, clip: DOMRect, image: DOMRect): Box[] {
  const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
  const range = document.createRange();
  const boxes: Box[] = [];
  for (let node = walker.nextNode() as Text | null; node; node = walker.nextNode() as Text | null) {
    if (!node.data.trim()) continue;
    range.selectNodeContents(node);
    const rects = range.getClientRects();
    for (const rect of rects) {
      const left = Math.max(rect.left, clip.left, image.left) - image.left;
      const top = Math.max(rect.top, clip.top, image.top) - image.top;
      const right = Math.min(rect.right, clip.right, image.right) - image.left;
      const bottom = Math.min(rect.bottom, clip.bottom, image.bottom) - image.top;
      if (right > left && bottom > top) boxes.push({left, top, right, bottom});
    }
  }
  return boxes;
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

// Paint and measure the same softened cover pixels so the contrast decision
// also holds at boundaries between bright and dark artwork.
function blurCover(pixels: ImageData, radius: number) {
  const {width, height, data} = pixels;
  const sums = colorSums(pixels);
  const stride = (width + 1) * 3;
  for (let y = 0; y < height; y++) {
    const top = Math.max(0, y - radius), bottom = Math.min(height, y + radius + 1);
    for (let x = 0; x < width; x++) {
      const left = Math.max(0, x - radius), right = Math.min(width, x + radius + 1);
      const area = (bottom - top) * (right - left);
      const offset = (y * width + x) * 4;
      for (let i = 0; i < 3; i++) {
        data[offset + i] = (sums[bottom * stride + right * 3 + i] - sums[top * stride + right * 3 + i]
          - sums[bottom * stride + left * 3 + i] + sums[top * stride + left * 3 + i]) / area;
      }
    }
  }
}

function luminance(data: Uint8ClampedArray, i: number) {
  return 0.2126 * linear[data[i]] + 0.7152 * linear[data[i + 1]] + 0.0722 * linear[data[i + 2]];
}

const floorForBlack = normalTextContrast * 0.05 - 0.05;
const ceilingForWhite = 1.05 / normalTextContrast - 0.05;

function chooseInk({width, data}: ImageData, lines: Box[]): Ink {
  let dark = 0, light = 0, total = 0, count = 0;
  for (const line of lines) {
    for (let y = line.top; y < line.bottom; y++) {
      for (let x = line.left; x < line.right; x++) {
        const value = luminance(data, (y * width + x) * 4);
        if (value >= floorForBlack) dark++;
        if (value <= ceilingForWhite) light++;
        total += value;
        count++;
      }
    }
  }
  const equalContrast = Math.sqrt(1.05 * 0.05) - 0.05;
  return dark > light || dark === light && total > equalContrast * count ? 'dark' : 'light';
}

function correctContrast({data}: ImageData, ink: Ink) {
  for (let i = 0; i < data.length; i += 4) {
    data[i + 3] = 0; // The line footprints below supply the opacity.
    const value = luminance(data, i);
    const lift = ink === 'dark';
    if (lift ? value >= floorForBlack : value <= ceilingForWhite) continue;
    // Mix toward white or black in linear light. Round toward the safe side
    // of the threshold when encoding the corrected colour back into sRGB.
    const keep = lift ? (1 - floorForBlack) / (1 - value) : ceilingForWhite / value;
    for (let channel = i; channel < i + 3; channel++) {
      const adjusted = linear[data[channel]] * keep + (lift ? 1 - keep : 0);
      const srgb = adjusted <= 0.0031308 ? 12.92 * adjusted : 1.055 * adjusted ** (1 / 2.4) - 0.055;
      data[channel] = lift ? Math.ceil(srgb * 255) : Math.floor(srgb * 255);
    }
  }
}

function featherLines({width, height, data}: ImageData, lines: Box[], feather: number) {
  for (const line of lines) {
    const left = Math.max(0, line.left - feather), right = Math.min(width, line.right + feather);
    const top = Math.max(0, line.top - feather), bottom = Math.min(height, line.bottom + feather);
    for (let y = top; y < bottom; y++) {
      const dy = Math.max(0, line.top - y, y + 1 - line.bottom);
      for (let x = left; x < right; x++) {
        const dx = Math.max(0, line.left - x, x + 1 - line.right);
        const opacity = 1 - Math.hypot(dx, dy) / feather;
        const alpha = (y * width + x) * 4 + 3;
        data[alpha] = Math.max(data[alpha], opacity * 255);
      }
    }
  }
}

function paintBackdrop(context: CanvasRenderingContext2D, art: HTMLImageElement, image: DOMRect,
  clip: DOMRect, canvas: HTMLCanvasElement, text: Box[]): Ink {
  const scale = Math.max(image.width / art.naturalWidth, image.height / art.naturalHeight);
  const cropX = (art.naturalWidth - image.width / scale) / 2;
  const resolution = Math.min(1, 800 / image.width);
  const cssScale = previewScale(canvas) * resolution;
  const feather = Math.max(1, Math.round(8 * cssScale));
  // A box with this radius approximates the previous 3 CSS pixel blur.
  const radius = Math.round(3 * Math.sqrt(3) * cssScale);
  const margin = radius + feather;
  const lines = text.map(({left, top, right, bottom}) => ({
    left: Math.floor(left * resolution), top: Math.floor(top * resolution),
    right: Math.ceil(right * resolution), bottom: Math.ceil(bottom * resolution),
  }));
  const left = Math.max(0, Math.min(...lines.map(rect => rect.left)) - margin);
  const top = Math.max(0, Math.min(...lines.map(rect => rect.top)) - margin);
  const right = Math.min(Math.ceil(image.width * resolution), Math.max(...lines.map(rect => rect.right)) + margin);
  const bottom = Math.min(Math.ceil(image.height * resolution), Math.max(...lines.map(rect => rect.bottom)) + margin);
  const width = right - left, height = bottom - top;
  canvas.width = width;
  canvas.height = height;
  // Match the cover's center/top object positioning and include enough
  // surrounding art to estimate the blur at every line edge.
  const factor = resolution * scale;
  context.drawImage(art, cropX + left / factor, top / factor, width / factor, height / factor, 0, 0, width, height);
  const pixels = context.getImageData(0, 0, width, height);
  const localLines = lines.map(box => ({
    left: box.left - left, top: box.top - top, right: box.right - left, bottom: box.bottom - top,
  }));
  blurCover(pixels, radius);
  const ink = chooseInk(pixels, localLines);
  correctContrast(pixels, ink);
  featherLines(pixels, localLines, feather);
  context.putImageData(pixels, 0, 0);
  canvas.style.left = `${(left - (clip.left - image.left) * resolution) / cssScale}px`;
  canvas.style.top = `${(top - (clip.top - image.top) * resolution) / cssScale}px`;
  canvas.style.width = `${width / cssScale}px`;
  canvas.style.height = `${height / cssScale}px`;
  return ink;
}

export function watchCarouselContrast(frame: HTMLElement) {
  const blocked = new WeakMap<HTMLImageElement, string>();
  const refresh = () => {
    // Rectangles during a story's 3D turn are projected out of scene space.
    if (frame.dataset.storyFlip && frame.dataset.storyFlip !== 'waiting') return;
    for (const slide of frame.querySelectorAll<HTMLElement>('.carousel-slide:not([hidden])')) {
      const art = slide.querySelector<HTMLImageElement>('.carousel-art');
      const description = slide.querySelector<HTMLElement>('.carousel-description');
      const canvas = slide.querySelector<HTMLCanvasElement>('.carousel-description-backdrop');
      if (!description || !canvas) continue;
      const clip = description.getBoundingClientRect();
      const image = art?.getBoundingClientRect() ?? clip;
      const text = visibleText(description, clip, image);
      const context = canvas.getContext('2d', {willReadFrequently: true});
      if (!context || !text.length || !art?.complete || !art.naturalWidth || blocked.get(art) === art.currentSrc) {
        canvas.hidden = true;
        delete slide.dataset.ink;
        continue;
      }
      try {
        slide.dataset.ink = paintBackdrop(context, art, image, clip, canvas, text);
        canvas.hidden = false;
      } catch (error) {
        // A remote cover without pixel-read permission still displays normally.
        if (!(error instanceof DOMException) || error.name !== 'SecurityError') throw error;
        blocked.set(art, art.currentSrc);
        canvas.hidden = true;
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
