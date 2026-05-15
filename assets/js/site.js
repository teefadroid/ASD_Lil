/* ASD International — site interactions */
(function () {
  'use strict';

  // Mobile menu toggle
  var menuBtn = document.querySelector('[data-menu-btn]');
  var mobile  = document.querySelector('[data-mobile-panel]');
  if (menuBtn && mobile) {
    menuBtn.addEventListener('click', function () {
      var open = mobile.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Reveal-on-scroll
  var io = ('IntersectionObserver' in window)
    ? new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add('visible');
            io.unobserve(e.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 })
    : null;
  if (io) {
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('visible'); });
  }

  // Active nav link
  var path = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
  document.querySelectorAll('[data-nav] a').forEach(function (a) {
    var href = a.getAttribute('href').replace(/\/index\.html$/, '/').replace(/\.html$/, '');
    if (href === path || (href === '/' && (path === '' || path === '/'))) {
      a.classList.add('active');
    }
    if (href !== '/' && path.indexOf(href) === 0 && href.length > 1) {
      a.classList.add('active');
    }
  });

  // Product category filter (products page)
  var grid = document.querySelector('[data-product-grid]');
  if (grid) {
    var filters = document.querySelectorAll('[data-filter]');
    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        filters.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        var cat = btn.getAttribute('data-filter');
        grid.querySelectorAll('.product-card').forEach(function (card) {
          var cardCat = card.getAttribute('data-category');
          card.style.display = (cat === 'all' || cardCat === cat) ? '' : 'none';
        });
      });
    });
  }

  // Contact form (client-side only — opens mail client as a no-backend fallback)
  var form = document.querySelector('[data-contact-form]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new FormData(form);
      var subject = encodeURIComponent('Website inquiry — ' + (data.get('subject') || 'General'));
      var body = encodeURIComponent(
        'Name: ' + (data.get('name') || '') + '\n' +
        'Email: ' + (data.get('email') || '') + '\n' +
        'Phone: ' + (data.get('phone') || '') + '\n' +
        'Subject: ' + (data.get('subject') || '') + '\n\n' +
        (data.get('message') || '')
      );
      window.location.href = 'mailto:info@asdinternational.co?subject=' + subject + '&body=' + body;
      var ok = form.querySelector('[data-form-success]');
      if (ok) ok.classList.add('show');
      form.reset();
    });
  }

  // Footer year
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
