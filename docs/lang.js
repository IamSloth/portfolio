// Language + Theme toggle
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
      langBtn.querySelector('[data-lang="ko"]').classList.toggle('active', newLang === 'ko');
      langBtn.querySelector('[data-lang="en"]').classList.toggle('active', newLang === 'en');
    }

    // Theme toggle
    var themeBtn = e.target.closest('.theme-toggle');
    if (themeBtn) {
      document.body.classList.toggle('dark');
      localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
    }
  });
})();
