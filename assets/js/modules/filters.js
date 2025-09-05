export function initProjectFilters() {
  const section = document.getElementById('projects');
  if (!section) return;
  const btns = section.querySelectorAll('.filter-btn');
  const cards = Array.from(section.querySelectorAll('.grid.three.cards .card'));
  const catHeadings = Array.from(section.querySelectorAll('h3')).filter(h => !h.closest('.card'));
  const grids = section.querySelectorAll('.grid.three.cards');
  const status = section.querySelector('.filters-status');

  // Precompute counts per category
  const counts = cards.length ? cards.reduce((acc, card) => {
    const cat = card.getAttribute('data-category') || 'other';
    acc[cat] = (acc[cat] || 0) + 1;
    acc.all = (acc.all || 0) + 1;
    return acc;
  }, {}) : { all: 0 };

  // Paint counts into buttons
  btns.forEach(btn => {
    const key = btn.getAttribute('data-filter');
    const countEl = btn.querySelector('.filter-count');
    if (countEl) countEl.textContent = counts[key] || 0;
  });

  function apply(filter, label = 'All') {
    cards.forEach(card => {
      const cat = card.getAttribute('data-category');
      const match = filter === 'all' || cat === filter;
      card.classList.toggle('is-hidden', !match);
    });

    const hideHeadings = filter !== 'all';
    catHeadings.forEach(h => h.classList.toggle('is-hidden', hideHeadings));

    grids.forEach(g => {
      if (filter === 'all') {
        g.classList.remove('is-hidden');
      } else {
        const visibleCount = g.querySelectorAll('.card:not(.is-hidden)').length;
        g.classList.toggle('is-hidden', visibleCount === 0);
      }
    });

    if (status) {
      const total = filter === 'all' ? (counts.all || 0) : (counts[filter] || 0);
      status.textContent = `Showing ${total} ${label} project${total === 1 ? '' : 's'}`;
    }
  }

  // Event delegation for robustness
  const filtersBar = section.querySelector('.filters');
  if (filtersBar) {
    filtersBar.addEventListener('click', (e) => {
      const btn = e.target.closest('.filter-btn');
      if (!btn) return;
      btns.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected', 'false'); b.setAttribute('aria-pressed', 'false'); });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      btn.setAttribute('aria-pressed', 'true');
      const filter = btn.getAttribute('data-filter');
      const label = (btn.querySelector('.label')?.textContent || btn.textContent || '').trim() || 'All';
      apply(filter, label);
    });
  }

  // Initial apply to normalize state
  apply('all', 'All');
}
