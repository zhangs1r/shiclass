/**
 * ShiClass Lesson Tools — localStorage-driven learning features (精简版)
 *
 * Features:
 *   1. Mark lesson as completed (shiclass_done + shiclass_vtally)
 *   2. Auto-save / restore scroll position (shiclass_scroll_{lessonId})
 *
 * Auto-detects lesson ID from the URL path. Injects a "标记已学" button
 * after .nav-links on lesson pages. All localStorage access wrapped in try-catch.
 */
(function () {
  'use strict';

  /* ===================================================================
     Safe localStorage helpers
     =================================================================== */
  function getJSON(key, fallback) {
    try { var v = localStorage.getItem(key); return v !== null ? JSON.parse(v) : fallback; }
    catch (_) { return fallback; }
  }
  function setJSON(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch (_) {}
  }

  /* ===================================================================
     Lesson ID detection
     =================================================================== */
  function detectLessonId() {
    var match = window.location.pathname.match(/([^/]+)\.html$/);
    if (!match) return null;
    var name = match[1];
    var d = name.match(/^(\d+)/);
    if (d) return d[1];
    var k = name.match(/^(KF-L\d+)/i);
    if (k) return k[1].toUpperCase();
    var e = name.match(/^([A-Za-z][A-Za-z0-9-]*)/);
    if (e) return e[1];
    return name;
  }

  var LID = detectLessonId();
  if (!LID) return;

  /* ===================================================================
     Inline styles — done button only
     =================================================================== */
  (function injectStyles() {
    if (document.getElementById('scl-style')) return;
    var css = document.createElement('style');
    css.id = 'scl-style';
    css.textContent =
      '.scl-tools{margin-top:20px;padding-top:16px;border-top:1px solid #E8E4DC}' +
      '.scl-btn{display:inline-flex;align-items:center;gap:4px;padding:8px 18px;border:1px solid #CC785C;border-radius:8px;background:#fff;color:#CC785C;font-size:0.9rem;cursor:pointer;transition:background 0.15s,color 0.15s;font-family:inherit;line-height:1.4}' +
      '.scl-btn:hover{background:#CC785C;color:#fff}' +
      '.scl-btn:disabled{opacity:0.5;cursor:default}' +
      '.scl-done,.scl-done:hover{background:#4CAF50;color:#fff;border-color:#4CAF50;opacity:1}';
    document.head.appendChild(css);
  })();

  /* ===================================================================
     1. Mark as completed
     =================================================================== */
  function getDone()        { return getJSON('shiclass_done', []); }
  function setDone(arr)     { setJSON('shiclass_done', arr); }
  function getVTally()      { return getJSON('shiclass_vtally', {}); }
  function setVTally(obj)   { setJSON('shiclass_vtally', obj); }

  function isDone() {
    return getDone().indexOf(LID) !== -1;
  }

  function toggleDone() {
    if (isDone()) return;
    var arr = getDone();
    arr.push(LID);
    setDone(arr);
    var vt = getVTally();
    vt[LID] = new Date().toISOString().slice(0, 10);
    setVTally(vt);
    updateDoneBtn();
  }

  function updateDoneBtn() {
    var btn = document.getElementById('scl-done-btn');
    if (!btn) return;
    if (isDone()) {
      btn.textContent = '\u2705 \u5df2\u5b66\u5b8c';
      btn.disabled = true;
      btn.className = 'scl-btn scl-done';
    } else {
      btn.textContent = '\u2705 \u6807\u8bb0\u4e3a\u5df2\u5b66';
      btn.disabled = false;
      btn.className = 'scl-btn';
    }
  }

  /* ===================================================================
     2. Scroll position save / restore
     =================================================================== */
  function restoreScroll() {
    var y = getJSON('shiclass_scroll_' + LID, null);
    if (typeof y === 'number') {
      requestAnimationFrame(function () { window.scrollTo(0, y); });
    }
  }

  (function initScrollSave() {
    var timer = null;
    window.addEventListener('scroll', function () {
      if (timer) clearTimeout(timer);
      timer = setTimeout(function () {
        setJSON('shiclass_scroll_' + LID, window.scrollY);
      }, 3000);
    }, { passive: true });
  })();

  /* ===================================================================
     Inject UI — done button only
     =================================================================== */
  function injectUI() {
    var nav = document.querySelector('.nav-links');
    if (!nav) return;
    var div = document.createElement('div');
    div.className = 'scl-tools';
    var doneRow = document.createElement('div');
    doneRow.style.cssText = 'margin-bottom:12px;';
    doneRow.innerHTML = '<button id="scl-done-btn" class="scl-btn">\u2705 \u6807\u8bb0\u4e3a\u5df2\u5b66</button>';
    div.appendChild(doneRow);
    nav.parentNode.insertBefore(div, nav.nextSibling);
  }

  /* ===================================================================
     Init
     =================================================================== */
  function init() {
    injectUI();
    updateDoneBtn();
    restoreScroll();
    var doneBtn = document.getElementById('scl-done-btn');
    if (doneBtn) doneBtn.addEventListener('click', toggleDone);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
