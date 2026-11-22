import {mountCatalogue} from './catalogue.ts';

const cover = document.querySelector<HTMLDivElement>('#catalogue-app');
if (cover) {
  mountCatalogue(cover);
} else {
  void import('./main.ts').then(({mountPlayer}) => mountPlayer(document.querySelector<HTMLElement>('#workspace')!));
}
