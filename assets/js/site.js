/* EMBRACER concept site. Everything here is progressive: pages read without it. */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector('[data-nav-toggle]');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus();
      }
    });
  }

  /* ---------- reveal + parallax ---------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    reveals.forEach(function (el) { var r = el.getBoundingClientRect(); if (r.top < window.innerHeight && r.bottom > 0) { el.classList.add('is-in'); } else { io.observe(el); } });
  } else { reveals.forEach(function (el) { el.classList.add('is-in'); }); }

  var parallax = document.querySelectorAll('.parallax');
  if (parallax.length && !reduce) {
    var tick = false;
    var run = function () {
      parallax.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var mid = r.top + r.height / 2 - window.innerHeight / 2;
        var k = parseFloat(el.dataset.parallax || '0.08');
        el.style.transform = 'translateY(' + (-mid * k).toFixed(1) + 'px)';
      });
      tick = false;
    };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(run); } }, { passive: true });
    run();
  }

  /* ---------- explore (hotspots + panel + list) ---------- */
  document.querySelectorAll('[data-explore]').forEach(function (ex) {
    var panel = ex.querySelector('.explore__panel');
    var topics = Array.prototype.slice.call(panel.querySelectorAll('.topic'));
    var triggers = Array.prototype.slice.call(ex.querySelectorAll('[data-topic]')).filter(function (b) { return b.tagName === 'BUTTON'; });
    var closeBtn = ex.querySelector('[data-explore-close]');
    var hint = document.createElement('p');
    hint.className = 'explore__panel-hint';
    hint.textContent = ex.dataset.hint || 'Choose a point on the image, or pick a topic from the list.';
    panel.insertBefore(hint, panel.firstChild);
    var mobile = window.matchMedia('(max-width: 900px)');

    function show(id, focusPanel) {
      topics.forEach(function (t) { t.hidden = t.dataset.topic !== id; });
      hint.hidden = !!id;
      triggers.forEach(function (b) { b.setAttribute('aria-expanded', String(b.dataset.topic === id)); });
      if (id) {
        panel.classList.add('is-open');
        var t = panel.querySelector('[data-topic="' + id + '"]');
        if (focusPanel && t) { t.focus({ preventScroll: mobile.matches }); }
        if (history.replaceState) { history.replaceState(null, '', '#' + id); }
      } else {
        panel.classList.remove('is-open');
      }
    }
    triggers.forEach(function (b) {
      b.addEventListener('click', function () {
        var id = b.dataset.topic;
        show(b.getAttribute('aria-expanded') === 'true' && !mobile.matches ? null : id, true);
      });
    });
    if (closeBtn) { closeBtn.addEventListener('click', function () { show(null); }); }
    ex.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { show(null); }
      var i = triggers.indexOf(document.activeElement);
      if (i > -1 && (e.key === 'ArrowRight' || e.key === 'ArrowDown')) { e.preventDefault(); triggers[(i + 1) % triggers.length].focus(); }
      if (i > -1 && (e.key === 'ArrowLeft' || e.key === 'ArrowUp')) { e.preventDefault(); triggers[(i - 1 + triggers.length) % triggers.length].focus(); }
    });
    var initial = location.hash.replace('#', '');
    show(topics.some(function (t) { return t.dataset.topic === initial; }) ? initial : null, false);
  });

  /* ---------- publications filter ---------- */
  var pubList = document.querySelector('[data-pub-list]');
  if (pubList) {
    var items = Array.prototype.slice.call(pubList.querySelectorAll('.pub'));
    var q = document.getElementById('pub-q'), year = document.getElementById('pub-year'), type = document.getElementById('pub-type'), proj = document.getElementById('pub-project');
    var count = document.querySelector('[data-pub-count]');
    var empty = document.querySelector('[data-pub-empty]');
    function apply() {
      var s = (q.value || '').toLowerCase().trim(), n = 0;
      items.forEach(function (li) {
        var ok = (!s || (li.textContent + ' ' + (li.dataset.search || '')).toLowerCase().indexOf(s) > -1) &&
          (!year.value || li.dataset.year === year.value) &&
          (!type.value || li.dataset.type === type.value) &&
          (!proj.value || li.dataset.project === proj.value);
        li.hidden = !ok; if (ok) n++;
      });
      if (count) { count.textContent = n + ' of ' + items.length + ' records'; }
      if (empty) { empty.hidden = n > 0; }
    }
    [q, year, type, proj].forEach(function (el) { if (el) { el.addEventListener('input', apply); el.addEventListener('change', apply); } });
    var reset = document.querySelector('[data-pub-reset]');
    if (reset) { reset.addEventListener('click', function () { q.value = ''; year.value = ''; type.value = ''; proj.value = ''; apply(); q.focus(); }); }
    apply();
  }

  /* ---------- forms: client-side states only (no backend in the concept) ---------- */
  document.querySelectorAll('form[data-demo-form]').forEach(function (form) {
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = [];
      form.querySelectorAll('[required]').forEach(function (f) {
        var field = f.closest('.field'); var err = field && field.querySelector('.field__error');
        var ok = f.checkValidity();
        if (field) { field.classList.toggle('field--error', !ok); }
        f.setAttribute('aria-invalid', String(!ok));
        if (err) { err.hidden = ok; }
        if (!ok) { bad.push(f); }
      });
      if (bad.length) {
        bad[0].focus();
        if (status) { status.className = 'form-status form-status--error'; status.textContent = 'Please check the ' + bad.length + (bad.length > 1 ? ' fields' : ' field') + ' marked above.'; status.hidden = false; }
        return;
      }
      if (status) { status.className = 'form-status form-status--ok'; status.textContent = form.dataset.success || 'Thank you. Your message has been received.'; status.hidden = false; }
      form.querySelectorAll('input, textarea, select, button').forEach(function (f) { f.disabled = true; });
      status && status.focus && status.setAttribute('tabindex', '-1');
      status && status.focus();
    });
  });

  /* ---------- admin: hotspot editor mock ---------- */
  var editor = document.querySelector('[data-hotspot-editor]');
  if (editor) {
    var fig = editor.querySelector('.explore__figure');
    var layer = editor.querySelector('.explore__hotspots');
    var props = document.querySelector('[data-hotspot-props]');
    var current = null;
    function pct(e) {
      var r = fig.getBoundingClientRect();
      var x = Math.min(100, Math.max(0, (e.clientX - r.left) / r.width * 100));
      var y = Math.min(100, Math.max(0, (e.clientY - r.top) / r.height * 100));
      return { x: x.toFixed(1), y: y.toFixed(1) };
    }
    function select(b) {
      current = b;
      layer.querySelectorAll('.hotspot').forEach(function (h) { h.setAttribute('aria-expanded', String(h === b)); });
      if (props) {
        props.querySelector('[name=title]').value = b.dataset.title || '';
        props.querySelector('[name=x]').value = b.style.getPropertyValue('--x').replace('%', '');
        props.querySelector('[name=y]').value = b.style.getPropertyValue('--y').replace('%', '');
        props.hidden = false;
      }
    }
    function addAt(p, title) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'hotspot hotspot--rust'; b.dataset.title = title || 'New point';
      b.style.setProperty('--x', p.x + '%'); b.style.setProperty('--y', p.y + '%');
      b.innerHTML = '<span aria-hidden="true">+</span><span class="sr-only">' + b.dataset.title + '</span>';
      b.setAttribute('aria-expanded', 'false');
      layer.appendChild(b); wire(b); select(b);
    }
    function wire(b) {
      var drag = false;
      b.addEventListener('pointerdown', function (e) { drag = true; b.classList.add('is-dragging'); b.setPointerCapture(e.pointerId); select(b); });
      b.addEventListener('pointermove', function (e) { if (!drag) { return; } var p = pct(e); b.style.setProperty('--x', p.x + '%'); b.style.setProperty('--y', p.y + '%'); if (props) { props.querySelector('[name=x]').value = p.x; props.querySelector('[name=y]').value = p.y; } });
      b.addEventListener('pointerup', function () { drag = false; b.classList.remove('is-dragging'); });
      b.addEventListener('keydown', function (e) {
        var dx = { ArrowLeft: -1, ArrowRight: 1 }[e.key] || 0, dy = { ArrowUp: -1, ArrowDown: 1 }[e.key] || 0;
        if (!dx && !dy) { return; }
        e.preventDefault();
        var x = parseFloat(b.style.getPropertyValue('--x')) + dx, y = parseFloat(b.style.getPropertyValue('--y')) + dy;
        b.style.setProperty('--x', Math.min(100, Math.max(0, x)) + '%'); b.style.setProperty('--y', Math.min(100, Math.max(0, y)) + '%'); select(b);
      });
    }
    layer.querySelectorAll('.hotspot').forEach(wire);
    fig.addEventListener('dblclick', function (e) { if (e.target.closest('.hotspot')) { return; } addAt(pct(e)); });
    var addBtn = document.querySelector('[data-hotspot-add]');
    if (addBtn) { addBtn.addEventListener('click', function () { addAt({ x: 50, y: 50 }); }); }
    if (props) {
      props.addEventListener('input', function (e) {
        if (!current) { return; }
        if (e.target.name === 'title') { current.dataset.title = e.target.value; current.querySelector('.sr-only').textContent = e.target.value; }
        if (e.target.name === 'x') { current.style.setProperty('--x', e.target.value + '%'); }
        if (e.target.name === 'y') { current.style.setProperty('--y', e.target.value + '%'); }
      });
      var del = props.querySelector('[data-hotspot-delete]');
      if (del) { del.addEventListener('click', function () { if (current) { current.remove(); current = null; props.hidden = true; } }); }
    }
    document.querySelectorAll('[data-preview]').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('[data-preview]').forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        editor.classList.toggle('is-phone', b.dataset.preview === 'phone');
      });
    });
  }
})();
