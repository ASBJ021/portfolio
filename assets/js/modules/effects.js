export function initEffects() {
  const toTop = document.getElementById('to-top');
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  window.addEventListener('scroll', () => {
    if (!toTop) return;
    const show = window.scrollY > 600;
    toTop.classList.toggle('show', show);
  });
  if (toTop) toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

