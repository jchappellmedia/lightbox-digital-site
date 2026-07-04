// Lightbox Digital — interactions
(function () {
  const nav = document.getElementById('nav');
  const onScroll = () => nav.classList.toggle('scrolled', scrollY > 24);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

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

  // scroll reveal
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  // video + photo lightbox
  const lb = document.getElementById('lightbox');
  const frame = document.getElementById('lbFrame');
  const close = () => { lb.hidden = true; frame.innerHTML = ''; document.body.style.overflow = ''; };
  document.getElementById('lbClose')?.addEventListener('click', close);
  lb?.addEventListener('click', e => { if (e.target === lb) close(); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && !lb.hidden) close(); });

  document.querySelectorAll('.vthumb').forEach(btn => btn.addEventListener('click', () => {
    const v = btn.dataset.vimeo;
    frame.innerHTML = `<iframe src="https://player.vimeo.com/video/${v}${v.includes('?') ? '&' : '?'}autoplay=1&title=0&byline=0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen title="Video player"></iframe>`;
    lb.hidden = false; document.body.style.overflow = 'hidden';
  }));
  document.querySelectorAll('.pthumb').forEach(btn => btn.addEventListener('click', () => {
    frame.innerHTML = `<img src="${btn.dataset.img}" alt="">`;
    lb.hidden = false; document.body.style.overflow = 'hidden';
  }));

  // portfolio filters
  const fbtns = document.querySelectorAll('.fbtn');
  fbtns.forEach(b => b.addEventListener('click', () => {
    fbtns.forEach(x => x.classList.remove('active')); b.classList.add('active');
    const f = b.dataset.f;
    document.querySelectorAll('#vgrid .vcard').forEach(c => {
      c.style.display = (f === 'all' || c.dataset.ind === f) ? '' : 'none';
    });
  }));
})();
