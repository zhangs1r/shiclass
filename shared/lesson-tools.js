/**
 * ShiClass Lesson Tools — localStorage-driven learning features
 *
 * Features:
 *   1. Mark lesson as completed (shiclass_done + shiclass_vtally)
 *   2. Auto-save / restore scroll position (shiclass_scroll_{lessonId})
 *   3. Inline formula bookmarking — 📌/✅ toggle on .formula-box elements
 *   4. Inline code snippet bookmarking — 💾/✅ toggle on <pre> elements
 *
 * Bookmark toggle: click 📌 to save, click ✅ to unsave.
 * Stores both raw text (for matching) and innerHTML (for rendered display).
 *
 * Auto-detects lesson ID from the URL path. Injects UI after .nav-links
 * on lesson pages. All localStorage access is wrapped in try-catch.
 * Does not block page rendering (uses requestAnimationFrame / defer).
 */
(function () {
  'use strict';

  /* ===================================================================
     Safe localStorage helpers
     =================================================================== */
  function getJSON(key, fallback) {
    try {
      var v = localStorage.getItem(key);
      return v !== null ? JSON.parse(v) : fallback;
    } catch (_) {
      return fallback;
    }
  }
  function setJSON(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch (_) {}
  }

  /* ===================================================================
     Lesson ID detection — derive stable short key from URL
     =================================================================== */
  function detectLessonId() {
    var match = window.location.pathname.match(/([^/]+)\.html$/);
    if (!match) return null;
    var name = match[1];

    // "0004-KF-L1-矩阵特征值" → "0004"
    var d = name.match(/^(\d+)/);
    if (d) return d[1];

    // "KF-L5-贝叶斯估计与BayesRule" → "KF-L5"
    var k = name.match(/^(KF-L\d+)/i);
    if (k) return k[1].toUpperCase();

    // "SomeEnglishPrefix-中文" → "SomeEnglishPrefix"
    var e = name.match(/^([A-Za-z][A-Za-z0-9-]*)/);
    if (e) return e[1];

    return name;
  }

  var LID = detectLessonId();
  if (!LID) return; // not a lesson page — bail silently

  /* ===================================================================
     Inline styles — explicit colors, no CSS variables
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
      '.scl-done,.scl-done:hover{background:#4CAF50;color:#fff;border-color:#4CAF50;opacity:1}' +
      '.scl-inline-btn{position:absolute;top:4px;right:4px;width:24px;height:24px;display:flex;align-items:center;justify-content:center;border:1px solid #CC785C;border-radius:4px;background:#fff;cursor:pointer;font-size:13px;line-height:1;padding:0;z-index:10;opacity:0.6;transition:opacity 0.15s,background 0.15s}' +
      '.scl-inline-btn:hover{opacity:1;background:#f9f4ee}' +
      '.scl-inline-btn.scl-saved{border-color:#4CAF50;opacity:1;background:#e8f5e9}' +
      '.scl-inline-btn.scl-saved:hover{background:#fce4ec;border-color:#E53935}' +
      '.scl-inline-btn.scl-marked{border-color:#2196F3;opacity:1;background:#e3f2fd}';
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

    // Record date stamp
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
     3. Inline formula bookmarking — 📌/✅ toggle on .formula-box elements
     =================================================================== */
  function getFormulas()       { return getJSON('shiclass_formulas', []); }
  function setFormulas(arr)    { setJSON('shiclass_formulas', arr); }

  function deleteFormula(id) {
    setFormulas(getFormulas().filter(function (f) { return f.id !== id; }));
  }

  /** Delete saved formulas whose raw text matches, within this lesson. */
  function deleteFormulaByText(text) {
    setFormulas(getFormulas().filter(function (f) {
      return !(f.lessonId === LID && f.formula === text);
    }));
  }

  function findSavedFormula(text) {
    var list = getFormulas().filter(function (f) { return f.lessonId === LID; });
    for (var i = 0; i < list.length; i++) {
      if (list[i].formula === text) return list[i].id;
    }
    return null;
  }

  /**
   * Toggle formula bookmark.
   * If text is already saved: remove it and return null.
   * Otherwise: save with both raw text and innerHTML, return the new id.
   */
  function saveInlineFormula(text, html) {
    var existingId = findSavedFormula(text);
    if (existingId) {
      deleteFormulaByText(text);
      return null;
    }
    var list = getFormulas();
    list.push({
      id: 'f_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6),
      lessonId: LID,
      formula: text,
      html: html || text,
      context: '',
      timestamp: new Date().toISOString()
    });
    setFormulas(list);
    return list[list.length - 1].id;
  }

  function scanInlineFormulas() {
    var boxes = document.querySelectorAll('.formula-box');
    for (var i = 0; i < boxes.length; i++) {
      (function (el) {
        // Ensure parent has positioning for absolute button
        if (getComputedStyle(el).position === 'static') {
          el.style.position = 'relative';
        }
        // Skip if button already added (e.g. re-init)
        if (el.querySelector('.scl-inline-btn')) return;

        var text = el.textContent.trim();
        if (!text) return;

        var saved = findSavedFormula(text);
        var btn = document.createElement('button');
        btn.className = 'scl-inline-btn' + (saved ? ' scl-saved' : '');
        btn.textContent = saved ? '\u2705' : '\uD83D\uDCCC';
        btn.setAttribute('data-scl-inline-formula', '1');
        btn.setAttribute('data-scl-text', text);
        btn.title = saved ? '\u5df2\u6536\u85cf \u70b9\u51fb\u53d6\u6d88' : '\u6536\u85cf\u516c\u5f0f';
        el.appendChild(btn);
      })(boxes[i]);
    }
  }

  /* ===================================================================
     4. Inline code snippet bookmarking — 💾/✅ toggle on <pre> elements
     =================================================================== */
  function getSnippets()       { return getJSON('shiclass_snippets', []); }
  function setSnippets(arr)    { setJSON('shiclass_snippets', arr); }

  function deleteSnippet(id) {
    setSnippets(getSnippets().filter(function (f) { return f.id !== id; }));
  }

  /** Delete saved snippets whose raw text matches, within this lesson. */
  function deleteSnippetByText(text) {
    setSnippets(getSnippets().filter(function (f) {
      return !(f.lessonId === LID && f.code === text);
    }));
  }

  function findSavedSnippet(text) {
    var list = getSnippets().filter(function (f) { return f.lessonId === LID; });
    for (var i = 0; i < list.length; i++) {
      if (list[i].code === text) return list[i].id;
    }
    return null;
  }

  /**
   * Toggle snippet bookmark.
   * If text is already saved: remove it and return null.
   * Otherwise: save with both raw text and innerHTML, return the new id.
   */
  function saveInlineSnippet(text, html) {
    var existingId = findSavedSnippet(text);
    if (existingId) {
      deleteSnippetByText(text);
      return null;
    }
    var list = getSnippets();
    list.push({
      id: 's_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6),
      lessonId: LID,
      code: text,
      html: html || text,
      language: '',
      context: '',
      timestamp: new Date().toISOString()
    });
    setSnippets(list);
    return list[list.length - 1].id;
  }

  function scanInlineSnippets() {
    var pres = document.querySelectorAll('pre');
    for (var i = 0; i < pres.length; i++) {
      (function (el) {
        if (getComputedStyle(el).position === 'static') {
          el.style.position = 'relative';
        }
        // Skip if button already added
        if (el.querySelector('.scl-inline-btn')) return;

        var text = el.textContent.trim();
        if (!text) return;

        var saved = findSavedSnippet(text);
        var btn = document.createElement('button');
        btn.className = 'scl-inline-btn' + (saved ? ' scl-saved' : '');
        btn.textContent = saved ? '\u2705' : '\uD83D\uDCBE';
        btn.setAttribute('data-scl-inline-snippet', '1');
        btn.setAttribute('data-scl-text', text);
        btn.title = saved ? '\u5df2\u6536\u85cf \u70b9\u51fb\u53d6\u6d88' : '\u6536\u85cf\u4ee3\u7801';
        el.appendChild(btn);
      })(pres[i]);
    }
  }

  /* ===================================================================
     HTML escaping helper (kept for backward compat)
     =================================================================== */
  function escHtml(str) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(str));
    return d.innerHTML;
  }

  /* ===================================================================
     Inject UI — done button only
     =================================================================== */
  function injectUI() {
    var nav = document.querySelector('.nav-links');
    if (!nav) return; // not a lesson page with nav

    var div = document.createElement('div');
    div.className = 'scl-tools';

    // ---- Done button ----
    var doneRow = document.createElement('div');
    doneRow.style.cssText = 'margin-bottom:12px;';
    doneRow.innerHTML = '<button id="scl-done-btn" class="scl-btn">\u2705 \u6807\u8bb0\u4e3a\u5df2\u5b66</button>';
    div.appendChild(doneRow);

    // Insert after the nav-links block
    nav.parentNode.insertBefore(div, nav.nextSibling);
  }

  /* ===================================================================
     Event delegation — toggle bookmark on click
     =================================================================== */
  function setupDelegation() {
    document.addEventListener('click', function (e) {
      var target = e.target;

      // Inline formula bookmark toggle
      if (target.hasAttribute('data-scl-inline-formula')) {
        var fText = target.getAttribute('data-scl-text');
        if (!fText) return;

        // Find the parent formula-box to get innerHTML
        var parentEl = target.parentElement;
        var html = parentEl ? parentEl.innerHTML : fText;

        var fId = saveInlineFormula(fText, html);
        if (fId === null) {
          // Un-saved: switch back to 📌
          target.textContent = '\uD83D\uDCCC';
          target.className = 'scl-inline-btn';
          target.title = '\u6536\u85cf\u516c\u5f0f';
        } else {
          // Saved: switch to ✅
          target.textContent = '\u2705';
          target.className = 'scl-inline-btn scl-saved';
          target.title = '\u5df2\u6536\u85cf \u70b9\u51fb\u53d6\u6d88';
        }
        return;
      }

      // Inline snippet bookmark toggle
      if (target.hasAttribute('data-scl-inline-snippet')) {
        var sText = target.getAttribute('data-scl-text');
        if (!sText) return;

        // Find the parent <pre> to get innerHTML
        var parentPre = target.parentElement;
        var shtml = parentPre ? parentPre.innerHTML : sText;

        var sId = saveInlineSnippet(sText, shtml);
        if (sId === null) {
          // Un-saved: switch back to 💾
          target.textContent = '\uD83D\uDCBE';
          target.className = 'scl-inline-btn';
          target.title = '\u6536\u85cf\u4ee3\u7801';
        } else {
          // Saved: switch to ✅
          target.textContent = '\u2705';
          target.className = 'scl-inline-btn scl-saved';
          target.title = '\u5df2\u6536\u85cf \u70b9\u51fb\u53d6\u6d88';
        }
        return;
      }

      // Backward-compat: old data-scl-del delete buttons (if any still exist)
      if (!target.hasAttribute('data-scl-del')) return;
      var kind = target.getAttribute('data-scl-del');
      var id   = target.getAttribute('data-scl-id');
      if (!kind || !id) return;
      if (kind === 'formula') deleteFormula(id);
      else if (kind === 'snippet') deleteSnippet(id);
    });
  }

  /* ===================================================================
     Init
     =================================================================== */
  function init() {
    injectUI();
    setupDelegation();
    updateDoneBtn();
    scanInlineFormulas();
    scanInlineSnippets();
    restoreScroll();

    // Wire up done button
    var doneBtn = document.getElementById('scl-done-btn');
    if (doneBtn) doneBtn.addEventListener('click', toggleDone);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
