/**
 * Shellwork flip-zine — page-turn, Simple/Advanced, breed card focus.
 * Commented source; npm run watch minifies into docs/js/.
 */
(function () {
  'use strict';

  var DEPTH_KEY = 'shellwork-depth';
  var BREED_KEY = 'shellwork-breed';
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var book = document.getElementById('book');
  var leaves = document.querySelectorAll('.book-leaf');
  var pageLabel = document.getElementById('page-label');
  var btnPrev = document.getElementById('btn-prev');
  var btnNext = document.getElementById('btn-next');
  var depthButtons = document.querySelectorAll('[data-depth]');
  var breedTabs = document.querySelectorAll('[data-breed]');
  var breedCards = document.querySelectorAll('[data-breed-card]');
  var shapeRange = document.getElementById('shape-range');
  var sizeRange = document.getElementById('size-range');
  var shapeEgg = document.getElementById('shape-egg');
  var sizeEgg = document.getElementById('size-egg');
  var sizeCaption = document.getElementById('size-caption');

  var flipIndex = 0;
  var totalLeaves = leaves.length;
  var maxFlip = totalLeaves;

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

  function updateChrome() {
    var page = Math.min(flipIndex + 1, maxFlip + 1);
    if (pageLabel) pageLabel.textContent = 'Page ' + page + ' of ' + (maxFlip + 1);
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
    if (Math.abs(dx) < 48) return;
    if (dx < 0) flipNext(); else flipPrev();
  }

  if (btnNext) btnNext.addEventListener('click', flipNext);
  if (btnPrev) btnPrev.addEventListener('click', flipPrev);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); flipNext(); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); flipPrev(); }
  });
  depthButtons.forEach(function (btn) {
    btn.addEventListener('click', function () { setDepth(btn.getAttribute('data-depth')); });
  });
  breedTabs.forEach(function (btn) {
    btn.addEventListener('click', function () { setBreed(btn.getAttribute('data-breed')); });
  });
  if (shapeRange) shapeRange.addEventListener('input', function () { setShape(shapeRange.value); });
  if (sizeRange) sizeRange.addEventListener('input', function () { setSize(sizeRange.value); });
  if (book) {
    book.addEventListener('pointerdown', onPointerDown);
    window.addEventListener('pointerup', onPointerUp);
  }
  leaves.forEach(function (leaf, i) {
    leaf.addEventListener('click', function (e) {
      if (e.target.closest('button, a, input, label, .breed-tabs, .pair-card')) return;
      if (Math.abs((e.clientX || 0) - drag.startX) > 40) return;
      if (i !== flipIndex) return;
      var rect = leaf.getBoundingClientRect();
      if (e.clientX >= rect.left + rect.width / 2) flipNext(); else flipPrev();
    });
  });

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
  flipTo(0);
})();
