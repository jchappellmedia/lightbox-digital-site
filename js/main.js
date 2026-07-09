// Lightbox Digital — interactions
(function () {
  const burger = document.getElementById('burger');
  const links = document.getElementById('navLinks');
  burger?.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    burger.classList.toggle('x', open);
    burger.setAttribute('aria-expanded', open);
    document.body.classList.toggle('navlock', open);
  });
  links?.addEventListener('click', e => {
    if (e.target.tagName === 'A') {
      links.classList.remove('open'); burger.classList.remove('x');
      document.body.classList.remove('navlock');
    }
  });

  // hero film: honor reduced motion
  const hv = document.querySelector('.hero-video');
  if (hv && matchMedia('(prefers-reduced-motion: reduce)').matches) {
    hv.removeAttribute('autoplay'); hv.pause();
  }

  // reveal on scroll
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  // lightbox: vimeo, local video, or image
  const lb = document.getElementById('lightbox');
  const frame = document.getElementById('lbFrame');
  const close = () => { lb.hidden = true; frame.innerHTML = ''; document.body.style.overflow = ''; };
  document.getElementById('lbClose')?.addEventListener('click', close);
  lb?.addEventListener('click', e => { if (e.target === lb) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && !lb.hidden) close(); });
  const openLb = html => { frame.innerHTML = html; lb.hidden = false; document.body.style.overflow = 'hidden'; };

  document.querySelectorAll('[data-vimeo]').forEach(btn => btn.addEventListener('click', () => {
    const v = btn.dataset.vimeo;
    openLb(`<iframe src="https://player.vimeo.com/video/${v}${v.includes('?') ? '&' : '?'}autoplay=1&title=0&byline=0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Video player"></iframe>`);
  }));
  document.querySelectorAll('[data-video]').forEach(btn => btn.addEventListener('click', () => {
    openLb(`<video src="${btn.dataset.video}" controls autoplay playsinline></video>`);
  }));
  document.querySelectorAll('[data-img]').forEach(btn => btn.addEventListener('click', () => {
    openLb(`<img src="${btn.dataset.img}" alt="">`);
  }));

  // work filters
  const fbtns = document.querySelectorAll('.fbtn');
  fbtns.forEach(b => b.addEventListener('click', () => {
    fbtns.forEach(x => x.classList.remove('active')); b.classList.add('active');
    const f = b.dataset.f;
    document.querySelectorAll('#workgrid .piece').forEach(c => {
      c.style.display = (f === 'all' || c.dataset.cat === f || c.dataset.cat === 'reel') ? '' : 'none';
    });
  }));
})();
