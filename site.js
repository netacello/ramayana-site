/* site.js — Ramayana Reader — bilingual EN / HE
   Pure vanilla JS, no dependencies.
   Reads from RAMAYANA_TEXT / RAMAYANA_COMMENTARY (EN, always loaded)
   and RAMAYANA_TEXT_HE / RAMAYANA_COMMENTARY_HE (HE, lazy-loaded)
*/
'use strict';

(function () {

  /* ── State ──────────────────────────────────────────── */
  var currentLang    = 'en';
  var readingMode    = 'both';
  var nightMode      = false;
  var syncScroll     = false;
  var syncLock       = false;
  var activeCantoId  = null;
  var searchVisible  = false;
  var searchIndex    = null;
  var heScriptsLoaded = false;

  /* ── UI Strings (both languages) ────────────────────── */
  var STRINGS = {
    en: {
      langBtn:          'עברית',
      searchPlaceholder:'Search text and commentary (Ctrl+F)…',
      both:             'Both',
      textOnly:         'Text only',
      commentary:       'Commentary',
      sync:             'Sync',
      night:            'Night',
      day:              'Day',
      epicSubtitle:     'An Epic of Ancient India',
      heroTitle:        'The Rámáyan of Válmíki',
      heroSub:          'Translated into English verse by Ralph T. H. Griffith, M.A. · 1870–1874',
      whatIs:           'What is the Rāmāyaṇa?',
      sevenBooks:       'The Seven Books',
      bookPrefix:       'Book',
      invocation:       'Invocation',
      navIntro:         '— Introduction',
      cantoPrefix:      'Canto',
      keyIdea:          'Key Idea',
      bookViiNote:      'Note: The Uttara Kaṇḍa (Book VII) was not included in Griffith’s translation. The following is a scholarly summary of its contents based on the Sanskrit original.',
      commPlaceholder:  'Commentary for this canto is being prepared.',
      noResults:        'No results found. Try a different search term.',
      resultsFor:       'result(s) for',
      typeText:         'text',
      typeComm:         'commentary',
      typeKey:          'key idea',
      footerCaption:    'Uttara Rāmacharit — Rāma enthroned with his family, Hanumān in eternal devotion, and Vālmīki presenting the poem to its own hero. Ravi Varma Press chromolithograph, c. 1895–1905.',
      footerHtml:       '<p><strong>Original text:</strong> <em>The Rámáyan of Válmíki</em>, translated by Ralph T.H. Griffith (1870–1874). Public domain via <a href="https://www.gutenberg.org/ebooks/24869" target="_blank" rel="noopener">Project Gutenberg #24869</a>.</p><p><strong>Commentary:</strong> Original scholarship.</p><p><strong>Illustrations:</strong> <a href="https://www.metmuseum.org/about-the-met/policies-and-documents/open-access" target="_blank" rel="noopener">The Metropolitan Museum of Art Open Access Collection</a>. Public domain (CC0).</p>',
      manuscriptCaption:'Illuminated Sanskrit manuscript page, 11th–13th century. The decorative tradition of illustrated Ramayana manuscripts spans over a thousand years.',
      heroAlt:          'Embroidered textile depicting scenes from the Ramayana',
      vishnuCaps: [
        'Vishnu (Nārāyaṇa) reclining on Shesha, the cosmic serpent.',
        'Shesha Nārāyaṇa on a cobra canopy.',
        'Vishnu with Hanumān, bridging the cosmic and narrative worlds of the epic.'
      ],
      valmikiCaption:   'Vālmīki, the Adi-Kavi (“first poet”), composing the Rāmāyaṇa. Indian miniature, 19th century.',
      loadingHe:        '',
    },
    he: {
      langBtn:          'English',
      searchPlaceholder:'חיפוש בטקסט ובפרשנות (Ctrl+F)…',
      both:             'שנייהם',
      textOnly:         'טקסט בלבד',
      commentary:       'פרשנות',
      sync:             'סנכרון',
      night:            'לילה',
      day:              'יום',
      epicSubtitle:     'אפוס מהודו העתיקה',
      heroTitle:        'הרמאיאן של ואלמיקי',
      heroSub:          'תרגום מאנגלית על ידי ראלף ט׳ה. גריפית׳ · 1870–1874',
      whatIs:           'מהו הרמאיאנה?',
      sevenBooks:       'שבעת הספרים',
      bookPrefix:       'ספר',
      invocation:       'הקדשה',
      navIntro:         '— מבוא',
      cantoPrefix:      'פרק',
      keyIdea:          'רעיון מפתח',
      bookViiNote:      'הערה: האוטרה קאנדה (ספר ז׳) לא נכלל בתרגום גריפית׳. להלן סיכום מלומדי של תוכנו על בסיס המקור הסנסקריטי.',
      commPlaceholder:  'הפרשנות לפרק זה בהכנה.',
      noResults:        'לא נמצאו תוצאות. נסה מונח חיפוש אחר.',
      resultsFor:       'תוצאות עבור',
      typeText:         'טקסט',
      typeComm:         'פרשנות',
      typeKey:          'רעיון מפתח',
      footerCaption:    'אוטרה ראמאצ׳ריט — ראמה על כיסאו עם משפחתו, האנומאן בדבקות נצחית, וואלמיקי מגיש את השיר לגיבורו. כרומוליתוגרפיה של בית הדפוס ראווי וארמה, כ-1895–1905.',
      footerHtml:       '<p><strong>טקסט מקורי:</strong> <em>הרמאיאן של ואלמיקי</em>, תרגום ראלף ט׳ה. גריפית׳ (1870–1874). נחלת הכלל.</p><p><strong>פרשנות:</strong> מחקר מקורי.</p><p><strong>איורים:</strong> <a href="https://www.metmuseum.org/about-the-met/policies-and-documents/open-access" target="_blank" rel="noopener">אוסף הנחלה הציבורית של מוזיאון המטרופוליטן לאמנות</a>. נחלת הכלל (CC0).</p>',
      manuscriptCaption:'דף כתב יד סנסקריטי מואר מהמאה ה-11 עד ה-13. מסורת כתבי היד המאוירים של הרמאיאנה מתפרשת על פני אלף שנים.',
      heroAlt:          'טקסטיל רקום המתאר סצנות מהרמאיאנה',
      vishnuCaps: [
        'וישנו (נאראיאנה) שוכב על ששה, הנחש הקוסמי.',
        'ששה נאראיאנה על מצע הקוברא.',
        'וישנו עם האנומאן, המגשר בין העולמות הקוסמיים לעלילות האפוס.'
      ],
      valmikiCaption:   'ואלמיקי, האדי-קאוי ("המשורר הראשון"), מחבר את הרמאיאנה. מיניאטורה הודית, המאה ה-19.',
      loadingHe:        'התרגום העברי נטען…',
    }
  };

  /* ── Language helpers ───────────────────────────────── */
  function s(key) { return STRINGS[currentLang][key] || STRINGS.en[key] || ''; }

  function getText() {
    if (currentLang === 'he' && typeof RAMAYANA_TEXT_HE !== 'undefined' && RAMAYANA_TEXT_HE.length) {
      return RAMAYANA_TEXT_HE;
    }
    return RAMAYANA_TEXT;
  }

  function getComm() {
    if (currentLang === 'he' && typeof RAMAYANA_COMMENTARY_HE !== 'undefined') {
      return RAMAYANA_COMMENTARY_HE;
    }
    return RAMAYANA_COMMENTARY;
  }

  /* ── Boot ───────────────────────────────────────────── */
  function initializeApp() {
    renderAll();
    buildSidebar();
    initControls();
    initSearch();
    initProgressBar();
    initKeyboard();
    initIntersectionObserver();
    var loading = document.getElementById('loading');
    if (loading) loading.remove();
    updateLangUI();
  }

  document.addEventListener('DOMContentLoaded', function () {
    loadPreferences();
    // Load Hebrew scripts immediately if user prefers Hebrew
    if (currentLang === 'he') {
      loadHeScripts(initializeApp);
    } else {
      initializeApp();
    }
  });

  /* ── Preferences ────────────────────────────────────── */
  function loadPreferences() {
    readingMode  = localStorage.getItem('ram-mode')  || 'both';
    nightMode    = localStorage.getItem('ram-night') === '1';
    syncScroll   = localStorage.getItem('ram-sync')  === '1';
    currentLang  = localStorage.getItem('ram-lang')  || 'en';
    applyMode(readingMode, false);
    if (nightMode)  applyNightMode(true, false);
    if (syncScroll) { var sc = document.getElementById('sync-scroll'); if (sc) sc.checked = true; }
    applyLangDOM(currentLang);
  }

  function applyMode(mode, save) {
    readingMode = mode;
    document.body.classList.remove('mode-both', 'mode-text', 'mode-commentary');
    document.body.classList.add('mode-' + mode);
    ['both', 'text', 'commentary'].forEach(function (m) {
      var btn = document.getElementById('mode-' + m);
      if (btn) btn.classList.toggle('active', m === mode);
    });
    if (save !== false) localStorage.setItem('ram-mode', mode);
  }

  function applyNightMode(on, save) {
    nightMode = !!on;
    document.body.classList.toggle('night-mode', nightMode);
    var btn = document.getElementById('night-mode-btn');
    if (btn) btn.textContent = nightMode ? s('day') : s('night');
    if (save !== false) localStorage.setItem('ram-night', nightMode ? '1' : '0');
  }

  /* ── Language switching ─────────────────────────────── */
  function applyLangDOM(lang) {
    var html = document.documentElement;
    if (lang === 'he') {
      html.setAttribute('lang', 'he');
      html.setAttribute('dir', 'rtl');
      document.body.classList.add('rtl');
    } else {
      html.setAttribute('lang', 'en');
      html.removeAttribute('dir');
      document.body.classList.remove('rtl');
    }
  }

  function updateLangUI() {
    var btn = document.getElementById('lang-btn');
    if (btn) btn.textContent = s('langBtn');

    var inp = document.getElementById('search-input');
    if (inp) inp.placeholder = s('searchPlaceholder');

    var mBoth = document.getElementById('mode-both');
    var mText = document.getElementById('mode-text');
    var mComm = document.getElementById('mode-commentary');
    if (mBoth) mBoth.textContent = s('both');
    if (mText) mText.textContent = s('textOnly');
    if (mComm) mComm.textContent = s('commentary');

    var syncLabel = document.querySelector('.sync-label-text');
    if (syncLabel) syncLabel.textContent = s('sync');

    var nightBtn = document.getElementById('night-mode-btn');
    if (nightBtn) nightBtn.textContent = nightMode ? s('day') : s('night');
  }

  function switchLanguage(lang) {
    if (lang === currentLang) return;
    if (lang === 'he') {
      loadHeScripts(function () {
        currentLang = 'he';
        localStorage.setItem('ram-lang', 'he');
        searchIndex = null;
        applyLangDOM('he');
        updateLangUI();
        renderAll();
        buildSidebar();
        initIntersectionObserver();
      });
    } else {
      currentLang = 'en';
      localStorage.setItem('ram-lang', 'en');
      searchIndex = null;
      applyLangDOM('en');
      updateLangUI();
      renderAll();
      buildSidebar();
      initIntersectionObserver();
    }
  }

  function loadHeScripts(callback) {
    if (heScriptsLoaded) { callback(); return; }
    var textReady = false, commReady = false;
    function check() { if (textReady && commReady) { heScriptsLoaded = true; callback(); } }

    function injectScript(src, onload) {
      if (document.querySelector('script[src="' + src + '"]')) { onload(); return; }
      var s = document.createElement('script');
      s.src  = src;
      s.onload  = onload;
      s.onerror = onload; /* still proceed even if file missing */
      document.head.appendChild(s);
    }

    injectScript('data/text_he.js',        function () { textReady = true;  check(); });
    injectScript('data/commentary_he.js',  function () { commReady = true;  check(); });
  }

  /* ── Main render ─────────────────────────────────────── */
  function renderAll() {
    var mainEl = document.getElementById('main');
    /* Remove old click listener by replacing with clone */
    var newMain = mainEl.cloneNode(false);
    mainEl.parentNode.replaceChild(newMain, mainEl);
    newMain.innerHTML = '';

    newMain.appendChild(buildIntroSection());
    getText().forEach(function (book) {
      newMain.appendChild(buildBookSection(book));
    });
    newMain.appendChild(buildFooter());
    newMain.addEventListener('click', onMainClick);

    /* Reattach scroll sync listener */
    newMain.addEventListener('scroll', onScrollSync, true);
  }

  /* ── Introduction section ────────────────────────────── */
  function buildIntroSection() {
    var section = mkEl('section', { id: 'section-intro', className: 'book-section' });

    /* Hero */
    var hero    = mkEl('div', { className: 'intro-hero' });
    var heroImg = mkEl('img');
    heroImg.src       = 'images/cover_narrative_textile.jpg';
    heroImg.alt       = s('heroAlt');
    heroImg.className = 'intro-hero-img';
    heroImg.loading   = 'lazy';
    imgFallback(heroImg, '#1a0e08, #2a1f10');

    var heroGrad = mkEl('div', { className: 'intro-hero-gradient' });
    var heroText = mkEl('div', { className: 'intro-hero-text' });
    heroText.innerHTML =
      '<div class="hero-eyebrow">' + escHtml(s('epicSubtitle')) + '</div>' +
      '<h1>' + escHtml(s('heroTitle')) + '</h1>' +
      '<p class="intro-hero-sub">' + escHtml(s('heroSub')) + '</p>';

    hero.appendChild(heroImg);
    hero.appendChild(heroGrad);
    hero.appendChild(heroText);
    section.appendChild(hero);

    /* Inner content */
    var content = mkEl('div', { className: 'intro-content' });

    /* Manuscript page */
    content.appendChild(buildFigure(
      'images/intro_manuscript_page.jpg',
      s('manuscriptCaption'),
      'inline-image'
    ));

    /* What is the Ramayana? */
    var introComm = getComm() && getComm().intro;
    if (introComm && introComm.text) {
      var introDiv = mkEl('div', { className: 'book-intro' });
      introDiv.innerHTML =
        '<h2 class="section-heading">' + escHtml(s('whatIs')) + '</h2>' +
        textToHtml(introComm.text.substring(0, 5000));
      content.appendChild(introDiv);
    }

    /* Three Vishnu images */
    var vishnuSrcs = [
      'images/intro_vishnu_shesha.jpg',
      'images/intro_vishnu_narayana.jpg',
      'images/intro_vishnu_hanuman.jpg'
    ];
    var vishnuCaps = s('vishnuCaps');
    var vishnuRow  = mkEl('div', { className: 'vishnu-images' });
    vishnuSrcs.forEach(function (src, i) {
      var fig = mkEl('figure', { className: 'vishnu-img-wrap' });
      var img = mkEl('img');
      img.src     = src;
      img.alt     = vishnuCaps[i];
      img.loading = 'lazy';
      imgFallback(img, '#1a2340, #2a3850');
      var cap = mkEl('figcaption');
      cap.textContent = vishnuCaps[i];
      fig.appendChild(img);
      fig.appendChild(cap);
      vishnuRow.appendChild(fig);
    });
    content.appendChild(vishnuRow);

    /* Valmiki image */
    var valWrap = mkEl('div', { className: 'book-intro' });
    valWrap.innerHTML =
      '<div style="display:flex;gap:2rem;align-items:flex-start;flex-wrap:wrap;">' +
      '<figure style="flex:0 0 220px;margin:0;">' +
      '<img src="images/intro_valmiki_writing.jpg" alt="' + escHtml(s('valmikiCaption')) + '" loading="lazy" style="width:220px;border-radius:4px;box-shadow:0 4px 16px rgba(0,0,0,.12);">' +
      '<figcaption style="font-family:\'Inter\',sans-serif;font-size:.78rem;color:#777;font-style:italic;margin-top:.4rem;">' +
      escHtml(s('valmikiCaption')) + '</figcaption></figure></div>';
    content.appendChild(valWrap);

    /* TOC */
    var tocHead = mkEl('h2', { className: 'section-heading' });
    tocHead.style.cssText = "font-family:'Cormorant Garamond',serif;color:var(--accent);font-size:2rem;margin:2rem 44px 1rem;";
    tocHead.textContent = s('sevenBooks');
    content.appendChild(tocHead);

    var tocGrid = mkEl('div', { className: 'toc-grid' });
    getText().forEach(function (book) {
      var card = mkEl('a');
      card.href      = '#section-book-' + book.number;
      card.className = 'toc-card';
      card.addEventListener('click', function (e) {
        e.preventDefault();
        var target = document.getElementById('section-book-' + book.number);
        if (target) target.scrollIntoView({ behavior: 'smooth' });
      });

      var cimg = mkEl('img');
      cimg.src       = 'images/' + book.headerImage;
      cimg.alt       = book.title;
      cimg.className = 'toc-card-img';
      cimg.loading   = 'lazy';
      imgFallback(cimg, '#1A2340, #2a3850');

      var cgrad  = mkEl('div', { className: 'toc-card-gradient' });
      var ctext  = mkEl('div', { className: 'toc-card-text' });
      ctext.innerHTML =
        '<div class="toc-card-eyebrow">' + escHtml(s('bookPrefix') + ' ' + book.number) + '</div>' +
        '<p class="toc-card-title">' + escHtml(book.title) + '</p>' +
        '<p class="toc-card-subtitle">' + escHtml(book.subtitle) + '</p>';

      card.appendChild(cimg);
      card.appendChild(cgrad);
      card.appendChild(ctext);
      tocGrid.appendChild(card);
    });
    content.appendChild(tocGrid);
    section.appendChild(content);
    return section;
  }

  /* ── Book section ────────────────────────────────────── */
  function buildBookSection(book) {
    var section = mkEl('section', {
      id:        'section-book-' + book.number,
      className: 'book-section'
    });

    /* Header banner */
    var header = mkEl('div', { className: 'book-header' });
    var bImg   = mkEl('img');
    bImg.src       = 'images/' + book.headerImage;
    bImg.alt       = book.title + ' — book header illustration';
    bImg.className = 'book-header-img';
    bImg.loading   = 'lazy';
    imgFallback(bImg, '#1A2340, #2a3850');

    var bGrad = mkEl('div', { className: 'book-header-gradient' });
    var bText = mkEl('div', { className: 'book-header-text' });
    bText.innerHTML =
      '<div class="book-number">' + escHtml(s('bookPrefix') + ' ' + book.number) + '</div>' +
      '<h2>' + escHtml(book.title) + '</h2>' +
      '<p class="book-subtitle">' + escHtml(book.subtitle) + '</p>';

    header.appendChild(bImg);
    header.appendChild(bGrad);
    header.appendChild(bText);
    section.appendChild(header);

    /* Book intro */
    var bookComm = getComm() && getComm().books ? getComm().books[book.number] : null;
    if (bookComm && bookComm.intro) {
      var introDiv = mkEl('div', { className: 'book-intro' });
      introDiv.innerHTML = textToHtml(bookComm.intro);
      section.appendChild(introDiv);
    }

    /* Book VII special note */
    if (book.number === 'VII') {
      var note = mkEl('div', { className: 'book-vii-note' });
      note.innerHTML = '<strong>' + (currentLang === 'he' ? 'הערה:' : 'Note:') + '</strong> ' +
        escHtml(s('bookViiNote').replace(/^(Note|הערה): /, ''));
      section.appendChild(note);
    }

    /* Cantos */
    var cantosContainer = mkEl('div', { className: 'cantos-container' });

    if (book.cantos.length === 0) {
      var summaryDiv = mkEl('div', { className: 'book-intro' });
      if (bookComm && bookComm.cantoMap) {
        Object.keys(bookComm.cantoMap).forEach(function (k) {
          var entry = bookComm.cantoMap[k];
          if (entry && entry.text) {
            summaryDiv.innerHTML += textToHtml(entry.text);
            if (entry.keyIdea) {
              summaryDiv.innerHTML +=
                '<div class="key-idea"><span class="key-idea-label">' + escHtml(s('keyIdea')) + '</span>' +
                escHtml(entry.keyIdea) + '</div>';
            }
          }
        });
      }
      cantosContainer.appendChild(summaryDiv);
    } else {
      book.cantos.forEach(function (canto) {
        cantosContainer.appendChild(buildCantoSection(book, canto, bookComm));
      });
    }

    section.appendChild(cantosContainer);
    return section;
  }

  /* ── Canto section ───────────────────────────────────── */
  function buildCantoSection(book, canto, bookComm) {
    var cantoId = 'canto-' + book.number + '-' + canto.number;
    var div = mkEl('div', { id: cantoId, className: 'canto' });
    div.dataset.book  = book.number;
    div.dataset.canto = canto.number;

    /* Header */
    var chdr = mkEl('div', { className: 'canto-header' });
    var titleText = canto.number === 'Invocation'
      ? s('invocation')
      : s('cantoPrefix') + ' ' + canto.number + (canto.title ? '. ' + canto.title : '');
    chdr.innerHTML =
      '<h3 class="canto-title-text">' + escHtml(titleText) + '</h3>' +
      '<hr class="canto-divider">';
    div.appendChild(chdr);

    /* Inline image */
    if (canto.inlineImage) {
      var imgWrap = mkEl('div', { className: 'canto-header' });
      imgWrap.appendChild(buildFigure(
        canto.inlineImage.src,
        canto.inlineImage.caption,
        'inline-image'
      ));
      div.appendChild(imgWrap);
    }

    /* Two-column reader */
    var cols    = mkEl('div', { className: 'reader-columns' });
    var textCol = mkEl('div', { className: 'text-column' });
    var commCol = mkEl('div', { className: 'commentary-column' });

    /* Verse paragraphs */
    canto.paragraphs.forEach(function (para, idx) {
      var p = mkEl('p', { className: 'verse-para' });
      p.dataset.cantoId = cantoId;
      p.dataset.idx     = String(idx);
      p.textContent     = para;
      textCol.appendChild(p);
    });

    /* Commentary */
    var comm = bookComm && bookComm.cantoMap ? bookComm.cantoMap[canto.number] : null;
    if (comm && comm.text) {
      var commDiv = mkEl('div', { className: 'commentary-text' });
      commDiv.innerHTML = textToHtml(comm.text);
      commCol.appendChild(commDiv);
      if (comm.keyIdea) {
        var ki = mkEl('div', { className: 'key-idea' });
        ki.innerHTML = '<span class="key-idea-label">' + escHtml(s('keyIdea')) + '</span>' + escHtml(comm.keyIdea);
        commCol.appendChild(ki);
      }
    } else {
      var ph = mkEl('p', { className: 'commentary-placeholder' });
      ph.textContent = s('commPlaceholder');
      commCol.appendChild(ph);
    }

    cols.appendChild(textCol);
    cols.appendChild(commCol);
    div.appendChild(cols);
    return div;
  }

  function buildFigure(src, caption, className) {
    var fig = mkEl('figure', { className: className || 'inline-image' });
    var img = mkEl('img');
    img.src     = src;
    img.alt     = caption || '';
    img.loading = 'lazy';
    imgFallback(img, '#2a1f10, #1a2340');
    var cap = mkEl('figcaption');
    cap.textContent = caption || '';
    fig.appendChild(img);
    fig.appendChild(cap);
    return fig;
  }

  /* ── Sidebar ─────────────────────────────────────────── */
  function buildSidebar() {
    var tree = document.getElementById('nav-tree');
    tree.innerHTML = '';

    /* Introduction link */
    var introDiv = mkEl('div', { className: 'nav-intro' });
    var introLink = mkEl('a');
    introLink.href = '#section-intro';
    introLink.className = 'nav-intro-link';
    introLink.id = 'nav-intro';
    introLink.setAttribute('role', 'treeitem');
    introLink.textContent = s('whatIs');
    introLink.addEventListener('click', function (e) {
      e.preventDefault();
      closeSidebarMobile();
      var t = document.getElementById('section-intro');
      if (t) t.scrollIntoView({ behavior: 'smooth' });
    });
    introDiv.appendChild(introLink);
    tree.appendChild(introDiv);

    getText().forEach(function (book) {
      var bookDiv = mkEl('div', {
        id:        'nav-book-' + book.number,
        className: 'nav-book'
      });

      var hdr = mkEl('div', { className: 'nav-book-header', tabIndex: 0 });
      hdr.setAttribute('role', 'treeitem');
      hdr.setAttribute('aria-expanded', 'true');
      hdr.innerHTML =
        '<span class="book-title-nav">' +
        escHtml(s('bookPrefix') + ' ' + book.number + ': ' + book.title) +
        '</span>' +
        '<span class="expand-icon" aria-hidden="true">&#9660;</span>';
      hdr.addEventListener('click', function () { toggleBook(bookDiv, hdr); });
      hdr.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleBook(bookDiv, hdr); }
      });
      bookDiv.appendChild(hdr);

      var cantosDiv = mkEl('div', { className: 'nav-cantos' });
      cantosDiv.setAttribute('role', 'group');

      var introLink = mkEl('a');
      introLink.href      = '#section-book-' + book.number;
      introLink.className = 'nav-canto';
      introLink.style.cssText = 'font-style:italic;opacity:.6;';
      introLink.textContent   = s('navIntro');
      introLink.addEventListener('click', function (e) {
        e.preventDefault();
        closeSidebarMobile();
        var t = document.getElementById('section-book-' + book.number);
        if (t) t.scrollIntoView({ behavior: 'smooth' });
      });
      cantosDiv.appendChild(introLink);

      book.cantos.forEach(function (canto) {
        var a = mkEl('a');
        a.href      = '#canto-' + book.number + '-' + canto.number;
        a.id        = 'nav-canto-' + book.number + '-' + canto.number;
        a.className = 'nav-canto';
        a.setAttribute('role', 'treeitem');
        a.textContent = canto.number === 'Invocation'
          ? s('invocation')
          : canto.number + '. ' + canto.title;
        a.addEventListener('click', function (e) {
          e.preventDefault();
          closeSidebarMobile();
          scrollToCanto('canto-' + book.number + '-' + canto.number);
        });
        cantosDiv.appendChild(a);
      });

      bookDiv.appendChild(cantosDiv);
      tree.appendChild(bookDiv);
    });
  }

  function toggleBook(bookDiv, hdr) {
    var collapsed = bookDiv.classList.toggle('collapsed');
    hdr.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
  }

  function scrollToCanto(id) {
    var target = document.getElementById(id);
    if (!target) return;
    var top = target.getBoundingClientRect().top + window.pageYOffset - 60 - 8;
    window.scrollTo({ top: top, behavior: 'smooth' });
  }

  function closeSidebarMobile() {
    if (window.innerWidth <= 768) {
      document.getElementById('sidebar').classList.remove('open');
    }
  }

  /* ── Controls ────────────────────────────────────────── */
  function initControls() {
    ['both', 'text', 'commentary'].forEach(function (mode) {
      var btn = document.getElementById('mode-' + mode);
      if (btn) btn.addEventListener('click', function () { applyMode(mode); });
    });

    var nightBtn = document.getElementById('night-mode-btn');
    if (nightBtn) {
      nightBtn.textContent = nightMode ? s('day') : s('night');
      nightBtn.addEventListener('click', function () { applyNightMode(!nightMode); });
    }

    var syncChk = document.getElementById('sync-scroll');
    if (syncChk) {
      syncChk.checked = syncScroll;
      syncChk.addEventListener('change', function () {
        syncScroll = syncChk.checked;
        localStorage.setItem('ram-sync', syncScroll ? '1' : '0');
      });
    }

    var langBtn = document.getElementById('lang-btn');
    if (langBtn) {
      langBtn.addEventListener('click', function () {
        switchLanguage(currentLang === 'en' ? 'he' : 'en');
      });
    }

    var toggleBtn = document.getElementById('sidebar-toggle-btn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function () {
        document.getElementById('sidebar').classList.toggle('open');
      });
    }

    document.getElementById('app').addEventListener('click', function (e) {
      if (window.innerWidth > 768) return;
      if (!e.target.closest('#sidebar') && !e.target.closest('#sidebar-toggle-btn')) {
        closeSidebarMobile();
      }
    });
  }

  /* ── Scroll sync ─────────────────────────────────────── */
  function onScrollSync(e) {
    if (!syncScroll || syncLock) return;
    var src = e.target;
    if (!src.classList.contains('text-column') && !src.classList.contains('commentary-column')) return;
    var container = src.closest('.reader-columns');
    if (!container) return;
    var dst = src.classList.contains('text-column')
      ? container.querySelector('.commentary-column')
      : container.querySelector('.text-column');
    if (!dst) return;
    syncLock = true;
    var ratio = src.scrollTop / Math.max(1, src.scrollHeight - src.clientHeight);
    dst.scrollTop = ratio * (dst.scrollHeight - dst.clientHeight);
    requestAnimationFrame(function () { syncLock = false; });
  }

  /* ── Click-to-highlight ──────────────────────────────── */
  function onMainClick(e) {
    var para = e.target.closest('.verse-para');
    if (!para) return;
    var wasHighlighted = para.classList.contains('highlighted');
    document.querySelectorAll('.verse-para.highlighted').forEach(function (p) {
      p.classList.remove('highlighted');
    });
    if (!wasHighlighted) {
      para.classList.add('highlighted');
      var cantoEl = para.closest('.canto');
      if (cantoEl) {
        var commCol = cantoEl.querySelector('.commentary-column');
        if (commCol) commCol.scrollTop = 0;
      }
    }
  }

  /* ── Progress bar ────────────────────────────────────── */
  function initProgressBar() {
    var bar = document.getElementById('progress-bar');
    if (!bar) return;
    window.addEventListener('scroll', function () {
      var scrolled = window.pageYOffset;
      var total    = document.body.scrollHeight - window.innerHeight;
      var pct      = total > 0 ? scrolled / total : 0;
      bar.style.transform = 'scaleX(' + pct + ')';
      bar.setAttribute('aria-valuenow', Math.round(pct * 100));
    }, { passive: true });
  }

  /* ── IntersectionObserver ───────────────────────────── */
  function initIntersectionObserver() {
    if (!('IntersectionObserver' in window)) return;
    if (window._ramObserver) window._ramObserver.disconnect();
    window._ramObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) updateActiveNav(entry.target.id);
      });
    }, { rootMargin: '-10% 0px -70% 0px' });
    var introEl = document.getElementById('section-intro');
    if (introEl) window._ramObserver.observe(introEl);
    document.querySelectorAll('.canto').forEach(function (el) {
      window._ramObserver.observe(el);
    });
  }

  function updateActiveNav(cantoId) {
    if (cantoId === activeCantoId) return;
    activeCantoId = cantoId;
    document.querySelectorAll('.nav-canto.active, .nav-intro-link.active').forEach(function (a) {
      a.classList.remove('active');
    });
    if (cantoId === 'section-intro') {
      var introLink = document.getElementById('nav-intro');
      if (introLink) {
        introLink.classList.add('active');
        introLink.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    } else {
      var navLink = document.getElementById('nav-' + cantoId);
      if (navLink) {
        navLink.classList.add('active');
        navLink.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    }
  }

  /* ── Search ──────────────────────────────────────────── */
  function buildSearchIndex() {
    if (searchIndex) return;
    searchIndex = [];
    getText().forEach(function (book) {
      book.cantos.forEach(function (canto) {
        var id       = 'canto-' + book.number + '-' + canto.number;
        var location = s('bookPrefix') + ' ' + book.number + ' — ' + book.title +
                       ', ' + s('cantoPrefix') + ' ' + canto.number +
                       (canto.title ? ': ' + canto.title : '');

        canto.paragraphs.forEach(function (para) {
          searchIndex.push({ id: id, location: location, text: para, type: s('typeText') });
        });

        var bookComm = getComm() && getComm().books ? getComm().books[book.number] : null;
        if (bookComm && bookComm.cantoMap) {
          var comm = bookComm.cantoMap[canto.number];
          if (comm) {
            if (comm.text)    searchIndex.push({ id: id, location: location, text: comm.text,    type: s('typeComm') });
            if (comm.keyIdea) searchIndex.push({ id: id, location: location, text: comm.keyIdea, type: s('typeKey')  });
          }
        }
      });
    });
  }

  function initSearch() {
    var input = document.getElementById('search-input');
    var btn   = document.getElementById('search-btn');
    var panel = document.getElementById('search-results');

    function doSearch() {
      var q = input.value.trim();
      if (!q) { hideSearch(); return; }
      buildSearchIndex();
      var results = performSearch(q);
      showResults(q, results);
    }

    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') doSearch();
      if (e.key === 'Escape') hideSearch();
    });
    btn.addEventListener('click', doSearch);

    panel.addEventListener('click', function (e) {
      var item = e.target.closest('.search-result-item');
      if (item) { hideSearch(); scrollToCanto(item.dataset.id); return; }
      if (e.target === panel) hideSearch();
    });
  }

  function performSearch(query) {
    var q       = query.toLowerCase();
    var seen    = {};
    var results = [];
    for (var i = 0; i < searchIndex.length; i++) {
      if (results.length >= 80) break;
      var entry = searchIndex[i];
      var text  = entry.text.toLowerCase();
      var pos   = text.indexOf(q);
      if (pos === -1) continue;
      var key = entry.id + ':' + entry.type;
      if (seen[key]) continue;
      seen[key] = true;
      var start   = Math.max(0, pos - 60);
      var end     = Math.min(entry.text.length, pos + q.length + 100);
      var snippet = (start > 0 ? '…' : '') + entry.text.slice(start, end) +
                    (end < entry.text.length ? '…' : '');
      results.push({ id: entry.id, location: entry.location, snippet: snippet,
                     type: entry.type });
    }
    return results;
  }

  function showResults(query, results) {
    var panel = document.getElementById('search-results');
    panel.innerHTML = '';

    var box   = mkEl('div', { className: 'search-results-panel' });
    var hdiv  = mkEl('div', { className: 'search-results-header' });
    var close = mkEl('button');
    close.innerHTML = '&#10005;';
    close.style.cssText = 'background:none;border:none;cursor:pointer;font-size:1.2rem;line-height:1;color:inherit;';
    close.setAttribute('aria-label', 'Close search results');
    close.addEventListener('click', hideSearch);

    hdiv.innerHTML = '<span>' + results.length + ' ' + escHtml(s('resultsFor')) +
                     ' “' + escHtml(query) + '”</span>';
    hdiv.appendChild(close);
    box.appendChild(hdiv);

    if (results.length === 0) {
      var none = mkEl('p');
      none.style.cssText = 'padding:1.5rem;color:#888;';
      none.textContent = s('noResults');
      box.appendChild(none);
    } else {
      var list = mkEl('div');
      list.setAttribute('role', 'list');
      results.forEach(function (r) {
        var item = mkEl('div', { className: 'search-result-item' });
        item.dataset.id = r.id;
        item.setAttribute('tabindex', '0');
        item.setAttribute('role', 'listitem');

        var loc = mkEl('div', { className: 'search-result-location' });
        loc.textContent = r.location + ' · ' + r.type;

        var snip = mkEl('div', { className: 'search-result-snippet' });
        snip.innerHTML = highlightQuery(escHtml(r.snippet), escHtml(query));

        item.appendChild(loc);
        item.appendChild(snip);
        item.addEventListener('keydown', function (e) {
          if (e.key === 'Enter') { hideSearch(); scrollToCanto(r.id); }
        });
        list.appendChild(item);
      });
      box.appendChild(list);
    }

    panel.appendChild(box);
    panel.classList.add('visible');
    panel.setAttribute('aria-hidden', 'false');
    searchVisible = true;
  }

  function highlightQuery(html, query) {
    var safe = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return html.replace(new RegExp('(' + safe + ')', 'gi'),
      '<mark class="search-highlight">$1</mark>');
  }

  function hideSearch() {
    var panel = document.getElementById('search-results');
    panel.classList.remove('visible');
    panel.setAttribute('aria-hidden', 'true');
    searchVisible = false;
  }

  /* ── Keyboard shortcuts ──────────────────────────────── */
  function initKeyboard() {
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        var inp = document.getElementById('search-input');
        inp.focus();
        inp.select();
      }
      if (e.key === 'Escape' && searchVisible) hideSearch();
    });
  }

  /* ── Footer ──────────────────────────────────────────── */
  function buildFooter() {
    var wrapper = mkEl('div');

    var closing = mkEl('div', { className: 'closing-image' });
    var cImg    = mkEl('img');
    cImg.src     = 'images/book7_rama_court_ravi_varma.jpg';
    cImg.alt     = 'Rama enthroned — Ravi Varma Press chromolithograph';
    cImg.loading = 'lazy';
    imgFallback(cImg, '#1a2340, #2a3850');
    closing.appendChild(cImg);

    var capBar = mkEl('div');
    capBar.style.cssText = "background:var(--nav-bg);color:rgba(237,232,208,.7);font-family:'Inter',sans-serif;font-size:.78rem;padding:.5rem 1.5rem;font-style:italic;";
    capBar.textContent = s('footerCaption');
    closing.appendChild(capBar);
    wrapper.appendChild(closing);

    var footer = mkEl('footer', { className: 'site-footer' });
    footer.innerHTML = s('footerHtml');
    wrapper.appendChild(footer);
    return wrapper;
  }

  /* ── Utility helpers ─────────────────────────────────── */
  function mkEl(tag, props) {
    var e = document.createElement(tag);
    if (props) Object.keys(props).forEach(function (k) { e[k] = props[k]; });
    return e;
  }

  function escHtml(s) {
    return String(s || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function textToHtml(text) {
    if (!text) return '';
    var html = '';
    var parts = text.split(/\n\n+/);

    for (var i = 0; i < parts.length; i++) {
      var para = parts[i].trim();
      if (!para) continue;

      if (isMarkdownTable(para)) {
        html += markdownTableToHtml(para);
      } else {
        html += '<p>' + escHtml(para).replace(/\n/g, '<br>') + '</p>';
      }
    }
    return html;
  }

  function isMarkdownTable(text) {
    var lines = text.split('\n');
    if (lines.length < 3) return false;
    var separatorLine = lines[1].trim();
    return /^\|[\s\-|:]+\|$/.test(separatorLine);
  }

  function markdownTableToHtml(text) {
    var lines = text.split('\n').map(function (l) { return l.trim(); });
    var rows = [];
    for (var i = 0; i < lines.length; i++) {
      if (/^\|[\s\-|:]+\|$/.test(lines[i])) continue;
      if (!lines[i] || !lines[i].startsWith('|')) continue;
      rows.push(lines[i].split('|').slice(1, -1).map(function (c) { return c.trim(); }));
    }
    if (rows.length < 2) return '<p>' + escHtml(text) + '</p>';

    var numCols = rows[0].length;
    var html = '<div class="kandas-grid" style="grid-template-columns:repeat(' + numCols + ',1fr);">';
    rows[0].forEach(function (cell) {
      html += '<div class="kandas-grid-cell kandas-header">' + escHtml(cell) + '</div>';
    });

    for (var r = 1; r < rows.length; r++) {
      rows[r].forEach(function (cell) {
        html += '<div class="kandas-grid-cell">' + escHtml(cell) + '</div>';
      });
    }
    html += '</div>';
    return html;
  }

  function imgFallback(img, gradient) {
    img.addEventListener('error', function () {
      img.style.display = 'none';
      if (img.parentElement) {
        img.parentElement.style.background = 'linear-gradient(135deg, ' + gradient + ')';
      }
    }, { once: true });
  }

})();
