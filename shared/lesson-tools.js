/**
 * ShiClass Lesson Tools — localStorage-driven learning features
 *
 * Features:
 *   1. Mark lesson as completed (shiclass_done + shiclass_vtally)
 *   2. Auto-save / restore scroll position (shiclass_scroll_{lessonId})
 *   3. Formula bookmarking (shiclass_formulas)
 *   4. Code snippet bookmarking (shiclass_snippets)
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
     Inline styles injected once
     =================================================================== */
  (function injectStyles() {
    if (document.getElementById('scl-style')) return;
    var css = document.createElement('style');
    css.id = 'scl-style';
    css.textContent =
      '.scl-tools{margin-top:20px;padding-top:16px;border-top:1px solid var(--border,#E8E4DC)}' +
      '.scl-btn{display:inline-flex;align-items:center;gap:4px;padding:8px 18px;border:1px solid var(--accent,#CC785C);border-radius:8px;background:var(--card-bg,#fff);color:var(--accent,#CC785C);font-size:0.9rem;cursor:pointer;transition:background 0.15s,color 0.15s;font-family:inherit;line-height:1.4}' +
      '.scl-btn:hover{background:var(--accent,#CC785C);color:#fff}' +
      '.scl-btn:disabled{opacity:0.5;cursor:default}' +
      '.scl-done,.scl-done:hover{background:#4CAF50;color:#fff;border-color:#4CAF50;opacity:1}' +
      '.scl-btn-sm{padding:5px 14px;font-size:0.83rem}' +
      '.scl-section{margin-bottom:12px}' +
      '.scl-list{margin-top:6px;display:flex;flex-direction:column;gap:6px}' +
      '.scl-bookmark-item{display:flex;align-items:flex-start;gap:8px;padding:8px 12px;background:var(--card-bg,#fff);border:1px solid var(--border,#E8E4DC);border-radius:8px;font-size:0.85rem;line-height:1.5}' +
      '.scl-bm-text{flex:1;font-family:\'JetBrains Mono\',monospace;word-break:break-all}' +
      '.scl-bm-ctx{flex-shrink:0;color:var(--text-secondary,#888);font-size:0.78rem;padding-top:2px}' +
      '.scl-bm-del{flex-shrink:0;width:22px;height:22px;display:flex;align-items:center;justify-content:center;border:none;background:transparent;color:#bbb;cursor:pointer;border-radius:4px;font-size:0.8rem;padding:0;line-height:1}' +
      '.scl-bm-del:hover{background:#fdecea;color:#d32f2f}' +
      '.scl-empty{margin:0;color:var(--text-secondary,#999);font-size:0.83rem;font-style:italic}';
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
     3. Formula bookmarking
     =================================================================== */
  function getFormulas()       { return getJSON('shiclass_formulas', []); }
  function setFormulas(arr)    { setJSON('shiclass_formulas', arr); }

  function addFormula() {
    var formula = prompt('\uD83D\uDCD0 \u8f93\u5165\u8981\u6536\u85cf\u7684\u516c\u5f0f\u5185\u5bb9\uFF08LaTeX \u6216\u6587\u5B57\uFF09\uFF1A');
    if (!formula || !formula.trim()) return;
    var ctx = prompt('\uD83D\uDCDD \u8f93\u5165\u5907\u6CE8/\u4E0A\u4E0B\u6587\uFF08\u53EF\u9009\uFF09\uFF1A');
    var list = getFormulas();
    list.push({
      id: 'f_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6),
      lessonId: LID,
      formula: formula.trim(),
      context: (ctx || '').trim(),
      timestamp: new Date().toISOString()
    });
    setFormulas(list);
    renderFormulas();
  }

  function deleteFormula(id) {
    setFormulas(getFormulas().filter(function (f) { return f.id !== id; }));
    renderFormulas();
  }

  function renderFormulas() {
    var container = document.getElementById('scl-formula-list');
    if (!container) return;
    var list = getFormulas().filter(function (f) { return f.lessonId === LID; });
    if (list.length === 0) {
      container.innerHTML = '<p class="scl-empty">\u6682\u65E0\u6536\u85CF\u516C\u5F0F</p>';
      return;
    }
    container.innerHTML = list.map(function (f) {
      return '<div class="scl-bookmark-item">' +
        '<span class="scl-bm-text">' + escHtml(f.formula) + '</span>' +
        (f.context ? '<span class="scl-bm-ctx">\u2014 ' + escHtml(f.context) + '</span>' : '') +
        '<button class="scl-bm-del" data-scl-del="formula" data-scl-id="' + f.id + '" title="\u5220\u9664">\u2715</button>' +
        '</div>';
    }).join('');
  }

  /* ===================================================================
     4. Code snippet bookmarking
     =================================================================== */
  function getSnippets()       { return getJSON('shiclass_snippets', []); }
  function setSnippets(arr)    { setJSON('shiclass_snippets', arr); }

  function addSnippet() {
    var code = prompt('\uD83D\uDCBE \u8F93\u5165\u8981\u6536\u85CF\u7684\u4EE3\u7801\u7247\u6BB5\uFF1A');
    if (!code || !code.trim()) return;
    var lang = prompt('\U0001F4DD \u8F93\u5165\u7F16\u7A0B\u8BED\u8A00\uFF08\u53EF\u9009\uFF0C\u5982 python / javascript\uFF09\uFF1A');
    var ctx = prompt('\uD83D\uDCDD \u8F93\u5165\u5907\u6CE8/\u4E0A\u4E0B\u6587\uFF08\u53EF\u9009\uFF09\uFF1A');
    var list = getSnippets();
    list.push({
      id: 's_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6),
      lessonId: LID,
      code: code.trim(),
      language: (lang || '').trim(),
      context: (ctx || '').trim(),
      timestamp: new Date().toISOString()
    });
    setSnippets(list);
    renderSnippets();
  }

  function deleteSnippet(id) {
    setSnippets(getSnippets().filter(function (f) { return f.id !== id; }));
    renderSnippets();
  }

  function renderSnippets() {
    var container = document.getElementById('scl-snippet-list');
    if (!container) return;
    var list = getSnippets().filter(function (f) { return f.lessonId === LID; });
    if (list.length === 0) {
      container.innerHTML = '<p class="scl-empty">\u6682\u65E0\u6536\u85CF\u4EE3\u7801\u7247\u6BB5</p>';
      return;
    }
    container.innerHTML = list.map(function (f) {
      return '<div class="scl-bookmark-item">' +
        '<span class="scl-bm-text">' + escHtml(f.code) + '</span>' +
        (f.language ? '<span class="scl-bm-ctx" style="padding-top:0">[' + escHtml(f.language) + ']</span>' : '') +
        (f.context ? '<span class="scl-bm-ctx">\u2014 ' + escHtml(f.context) + '</span>' : '') +
        '<button class="scl-bm-del" data-scl-del="snippet" data-scl-id="' + f.id + '" title="\u5220\u9664">\u2715</button>' +
        '</div>';
    }).join('');
  }

  /* ===================================================================
     HTML escaping helper
     =================================================================== */
  function escHtml(str) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(str));
    return d.innerHTML;
  }

  /* ===================================================================
     Inject UI into the lesson page
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

    // ---- Formula section ----
    var fSection = document.createElement('div');
    fSection.className = 'scl-section';
    fSection.innerHTML = '<button id="scl-formula-btn" class="scl-btn scl-btn-sm">\uD83D\uDCCC \u6536\u85CF\u6B64\u8BFE\u516C\u5F0F</button><div id="scl-formula-list" class="scl-list"><p class="scl-empty">\u6682\u65E0\u6536\u85CF\u516C\u5F0F</p></div>';
    div.appendChild(fSection);

    // ---- Snippet section ----
    var sSection = document.createElement('div');
    sSection.className = 'scl-section';
    sSection.innerHTML = '<button id="scl-snippet-btn" class="scl-btn scl-btn-sm">\uD83D\uDCBE \u6536\u85CF\u4EE3\u7801\u7247\u6BB5</button><div id="scl-snippet-list" class="scl-list"><p class="scl-empty">\u6682\u65E0\u6536\u85CF\u4EE3\u7801\u7247\u6BB5</p></div>';
    div.appendChild(sSection);

    // Insert after the nav-links block
    nav.parentNode.insertBefore(div, nav.nextSibling);
  }

  /* ===================================================================
     Event delegation for delete buttons
     =================================================================== */
  function setupDelegation() {
    document.addEventListener('click', function (e) {
      var target = e.target;
      if (!target || !target.hasAttribute('data-scl-del')) return;
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
    renderFormulas();
    renderSnippets();
    restoreScroll();

    // Wire up buttons (in case injected after DOMContentLoaded)
    var doneBtn = document.getElementById('scl-done-btn');
    if (doneBtn) doneBtn.addEventListener('click', toggleDone);
    var fBtn = document.getElementById('scl-formula-btn');
    if (fBtn) fBtn.addEventListener('click', addFormula);
    var sBtn = document.getElementById('scl-snippet-btn');
    if (sBtn) sBtn.addEventListener('click', addSnippet);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
