// Lightweight vanilla-JS replacement for the Bootstrap components used on this site:
// modals, collapsibles (navbar + accordion) and pill tabs. No external dependencies.

(function () {
  'use strict';

  function ready(fn) {
    if (document.readyState !== 'loading') {
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
  }

  // ---------------------------------------------------------------- Modals
  ready(function () {
    document.addEventListener('click', function (event) {
      var trigger = event.target.closest('[data-bs-toggle="modal"]');
      if (trigger) {
        event.preventDefault();
        var targetId = trigger.getAttribute('data-bs-target');
        if (targetId) openModal(targetId);
        return;
      }

      var dismiss = event.target.closest('[data-bs-dismiss="modal"]');
      if (dismiss) {
        var modal = dismiss.closest('.modal');
        if (modal) closeModal(modal);
        return;
      }

      var backdrop = event.target.closest('.modal-backdrop');
      if (backdrop) {
        var activeModal = document.querySelector('.modal.show');
        if (activeModal) closeModal(activeModal);
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        var activeModal = document.querySelector('.modal.show');
        if (activeModal) closeModal(activeModal);
      }
    });
  });

  function openModal(targetId) {
    var modal = document.getElementById(targetId.replace(/^#/, ''));
    if (!modal || modal.classList.contains('show')) return;

    var lastFocused = document.activeElement;

    modal.classList.add('show');
    modal.setAttribute('aria-hidden', 'false');
    modal.style.display = 'block';
    document.body.classList.add('modal-open');
    document.body.style.overflow = 'hidden';
    document.body.style.paddingRight = getScrollbarWidth() + 'px';

    var backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop fade show';
    document.body.appendChild(backdrop);

    var focusable = modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    var firstEl = focusable[0];
    if (firstEl) {
      setTimeout(function () {
        firstEl.focus();
      }, 120);
    }

    // Store reference for later dismissal
    modal._lastFocused = lastFocused;
    modal._backdrop = backdrop;
  }

  function closeModal(modal) {
    if (!modal) return;

    modal.classList.remove('show');
    modal.setAttribute('aria-hidden', 'true');
    setTimeout(function () {
      modal.style.display = 'none';
    }, 200);

    if (modal._backdrop) {
      modal._backdrop.remove();
      modal._backdrop = null;
    }

    var anyOpen = document.querySelector('.modal.show');
    if (!anyOpen) {
      document.body.classList.remove('modal-open');
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    }

    if (modal._lastFocused) {
      modal._lastFocused.focus();
      modal._lastFocused = null;
    }
  }

  function getScrollbarWidth() {
    var div = document.createElement('div');
    div.style.overflowY = 'scroll';
    div.style.width = '50px';
    div.style.height = '50px';
    div.style.visibility = 'hidden';
    document.body.appendChild(div);
    var width = div.offsetWidth - div.clientWidth;
    document.body.removeChild(div);
    return width;
  }

  // ---------------------------------------------------------------- Collapse
  ready(function () {
    document.addEventListener('click', function (event) {
      var trigger = event.target.closest('[data-bs-toggle="collapse"]');
      if (!trigger) return;
      event.preventDefault();

      var targetId = trigger.getAttribute('data-bs-target');
      var target = targetId ? document.querySelector(targetId) : null;
      if (!target) return;

      var parentSelector = trigger.getAttribute('data-bs-parent');
      var willOpen = !target.classList.contains('show');

      if (parentSelector) {
        var accordion = target.closest(parentSelector);
        if (accordion) {
          accordion.querySelectorAll('.collapse.show').forEach(function (item) {
            if (item !== target) setCollapse(item, false);
          });
        }
      }

      setCollapse(target, willOpen);

      var expanded = trigger.getAttribute('aria-expanded') === 'true';
      trigger.setAttribute('aria-expanded', String(!expanded));
      trigger.classList.toggle('collapsed', expanded);
    });
  });

  function setCollapse(element, open) {
    if (open) {
      element.classList.add('show');
      element.style.height = element.scrollHeight + 'px';
      setTimeout(function () {
        element.style.height = '';
      }, 50);
    } else {
      element.style.height = element.scrollHeight + 'px';
      // Force reflow then collapse
      void element.offsetHeight;
      element.style.height = '0px';
      setTimeout(function () {
        element.classList.remove('show');
        element.style.height = '';
      }, 250);
    }
  }

  // ---------------------------------------------------------------- Tabs / Pills
  ready(function () {
    document.addEventListener('click', function (event) {
      var trigger = event.target.closest('[data-bs-toggle="pill"], [data-bs-toggle="tab"]');
      if (!trigger) return;
      event.preventDefault();

      var targetId = trigger.getAttribute('data-bs-target') || trigger.getAttribute('href');
      if (!targetId || targetId === '#') return;

      var targetPane = document.querySelector(targetId);
      if (!targetPane) return;

      var tabList = trigger.closest('.nav');
      if (tabList) {
        tabList.querySelectorAll('.nav-link').forEach(function (link) {
          link.classList.remove('active');
          link.setAttribute('aria-selected', 'false');
        });
        var paneContainer = targetPane.closest('.tab-content');
        if (paneContainer) {
          paneContainer.querySelectorAll('.tab-pane').forEach(function (pane) {
            pane.classList.remove('show', 'active');
          });
        }
      }

      trigger.classList.add('active');
      trigger.setAttribute('aria-selected', 'true');
      targetPane.classList.add('show', 'active');
    });
  });

  // ---------------------------------------------------------------- Alerts
  ready(function () {
    document.addEventListener('click', function (event) {
      var dismiss = event.target.closest('[data-bs-dismiss="alert"]');
      if (!dismiss) return;
      var alertEl = dismiss.closest('.alert');
      if (!alertEl) return;
      alertEl.classList.remove('show');
      setTimeout(function () {
        alertEl.remove();
      }, 300);
    });
  });

  // ---------------------------------------------------------------- Dropdowns
  ready(function () {
    document.addEventListener('click', function (event) {
      var toggle = event.target.closest('[data-bs-toggle="dropdown"]');
      if (toggle) {
        event.preventDefault();
        event.stopPropagation();
        var menu = toggle.parentElement.querySelector('.dropdown-menu');
        if (menu) {
          menu.classList.toggle('show');
          toggle.setAttribute('aria-expanded', String(menu.classList.contains('show')));
        }
        return;
      }
      document.querySelectorAll('.dropdown-menu.show').forEach(function (menu) {
        menu.classList.remove('show');
        var btn = menu.parentElement.querySelector('[data-bs-toggle="dropdown"]');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      });
    });
  });

  // ---------------------------------------------------------------- Mobile navigation drawer
  ready(function () {
    var toggler = document.querySelector('[data-nav-toggle]');
    var drawer = document.querySelector('[data-nav-drawer]');
    if (!toggler || !drawer) return;

    var closeBtn = drawer.querySelector('[data-nav-close]');
    var backdrop = drawer.querySelector('.mobile-nav-backdrop');

    function openNav() {
      drawer.classList.add('open');
      drawer.setAttribute('aria-hidden', 'false');
      toggler.setAttribute('aria-expanded', 'true');
      document.body.classList.add('nav-open');
    }

    function closeNav() {
      drawer.classList.remove('open');
      drawer.setAttribute('aria-hidden', 'true');
      toggler.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('nav-open');
    }

    toggler.addEventListener('click', function () {
      if (drawer.classList.contains('open')) {
        closeNav();
      } else {
        openNav();
      }
    });

    if (closeBtn) closeBtn.addEventListener('click', closeNav);
    if (backdrop) backdrop.addEventListener('click', closeNav);

    drawer.addEventListener('click', function (event) {
      if (event.target.closest('.mobile-nav-link')) closeNav();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && drawer.classList.contains('open')) closeNav();
    });
  });

  // ---------------------------------------------------------------- Floating WhatsApp button
  ready(function () {
    var whatsappBtn = document.querySelector('[data-whatsapp-number]');
    if (!whatsappBtn) return;

    whatsappBtn.addEventListener('click', function (event) {
      event.preventDefault();
      var number = whatsappBtn.getAttribute('data-whatsapp-number') || '';
      var message = whatsappBtn.getAttribute('data-whatsapp-message') || '';
      var whatsappUrl = 'https://wa.me/' + number;
      if (message) {
        whatsappUrl += '?text=' + encodeURIComponent(message);
      }
      window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
    });
  });

  // ---------------------------------------------------------------- About Read More / Show Less
  ready(function () {
    var toggle = document.getElementById('about-toggle');
    var more = document.getElementById('about-more');
    if (!toggle || !more) return;

    var textEl = toggle.querySelector('.about-toggle-text');
    var iconEl = toggle.querySelector('.about-toggle-icon');

    toggle.addEventListener('click', function () {
      var isOpen = more.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      if (textEl) textEl.textContent = isOpen ? 'Show Less' : 'Read More';
      if (iconEl) iconEl.innerHTML = isOpen ? '&uarr;' : '&rarr;';
    });
  });

  // ---------------------------------------------------------------- FAQ accordion
  ready(function () {
    var faqSection = document.querySelector('.faq-section');
    if (!faqSection) return;

    faqSection.addEventListener('click', function (event) {
      var question = event.target.closest('.faq-question');
      if (!question) return;

      var item = question.closest('.faq-item');
      var isOpen = item.classList.contains('active');

      faqSection.querySelectorAll('.faq-item.active').forEach(function (openItem) {
        openItem.classList.remove('active');
        var openBtn = openItem.querySelector('.faq-question');
        if (openBtn) openBtn.setAttribute('aria-expanded', 'false');
      });

      if (!isOpen) {
        item.classList.add('active');
        question.setAttribute('aria-expanded', 'true');
      }
    });
  });

  // ---------------------------------------------------------------- Navbar autoscroll offset
  ready(function () {
    var navbar = document.querySelector('.navbar');
    if (navbar) {
      // Smooth scroll to anchor links with offset for the fixed navbar
      document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
          var href = this.getAttribute('href');
          if (href === '#' || href === '#!') return;
          var target = document.querySelector(href);
          if (!target) return;
          e.preventDefault();
          var top = target.getBoundingClientRect().top + window.pageYOffset - 70;
          window.scrollTo({ top: top, behavior: 'smooth' });
        });
      });
    }
  });
})();
