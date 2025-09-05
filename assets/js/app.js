import { initTheme } from './modules/theme.js';
import { initNav } from './modules/nav.js';
import { initEffects } from './modules/effects.js';
import { initProjectFilters } from './modules/filters.js';

function init() {
  initTheme();
  initNav();
  initEffects();
  initProjectFilters();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
