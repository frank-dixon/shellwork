/**
 * Shellwork immersive experience — parallax, ambient drift, scene reveals,
 * Simple/Advanced depth, breed cards, shape/size controls.
 * Commented source; npm run watch minifies into docs/js/.
 */
(function () {
  'use strict';

  var DEPTH_KEY = 'shellwork-depth';
  var BREED_KEY = 'shellwork-breed';
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var depthButtons = document.querySelectorAll('.depth-btn[data-depth]');
  var breedTabs = document.querySelectorAll('[data-breed]');
  var breedCards = document.querySelectorAll('[data-breed-card]');
  var shapeRange = document.getElementById('shape-range');
  var sizeRange = document.getElementById('size-range');
  var shapeEgg = document.getElementById('shape-egg');
  var sizeEgg = document.getElementById('size-egg');
  var sizeCaption = document.getElementById('size-caption');
  var scenes = document.querySelectorAll('[data-scene]');
  var navDots = document.querySelectorAll('[data-scene-nav]');
  var parallaxLayers = document.querySelectorAll('[data-parallax]');
  var reveals = document.querySelectorAll('.scene-reveal');
  var ambientStage = document.getElementById('ambient-stage');

  /* ---------- Simple ↔ Advanced ---------- */
  function setDepth(mode) {
    var next = mode === 'advanced' ? 'advanced' : 'simple';
    document.documentElement.setAttribute('data-depth', next);
    depthButtons.forEach(function (btn) {
      var on = btn.getAttribute('data-depth') === next;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.classList.toggle('is-active', on);
    });
    try { localStorage.setItem(DEPTH_KEY, next); } catch (e) { /* ignore */ }
  }

  /* ---------- Breed tabs (color scene) ---------- */
  function setBreed(id) {
    var next = id || 'leghorn';
    breedTabs.forEach(function (btn) {
      var on = btn.getAttribute('data-breed') === next;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.classList.toggle('is-active', on);
    });
    breedCards.forEach(function (card) {
      var on = card.getAttribute('data-breed-card') === next;
      card.classList.toggle('hidden', !on);
      card.setAttribute('aria-hidden', on ? 'false' : 'true');
    });
    try { localStorage.setItem(BREED_KEY, next); } catch (e) { /* ignore */ }
  }

  /* ---------- Shape morph ---------- */
  function setShape(value) {
    var v = Number(value);
    if (!shapeEgg) return;
    var top = 52 + v * 0.18;
    var bottom = 48 - v * 0.12;
    var side = 50 - v * 0.08;
    shapeEgg.style.borderRadius =
      side + '% ' + side + '% ' + side + '% ' + side + '% / ' +
      top + '% ' + top + '% ' + bottom + '% ' + bottom + '%';
    shapeEgg.style.transform = 'scale(' + (1 - v * 0.0018) + ', ' + (1 + v * 0.0025) + ')';
  }

  /* ---------- Size scale ---------- */
  var SIZE_LABELS = [
    { max: 16, label: 'Peewee · ~1.25 oz (35 g) · bantam / very young pullet' },
    { max: 33, label: 'Small · ~1.5 oz (43 g) · early lay for many light breeds' },
    { max: 50, label: 'Medium · ~1.75 oz (50 g) · common for Leghorn & young dual-purpose' },
    { max: 66, label: 'Large · ~2 oz (57 g) · grocery baseline for brown layers' },
    { max: 83, label: 'Extra Large · ~2.25 oz (64 g) · mature Orpington / heavy dual-purpose' },
    { max: 100, label: 'Jumbo · ~2.5 oz (71 g)+ · older heavy hens' },
  ];

  function setSize(value) {
    var v = Number(value);
    if (!sizeEgg) return;
    sizeEgg.style.transform = 'scale(' + (0.55 + (v / 100) * 0.7) + ')';
    if (sizeCaption) {
      var label = SIZE_LABELS[SIZE_LABELS.length - 1].label;
      for (var i = 0; i < SIZE_LABELS.length; i++) {
        if (v <= SIZE_LABELS[i].max) { label = SIZE_LABELS[i].label; break; }
      }
      sizeCaption.textContent = label;
    }
  }

  /* ---------- Ambient particles / soft shapes ---------- */
  function buildAmbient() {
    if (!ambientStage || reducedMotion) return;

    var blobs = [
      { className: 'ambient-blob w-[42vw] h-[42vw] left-[-8%] top-[8%] animate-floaty', delay: '0s' },
      { className: 'ambient-blob w-[36vw] h-[36vw] right-[-10%] top-[38%] animate-drift', delay: '-4s' },
      { className: 'ambient-blob w-[28vw] h-[28vw] left-[20%] bottom-[5%] animate-haze', delay: '-8s' },
    ];
    blobs.forEach(function (b) {
      var el = document.createElement('div');
      el.className = b.className;
      el.style.animationDelay = b.delay;
      el.setAttribute('aria-hidden', 'true');
      ambientStage.appendChild(el);
    });

    var clouds = [
      { className: 'ambient-cloud w-[48vw] h-[22vw] left-[5%] top-[18%] animate-haze', delay: '-2s' },
      { className: 'ambient-cloud w-[40vw] h-[18vw] right-[8%] bottom-[22%] animate-drift', delay: '-6s' },
    ];
    clouds.forEach(function (c) {
      var el = document.createElement('div');
      el.className = c.className;
      el.style.animationDelay = c.delay;
      el.setAttribute('aria-hidden', 'true');
      ambientStage.appendChild(el);
    });

    for (var i = 0; i < 18; i++) {
      var p = document.createElement('span');
      var size = 4 + Math.random() * 8;
      p.className = 'ambient-particle';
      p.style.width = size + 'px';
      p.style.height = size + 'px';
      p.style.left = (Math.random() * 100) + '%';
      p.style.top = (Math.random() * 100) + '%';
      p.style.opacity = String(0.25 + Math.random() * 0.45);
      p.style.animation = 'floaty ' + (10 + Math.random() * 14) + 's ease-in-out infinite';
      p.style.animationDelay = (-Math.random() * 12) + 's';
      p.setAttribute('aria-hidden', 'true');
      ambientStage.appendChild(p);
    }
  }

  /* ---------- Parallax on scroll ---------- */
  var ticking = false;
  function applyParallax() {
    ticking = false;
    if (reducedMotion) return;
    var scrollY = window.scrollY || window.pageYOffset;
    parallaxLayers.forEach(function (layer) {
      var speed = parseFloat(layer.getAttribute('data-parallax') || '0.2');
      var y = scrollY * speed * -0.35;
      layer.style.transform = 'translate3d(0, ' + y.toFixed(2) + 'px, 0)';
    });
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(applyParallax);
    }
    updateActiveScene();
  }

  /* ---------- Scene nav + soft reveal ---------- */
  function updateActiveScene() {
    var mid = window.innerHeight * 0.4;
    var activeId = null;
    scenes.forEach(function (scene) {
      var rect = scene.getBoundingClientRect();
      if (rect.top <= mid && rect.bottom >= mid) {
        activeId = scene.getAttribute('data-scene');
      }
    });
    if (!activeId) return;
    navDots.forEach(function (dot) {
      var on = dot.getAttribute('data-scene-nav') === activeId;
      dot.classList.toggle('is-active', on);
      dot.setAttribute('aria-current', on ? 'true' : 'false');
    });
  }

  function observeReveals() {
    if (!('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('is-inview'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-inview');
        }
      });
    }, { threshold: 0.18, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  }

  function scrollToScene(id) {
    var target = document.querySelector('[data-scene="' + id + '"]');
    if (!target) return;
    target.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
  }

  /* ---------- Wire events ---------- */
  depthButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      setDepth(btn.getAttribute('data-depth'));
    });
  });
  breedTabs.forEach(function (btn) {
    btn.addEventListener('click', function () {
      setBreed(btn.getAttribute('data-breed'));
    });
  });
  if (shapeRange) shapeRange.addEventListener('input', function () { setShape(shapeRange.value); });
  if (sizeRange) sizeRange.addEventListener('input', function () { setSize(sizeRange.value); });
  navDots.forEach(function (dot) {
    dot.addEventListener('click', function () {
      scrollToScene(dot.getAttribute('data-scene-nav'));
    });
  });
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', updateActiveScene);

  /* ---------- Boot ---------- */
  var savedDepth = 'simple';
  var savedBreed = 'rir';
  try {
    savedDepth = localStorage.getItem(DEPTH_KEY) || 'simple';
    savedBreed = localStorage.getItem(BREED_KEY) || 'rir';
  } catch (e) { /* ignore */ }

  setDepth(savedDepth);
  setBreed(savedBreed);
  setShape(shapeRange ? shapeRange.value : 35);
  setSize(sizeRange ? sizeRange.value : 55);
  buildAmbient();
  observeReveals();
  applyParallax();
  updateActiveScene();
})();
