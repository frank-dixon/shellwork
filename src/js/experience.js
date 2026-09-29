/**
 * Shellwork immersive experience — parallax, ambient drift, scene reveals,
 * Simple/Advanced depth, searchable breed picker, shape/size controls.
 * Commented source; npm run watch bundles + minifies into docs/js/.
 */
import { BREEDS, EGG_FAMILIES, EGG_SHELL_STYLE, getBreedById } from './breeds.js';

(function () {
  'use strict';

  var DEPTH_KEY = 'shellwork-depth';
  var BREED_KEY = 'shellwork-breed';
  var FILTER_KEY = 'shellwork-egg-filter';
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var depthButtons = document.querySelectorAll('.depth-btn[data-depth]');
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

  var filterBar = document.getElementById('breed-filters');
  var searchInput = document.getElementById('breed-search');
  var breedList = document.getElementById('breed-list');
  var breedCardHost = document.getElementById('breed-card-host');
  var breedCountEl = document.getElementById('breed-count');
  var breedEmpty = document.getElementById('breed-empty');

  var activeFamily = 'all';
  var activeBreedId = 'rir';
  var searchQuery = '';

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

  /* ---------- Breed filter / search ---------- */
  function familyLabel(id) {
    for (var i = 0; i < EGG_FAMILIES.length; i++) {
      if (EGG_FAMILIES[i].id === id) return EGG_FAMILIES[i].label;
    }
    return id;
  }

  function filteredBreeds() {
    var q = searchQuery.trim().toLowerCase();
    return BREEDS.filter(function (b) {
      if (activeFamily !== 'all' && b.eggColorFamily !== activeFamily) return false;
      if (!q) return true;
      var hay = (b.name + ' ' + b.eggColorLabel + ' ' + b.tagline + ' ' + b.eggSize).toLowerCase();
      return hay.indexOf(q) !== -1;
    });
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderFilters() {
    if (!filterBar) return;
    var html = '<button type="button" class="breed-filter-btn' + (activeFamily === 'all' ? ' is-active' : '') + '" data-family="all" aria-pressed="' + (activeFamily === 'all' ? 'true' : 'false') + '">All</button>';
    EGG_FAMILIES.forEach(function (f) {
      var on = activeFamily === f.id;
      html += '<button type="button" class="breed-filter-btn' + (on ? ' is-active' : '') + '" data-family="' + f.id + '" aria-pressed="' + (on ? 'true' : 'false') + '">' + escapeHtml(f.short) + '</button>';
    });
    filterBar.innerHTML = html;
    filterBar.querySelectorAll('[data-family]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeFamily = btn.getAttribute('data-family') || 'all';
        try { localStorage.setItem(FILTER_KEY, activeFamily); } catch (e) { /* ignore */ }
        renderFilters();
        renderBreedList();
      });
    });
  }

  function renderBreedList() {
    if (!breedList) return;
    var list = filteredBreeds();
    if (breedCountEl) {
      breedCountEl.textContent = list.length + ' of ' + BREEDS.length + ' breeds';
    }
    if (!list.length) {
      breedList.innerHTML = '';
      if (breedEmpty) breedEmpty.classList.remove('hidden');
      if (breedCardHost) breedCardHost.innerHTML = '';
      return;
    }
    if (breedEmpty) breedEmpty.classList.add('hidden');

    var stillVisible = list.some(function (b) { return b.id === activeBreedId; });
    if (!stillVisible) activeBreedId = list[0].id;

    var html = '';
    list.forEach(function (b) {
      var on = b.id === activeBreedId;
      html += '<button type="button" role="tab" data-breed="' + escapeHtml(b.id) + '" aria-pressed="' + (on ? 'true' : 'false') + '" class="breed-pick-btn' + (on ? ' is-active' : '') + '">' +
        '<span class="breed-pick-egg" style="background:' + EGG_SHELL_STYLE[b.eggColorFamily].bg + '" aria-hidden="true"></span>' +
        '<span class="breed-pick-text"><span class="breed-pick-name">' + escapeHtml(b.name) + '</span>' +
        '<span class="breed-pick-meta">' + escapeHtml(b.eggColorLabel) + ' · ' + escapeHtml(b.eggSize) + '</span></span></button>';
    });
    breedList.innerHTML = html;
    breedList.querySelectorAll('[data-breed]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        setBreed(btn.getAttribute('data-breed'));
      });
    });
    renderBreedCard();
  }

  function photoCaption(breed) {
    if (!breed.photoCredit) return '';
    var credit = escapeHtml(breed.photoCredit);
    if (breed.photoSource) {
      credit = '<a href="' + escapeHtml(breed.photoSource) + '" class="underline-offset-2 hover:text-teal hover:underline" target="_blank" rel="noopener noreferrer">' + credit + '</a>';
    }
    return '<figcaption class="px-3 py-2 text-xs text-ink-mute">' + credit + '</figcaption>';
  }

  function henVisual(breed) {
    if (breed.photo) {
      return '<figure class="overflow-hidden rounded-xl border border-ink/10 bg-cream">' +
        '<img src="' + escapeHtml(breed.photo) + '" alt="' + escapeHtml(breed.photoAlt || breed.name + ' hen') + '" class="h-56 w-full object-cover object-top sm:h-72" width="400" height="300" loading="lazy" />' +
        photoCaption(breed) + '</figure>';
    }
    var shell = EGG_SHELL_STYLE[breed.eggColorFamily];
    return '<figure class="overflow-hidden rounded-xl border border-ink/10 bg-cream">' +
      '<div class="hen-placeholder flex h-56 flex-col items-center justify-center gap-3 sm:h-72" style="--egg-bg:' + shell.bg + '">' +
      '<div class="hen-silhouette" aria-hidden="true"></div>' +
      '<div class="egg-shell h-12 w-9' + (shell.speckled ? ' egg-speckle' : '') + '" style="background:' + shell.bg + '" aria-hidden="true"></div>' +
      '<p class="px-4 text-center text-xs font-semibold text-ink-soft">' + escapeHtml(breed.name) + '</p>' +
      '</div>' +
      photoCaption(breed) + '</figure>';
  }

  function renderBreedCard() {
    if (!breedCardHost) return;
    var breed = getBreedById(activeBreedId);
    var shell = EGG_SHELL_STYLE[breed.eggColorFamily];
    var sourcesHtml = breed.sources.map(function (s) {
      return '<a href="' + escapeHtml(s.url) + '" class="text-teal underline-offset-2 hover:underline" target="_blank" rel="noopener noreferrer">' + escapeHtml(s.label) + '</a>';
    }).join(' · ');

    breedCardHost.innerHTML =
      '<article class="pair-card grid gap-4 rounded-2xl border border-ink/10 bg-cream-paper p-4 shadow-scene sm:grid-cols-2 sm:p-6" data-breed-card="' + escapeHtml(breed.id) + '">' +
      henVisual(breed) +
      '<div class="flex flex-col gap-2">' +
      '<div class="flex items-center gap-3">' +
      '<div class="egg-shell h-14 w-11 shrink-0' + (shell.speckled ? ' egg-speckle' : '') + '" style="background:' + shell.bg + '" aria-hidden="true"></div>' +
      '<div>' +
      '<h3 class="font-display text-lg leading-snug text-ink">' + escapeHtml(breed.eggColorLabel) + ' egg · ' + escapeHtml(breed.name) + '</h3>' +
      '<p class="text-xs font-semibold uppercase tracking-wider text-teal">' + escapeHtml(breed.tagline) + ' · ' + escapeHtml(familyLabel(breed.eggColorFamily)) + ' · ' + escapeHtml(breed.eggSize) + '</p>' +
      '</div></div>' +
      '<ul class="space-y-1 text-sm leading-snug text-ink-soft">' +
      '<li><span class="font-semibold text-ink">Comb / wattles:</span> ' + escapeHtml(breed.henTraits.comb) + '</li>' +
      '<li><span class="font-semibold text-ink">Plumage:</span> ' + escapeHtml(breed.henTraits.plumage) + '</li>' +
      '<li><span class="font-semibold text-ink">Body / posture:</span> ' + escapeHtml(breed.henTraits.body) + '</li>' +
      '<li><span class="font-semibold text-ink">Legs:</span> ' + escapeHtml(breed.henTraits.legs) + '</li>' +
      '</ul>' +
      '<p class="simple text-sm leading-relaxed text-ink-soft" data-depth-block="simple">' + escapeHtml(breed.simpleCopy) + '</p>' +
      '<p class="advanced hidden text-sm leading-relaxed text-ink-soft" data-depth-block="advanced">' + escapeHtml(breed.advancedCopy) + '</p>' +
      '<p class="mt-1 text-[0.7rem] leading-relaxed text-ink-mute">Sources: ' + sourcesHtml + '</p>' +
      '</div></article>';
  }

  /* ---------- Photo credits (Sources scene) ---------- */
  function renderPhotoCredits() {
    var host = document.getElementById('photo-credits-list');
    if (!host) return;
    var seen = {};
    var html = '';
    BREEDS.forEach(function (b) {
      if (!b.photo || !b.photoCredit || seen[b.photo]) return;
      seen[b.photo] = true;
      var credit = escapeHtml(b.photoCredit.replace(/^Photo( \([^)]*\))?: /, ''));
      if (b.photoSource) {
        credit = '<a href="' + escapeHtml(b.photoSource) + '" class="text-teal hover:underline" target="_blank" rel="noopener noreferrer">' + credit + '</a>';
      }
      html += '<li><span class="font-semibold text-ink-soft">' + escapeHtml(b.name) + '</span>: ' + credit + '</li>';
    });
    host.innerHTML = html;
  }

  function setBreed(id) {
    activeBreedId = id || 'rir';
    try { localStorage.setItem(BREED_KEY, activeBreedId); } catch (e) { /* ignore */ }
    renderBreedList();
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
  if (shapeRange) shapeRange.addEventListener('input', function () { setShape(shapeRange.value); });
  if (sizeRange) sizeRange.addEventListener('input', function () { setSize(sizeRange.value); });
  navDots.forEach(function (dot) {
    dot.addEventListener('click', function () {
      scrollToScene(dot.getAttribute('data-scene-nav'));
    });
  });
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      searchQuery = searchInput.value || '';
      renderBreedList();
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', updateActiveScene);

  /* ---------- Boot ---------- */
  var savedDepth = 'simple';
  var savedBreed = 'rir';
  var savedFilter = 'all';
  try {
    savedDepth = localStorage.getItem(DEPTH_KEY) || 'simple';
    savedBreed = localStorage.getItem(BREED_KEY) || 'rir';
    savedFilter = localStorage.getItem(FILTER_KEY) || 'all';
  } catch (e) { /* ignore */ }

  activeBreedId = getBreedById(savedBreed).id;
  activeFamily = savedFilter;

  setDepth(savedDepth);
  renderFilters();
  renderBreedList();
  renderPhotoCredits();
  setShape(shapeRange ? shapeRange.value : 35);
  setSize(sizeRange ? sizeRange.value : 55);
  buildAmbient();
  observeReveals();
  applyParallax();
  updateActiveScene();
})();
