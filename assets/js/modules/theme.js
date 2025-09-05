export function initTheme() {
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');
  const stored = localStorage.getItem('theme');
  const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
  const initial = stored || (prefersLight ? 'light' : 'dark');
  if (initial === 'light') root.setAttribute('data-theme', 'light');

  function setTheme(next) {
    if (next === 'light') root.setAttribute('data-theme', 'light');
    else root.removeAttribute('data-theme');
    localStorage.setItem('theme', next);
    if (toggle) toggle.textContent = root.getAttribute('data-theme') === 'light' ? '🌞' : '🌙';
  }

  if (toggle) {
    toggle.addEventListener('click', () => {
      const now = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      setTheme(now);
    });
    toggle.textContent = root.getAttribute('data-theme') === 'light' ? '🌞' : '🌙';
  }
}

