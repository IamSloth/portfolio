// Language + Theme toggle + Animations
(function () {
  // Language
  var lang = localStorage.getItem('lang') || 'ko';
  document.body.classList.add(lang);

  // Theme
  var theme = localStorage.getItem('theme');
  if (!theme) {
    theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  if (theme === 'dark') document.body.classList.add('dark');

  document.addEventListener('click', function (e) {
    // Language toggle
    var langBtn = e.target.closest('.lang-toggle');
    if (langBtn) {
      var newLang = document.body.classList.contains('ko') ? 'en' : 'ko';
      document.body.classList.remove('ko', 'en');
      document.body.classList.add(newLang);
      localStorage.setItem('lang', newLang);
      document.documentElement.lang = newLang;
      langBtn.querySelector('[data-lang="ko"]').classList.toggle('active', newLang === 'ko');
      langBtn.querySelector('[data-lang="en"]').classList.toggle('active', newLang === 'en');
    }

    // Menu toggle (mobile)
    var menuBtn = e.target.closest('.menu-toggle');
    if (menuBtn) {
      menuBtn.classList.toggle('open');
      var navLinks = document.querySelector('.nav-links');
      if (navLinks) navLinks.classList.toggle('open');
    }

    // Close menu when clicking a nav link
    var clickedNavLink = e.target.closest('.nav-link');
    if (clickedNavLink) {
      var menuToggle = document.querySelector('.menu-toggle');
      var navLinksEl = document.querySelector('.nav-links');
      if (menuToggle) menuToggle.classList.remove('open');
      if (navLinksEl) navLinksEl.classList.remove('open');
    }

    // Theme toggle
    var themeBtn = e.target.closest('.theme-toggle');
    if (themeBtn) {
      document.body.classList.toggle('dark');
      localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
    }
  });

  // ===== Scroll Reveal =====
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var revealObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach(function (el) { revealObs.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('visible'); });
  }

  // ===== Count-Up Animation =====
  var countEls = document.querySelectorAll('.count-up');
  if (countEls.length && 'IntersectionObserver' in window) {
    var countObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          countObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    countEls.forEach(function (el) { countObs.observe(el); });
  }

  function animateCount(el) {
    var target = parseFloat(el.getAttribute('data-target'));
    var decimal = parseInt(el.getAttribute('data-decimal')) || 0;
    var duration = 1200;
    var start = performance.now();

    function step(now) {
      var progress = Math.min((now - start) / duration, 1);
      var ease = 1 - Math.pow(1 - progress, 3);
      var current = target * ease;
      el.textContent = decimal > 0 ? current.toFixed(decimal) : Math.round(current);
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // ===== Tool Bar Animation =====
  var toolFills = document.querySelectorAll('.tool-fill');
  if (toolFills.length && 'IntersectionObserver' in window) {
    var barObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var w = entry.target.getAttribute('data-width');
          entry.target.style.width = w + '%';
          entry.target.style.setProperty('--print-width', w + '%');
          barObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    toolFills.forEach(function (el) { barObs.observe(el); });
  }

  // ===== 3D Card Tilt Effect =====
  var tiltCards = document.querySelectorAll('.project-card, .showcase-card');
  tiltCards.forEach(function (card) {
    card.addEventListener('mousemove', function (e) {
      var rect = card.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;
      var centerX = rect.width / 2;
      var centerY = rect.height / 2;
      var rotateX = (y - centerY) / centerY * -4;
      var rotateY = (x - centerX) / centerX * 4;
      card.style.transform = 'translateY(-10px) scale(1.02) perspective(800px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg)';
    });

    card.addEventListener('mouseleave', function () {
      card.style.transform = '';
    });
  });

  // ===== Nav Background on Scroll =====
  var nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
      } else {
        nav.style.boxShadow = '';
      }
    });
  }

  // ===== Scroll Spy =====
  var navLinks = document.querySelectorAll('.nav-link');
  var sections = [];
  navLinks.forEach(function (link) {
    var href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      var sec = document.querySelector(href);
      if (sec) sections.push({ el: sec, link: link });
    }
  });

  if (sections.length) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          var scrollY = window.scrollY + 100;
          var current = null;
          sections.forEach(function (s) {
            if (s.el.offsetTop <= scrollY) current = s;
          });
          navLinks.forEach(function (l) { l.classList.remove('active'); });
          if (current) current.link.classList.add('active');
          ticking = false;
        });
        ticking = true;
      }
    });
  }
})();
