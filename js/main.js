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

  // contact form → Supabase (storage) + FormSubmit (email notification)
  const cform = document.getElementById('contactForm');
  if (cform) {
    const SB_URL = 'https://otcokfqvyburuqcndcne.supabase.co';
    const SB_KEY = 'sb_publishable_8Tx63dr_5YEjRcBdu21HXA_5EaGTItM'; // public key; RLS = insert-only
    const status = document.getElementById('formStatus');
    const btn = cform.querySelector('button[type=submit]');
    cform.addEventListener('submit', async e => {
      e.preventDefault();
      const f = Object.fromEntries(new FormData(cform));
      if (f._honey) { cform.reset(); return; } // bot trap
      btn.disabled = true; btn.textContent = 'Sending…';
      status.textContent = ''; status.className = 'form-status';
      const save = fetch(SB_URL + '/rest/v1/contact_submissions', {
        method: 'POST',
        headers: { apikey: SB_KEY, Authorization: 'Bearer ' + SB_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: f.name, email: f.email, project: f.project, message: f.message, page: location.href })
      }).then(r => r.ok, () => false);
      const mail = fetch('https://formsubmit.co/ajax/jchappellmedia@gmail.com', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ name: f.name, email: f.email, project: f.project, message: f.message, _subject: f._subject })
      }).then(r => r.ok, () => false);
      const [saved, mailed] = await Promise.all([save, mail]);
      btn.disabled = false; btn.textContent = 'Send';
      if (saved || mailed) {
        cform.reset();
        status.textContent = "Sent — we'll get back to you within a business day.";
        status.classList.add('ok');
      } else {
        status.textContent = 'Something glitched. Email us directly: josh.lightbox@gmail.com';
        status.classList.add('err');
      }
    });
  }

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
