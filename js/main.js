/* ============================================================
   임종권 — Operations × Technology
   Subtle interactions only. First screen renders without JS.
   ============================================================ */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Mobile nav toggle ---------- */
  var toggle = document.getElementById('nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- IntersectionObserver reveal (opacity/translate only) ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Lightbox (award photos) ---------- */
  var lightbox = document.getElementById('lightbox');
  var lbClose = document.getElementById('lightbox-close');
  var lbTrigger = document.querySelector('[data-lightbox]');
  var lastFocus = null;

  function openLightbox() {
    if (!lightbox) return;
    lastFocus = document.activeElement;
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
    if (lbClose) lbClose.focus();
  }
  function closeLightbox() {
    if (!lightbox) return;
    lightbox.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  if (lbTrigger) lbTrigger.addEventListener('click', openLightbox);
  if (lbClose) lbClose.addEventListener('click', closeLightbox);
  if (lightbox) {
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && lightbox && !lightbox.hidden) closeLightbox();
  });
})();
