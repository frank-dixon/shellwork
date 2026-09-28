/**
 * Shellwork flip-zine — page-turn, Simple/Advanced depth, egg demos.
 * Source is commented; npm run watch minifies into docs/js/.
 */
(function () {
  'use strict';

  var DEPTH_KEY = 'shellwork-depth';
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /** @type {HTMLElement} */
  var book = document.getElementById('book');
  /** @type {NodeListOf<HTMLElement>} */
  var leaves = document.querySelectorAll('.book-leaf');
  var pageLabel = document.getElementById('page-label');
  var btnPrev = document.getElementById('btn-prev');
  var btnNext = document.getElementById('btn-next');
  var depthButtons = document.querySelectorAll('[data-depth]');
  var colorSwatches = document.querySelectorAll('[data-egg-color]');
  var shapeRange = document.getElementById('shape-range');
  var sizeRange = document.getElementById('size-range');
  var demoEgg = document.getElementById('demo-egg');
  var shapeEgg = document.getElementById('shape-egg');
  var sizeEgg = document.getElementById('size-egg');
  var sizeCaption = document.getElementById('size-caption');

  // Index of the next leaf that will flip (0 = none flipped yet)
  var flipIndex = 0;
  var totalLeaves = leaves.length;
  // Visible spread count: cover + each leaf face pair ≈ leaves + 1
  var maxFlip = totalLeaves;

  function setDepth(mode) {
    var next = mode === 'advanced' ? 'advanced' : 'simple';
    document.documentElement.setAttribute('data-depth', next);
    depthButtons.forEach(function (btn) {
      var on = btn.getAttribute('data-depth') === next;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.classList.toggle('is-active', on);
    });
    try {
      localStorage.setItem(DEPTH_KEY, next);
    } catch (e) { /* ignore */ }
  }

  function updateChrome() {
    var page = Math.min(flipIndex + 1, maxFlip + 1);
    var total = maxFlip + 1;
    if (pageLabel) {
      pageLabel.textContent = 'Page ' + page + ' of ' + total;
    }
    if (btnPrev) btnPrev.disabled = flipIndex <= 0;
    if (btnNext) btnNext.disabled = flipIndex >= maxFlip;
  }

  function flipTo(index) {
    var target = Math.max(0, Math.min(maxFlip, index));
    flipIndex = target;
    leaves.forEach(function (leaf, i) {
      var flipped = i < flipIndex;
      leaf.classList.toggle('is-flipped', flipped);
      leaf.classList.toggle('is-turning', false);
      // Stacking: flipped leaves sit under; upcoming leaf on top
      leaf.style.zIndex = String(flipped ? i : totalLeaves - i);
    });
    updateChrome();
  }

  function flipNext() {
    if (flipIndex >= maxFlip) return;
    var leaf = leaves[flipIndex];
    if (leaf && !reducedMotion) leaf.classList.add('is-turning');
    flipTo(flipIndex + 1);
  }

  function flipPrev() {
    if (flipIndex <= 0) return;
    flipTo(flipIndex - 1);
  }

  // --- Egg demos -----------------------------------------------------------

  var COLORS = {
    white: { fill: 'linear-gradient(145deg, #fffef9 0%, #f3eee4 55%, #e7dfd2 100%)', speckled: false },
    tint: { fill: 'linear-gradient(145deg, #f7e7c8 0%, #efd4a4 55%, #e2c08a 100%)', speckled: false },
    brown: { fill: 'linear-gradient(145deg, #c9956a 0%, #a86d42 50%, #8a5330 100%)', speckled: true },
    blue: { fill: 'linear-gradient(145deg, #b7d6d8 0%, #7fb0b6 50%, #5a9399 100%)', speckled: false },
    olive: { fill: 'linear-gradient(145deg, #9aaa6e 0%, #6f7f45 55%, #556334 100%)', speckled: true },
  };

  function setEggColor(name) {
    var conf = COLORS[name] || COLORS.white;
    if (!demoEgg) return;
    demoEgg.style.background = conf.fill;
    demoEgg.classList.toggle('egg-speckle', !!conf.speckled);
    colorSwatches.forEach(function (btn) {
      var on = btn.getAttribute('data-egg-color') === name;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.classList.toggle('ring-2', on);
      btn.classList.toggle('ring-terra', on);
    });
  }

  /**
   * Shape slider 0–100: round (wide) → classic → elongated/pointed.
   * Uses border-radius percentages to morph the silhouette.
   */
  function setShape(value) {
    var v = Number(value);
    if (!shapeEgg) return;
    // Top lobes vs bottom lobes; higher v = more pointed top, elongated
    var top = 52 + v * 0.18;
    var bottom = 48 - v * 0.12;
    var side = 50 - v * 0.08;
    shapeEgg.style.borderRadius =
      side + '% ' + side + '% ' + side + '% ' + side + '% / ' +
      top + '% ' + top + '% ' + bottom + '% ' + bottom + '%';
    var scaleY = 1 + v * 0.0025;
    var scaleX = 1 - v * 0.0018;
    shapeEgg.style.transform = 'scale(' + scaleX + ', ' + scaleY + ')';
  }

  var SIZE_LABELS = [
    { max: 16, label: 'Peewee · about 1.25 oz (35 g)' },
    { max: 33, label: 'Small · about 1.5 oz (43 g)' },
    { max: 50, label: 'Medium · about 1.75 oz (50 g)' },
    { max: 66, label: 'Large · about 2 oz (57 g)' },
    { max: 83, label: 'Extra Large · about 2.25 oz (64 g)' },
    { max: 100, label: 'Jumbo · about 2.5 oz (71 g)+' },
  ];

  function setSize(value) {
    var v = Number(value);
    if (!sizeEgg) return;
    var scale = 0.55 + (v / 100) * 0.7;
    sizeEgg.style.transform = 'scale(' + scale + ')';
    if (sizeCaption) {
      var label = SIZE_LABELS[SIZE_LABELS.length - 1].label;
      for (var i = 0; i < SIZE_LABELS.length; i++) {
        if (v <= SIZE_LABELS[i].max) {
          label = SIZE_LABELS[i].label;
          break;
        }
      }
      sizeCaption.textContent = label;
    }
  }

  // --- Pointer drag on the book --------------------------------------------

  var drag = { active: false, startX: 0 };

  function onPointerDown(e) {
    if (!book) return;
    drag.active = true;
    drag.startX = e.clientX || (e.touches && e.touches[0].clientX) || 0;
  }

  function onPointerUp(e) {
    if (!drag.active) return;
    drag.active = false;
    var endX = e.clientX || (e.changedTouches && e.changedTouches[0].clientX) || drag.startX;
    var dx = endX - drag.startX;
    if (Math.abs(dx) < 40) return;
    if (dx < 0) flipNext();
    else flipPrev();
  }

  // --- Wire up -------------------------------------------------------------

  if (btnNext) btnNext.addEventListener('click', flipNext);
  if (btnPrev) btnPrev.addEventListener('click', flipPrev);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'PageDown') {
      e.preventDefault();
      flipNext();
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      flipPrev();
    }
  });

  depthButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      setDepth(btn.getAttribute('data-depth'));
    });
  });

  colorSwatches.forEach(function (btn) {
    btn.addEventListener('click', function () {
      setEggColor(btn.getAttribute('data-egg-color'));
    });
  });

  if (shapeRange) {
    shapeRange.addEventListener('input', function () {
      setShape(shapeRange.value);
    });
  }
  if (sizeRange) {
    sizeRange.addEventListener('input', function () {
      setSize(sizeRange.value);
    });
  }

  if (book) {
    book.addEventListener('pointerdown', onPointerDown);
    window.addEventListener('pointerup', onPointerUp);
  }

  // Click right half of top leaf to advance (when not dragging far)
  leaves.forEach(function (leaf, i) {
    leaf.addEventListener('click', function (e) {
      if (Math.abs((e.clientX || 0) - drag.startX) > 40) return;
      if (i !== flipIndex) return;
      var rect = leaf.getBoundingClientRect();
      var mid = rect.left + rect.width / 2;
      if (e.clientX >= mid) flipNext();
      else flipPrev();
    });
  });

  // Init
  var saved = 'simple';
  try {
    saved = localStorage.getItem(DEPTH_KEY) || 'simple';
  } catch (e) { /* ignore */ }
  setDepth(saved);
  setEggColor('brown');
  setShape(shapeRange ? shapeRange.value : 35);
  setSize(sizeRange ? sizeRange.value : 50);
  flipTo(0);
})();
