import {mountCatalogue} from './catalogue.ts';
import {initializeDevicePreview} from './device-preview.ts';

initializeDevicePreview();
const cover = document.querySelector<HTMLDivElement>('#catalogue-app');
if (cover) {
  mountCatalogue(cover);
} else {
  void import('./main.ts').then(({mountPlayer}) => mountPlayer(document.querySelector<HTMLElement>('#workspace')!));
}
