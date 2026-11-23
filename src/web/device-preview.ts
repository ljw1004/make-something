import {browserDebugAvailable} from './debug-control.ts';
import {standaloneDisplay} from './home-screen.ts';

export const previewDevices = [
  {id:'auto', label:'Auto', width:0, height:0},
  {id:'iphone', label:'iPhone', width:390, height:844},
  {id:'ipad-portrait', label:'iPad portrait', width:1024, height:1366},
  {id:'ipad-landscape', label:'iPad landscape', width:1366, height:1024},
] as const;
const key = 'make-something-device-preview-v1';
const root = document.documentElement;
const deviceFor = (id: string | null) => previewDevices.find(device => device.id === id) ?? previewDevices[0];
export let selectedDevice = deviceFor(null);

function apply() {
  const device = selectedDevice;
  if (!device.width || !browserDebugAvailable()) {
    delete root.dataset.devicePreview;
    for (const name of ['--device-width','--device-height','--device-fit','--device-split-fit']) root.style.removeProperty(name);
    return;
  }
  root.dataset.devicePreview = device.id;
  const heightFit = Math.min(1, root.clientHeight / device.height);
  root.style.setProperty('--device-width', device.width + 'px');
  root.style.setProperty('--device-height', device.height + 'px');
  root.style.setProperty('--device-fit', String(Math.min(heightFit, root.clientWidth / device.width)));
  root.style.setProperty('--device-split-fit', String(Math.min(heightFit, root.clientWidth / 2 / device.width)));
}
export function selectDevice(id: string) {
  selectedDevice = deviceFor(id);
  try { localStorage.setItem(key, selectedDevice.id); } catch { /* Keep the selection for this visit. */ }
  apply();
}
export function initializeDevicePreview() {
  try { selectedDevice = deviceFor(localStorage.getItem(key)); } catch { /* Auto is the default. */ }
  apply();
  window.addEventListener('resize', apply);
  standaloneDisplay.addEventListener('change', apply);
}

/** Client rectangles and pointer events are in displayed pixels. The board lays out in device CSS pixels. */
export function previewScale(element: Element) {
  return root.dataset.devicePreview ? Number(getComputedStyle(element).getPropertyValue('--device-scale')) || 1 : 1;
}
export function layoutRect(element: Element, scale: number) {
  const rect = element.getBoundingClientRect();
  return scale === 1 ? rect : new DOMRect(rect.x / scale, rect.y / scale, rect.width / scale, rect.height / scale);
}
