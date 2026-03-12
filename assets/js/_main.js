/* ==========================================================================
   jQuery plugin settings and other scripts
   ========================================================================== */

$(document).ready(function() {
  // FitVids init
  $("#main").fitVids();

  // Sticky sidebar
  var stickySideBar = function() {
    var show =
      $(".author__urls-wrapper button").length === 0
        ? $(window).width() > 1024 // width should match $large Sass variable
        : !$(".author__urls-wrapper button").is(":visible");
    if (show) {
      // fix
      $(".sidebar").addClass("sticky");
    } else {
      // unfix
      $(".sidebar").removeClass("sticky");
    }
  };

  stickySideBar();

  $(window).resize(function() {
    stickySideBar();
  });

  // Follow menu drop down
  $(".author__urls-wrapper button").on("click", function() {
    $(".author__urls").toggleClass("is--visible");
    $(".author__urls-wrapper button").toggleClass("open");
  });

  // Close search screen with Esc key
  $(document).keyup(function(e) {
    if (e.keyCode === 27) {
      if ($(".initial-content").hasClass("is--hidden")) {
        $(".search-content").toggleClass("is--visible");
        $(".initial-content").toggleClass("is--hidden");
      }
    }
  });

  // Search toggle
  $(".search__toggle").on("click", function() {
    $(".search-content").toggleClass("is--visible");
    $(".initial-content").toggleClass("is--hidden");
    // set focus on input
    setTimeout(function() {
      $(".search-content input").focus();
    }, 400);
  });

  // Smooth scrolling: exclude .nav__link (sidebar section links); those use the handler below
  var scroll = new SmoothScroll('a[href*="#"]:not(.nav__link)', {
    header: '.masthead',
    offset: 20,
    speed: 400,
    speedAsDuration: true,
    durationMax: 500
  });

  // Sidebar section links: use getBoundingClientRect so scroll target is correct regardless of current scroll (fixes wrong-spot when clicking second tab)
  function setSidebarActiveFromScroll() {
    var sectionIds = ['papers', 'team', 'section-code'];
    var threshold = 120;
    var currentId = 'papers';
    var nearBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 30;
    if (nearBottom) {
      currentId = 'section-code';
    } else {
      for (var i = 0; i < sectionIds.length; i++) {
        var el = document.getElementById(sectionIds[i]);
        if (el) {
          var top = el.getBoundingClientRect().top;
          if (top <= threshold) currentId = sectionIds[i];
        }
      }
    }
    $('.sidebar .nav__list .nav__link, .section-nav__dropdown-link').each(function() {
      var href = (this.getAttribute('href') || '').split('#').pop();
      var linkId = href && href.length ? href : null;
      if (linkId && sectionIds.indexOf(linkId) !== -1) {
        $(this).toggleClass('active', linkId === currentId);
      }
    });
  }
  setSidebarActiveFromScroll();
  function onScroll() {
    window.requestAnimationFrame(setSidebarActiveFromScroll);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('load', setSidebarActiveFromScroll);
  window.addEventListener('resize', onScroll);
  setInterval(setSidebarActiveFromScroll, 400);
  $('.sidebar .nav__list .nav__link, .section-nav__dropdown-link').on('click', function(e) {
    var href = $(this).attr('href');
    if (!href || href === '#') return;
    var id = href.split('#')[1];
    var el = document.getElementById(id);
    if (!el) return;
    e.preventDefault();
    var masthead = document.querySelector('.masthead');
    var headerHeight = masthead ? masthead.offsetHeight : 0;
    var offset = 20;
    var top = el.getBoundingClientRect().top + window.pageYOffset;
    var target = Math.max(0, top - headerHeight - offset);
    window.scrollTo({ top: target, behavior: 'smooth' });
    if (history.replaceState) history.replaceState(null, '', href);
    setSidebarActiveFromScroll();
    var acToc = document.getElementById('ac-toc');
    if (acToc) acToc.checked = false;
  });

  // Sync body class for section nav (masthead hamburger) open state so CSS can show X icon
  var acToc = document.getElementById('ac-toc');
  if (acToc) {
    function syncSectionNavOpen() {
      document.body.classList.toggle('section-nav-open', acToc.checked);
    }
    syncSectionNavOpen();
    acToc.addEventListener('change', syncSectionNavOpen);
  }

  // Gumshoe scroll spy init
  if($("nav.toc").length > 0) {
    var spy = new Gumshoe("nav.toc a", {
      // Active classes
      navClass: "active", // applied to the nav list item
      contentClass: "active", // applied to the content

      // Nested navigation
      nested: false, // if true, add classes to parents of active link
      nestedClass: "active", // applied to the parent items

      // Offset & reflow
      offset: 20, // how far from the top of the page to activate a content area
      reflow: true, // if true, listen for reflows

      // Event support
      events: true // if true, emit custom events
    });
  }

  // add lightbox class to all image links
  $(
    "a[href$='.jpg'],a[href$='.jpeg'],a[href$='.JPG'],a[href$='.png'],a[href$='.gif'],a[href$='.webp']"
  ).has("> img").addClass("image-popup");

  // Magnific-Popup options
  $(".image-popup").magnificPopup({
    // disableOn: function() {
    //   if( $(window).width() < 500 ) {
    //     return false;
    //   }
    //   return true;
    // },
    type: "image",
    tLoading: "Loading image #%curr%...",
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
    },
    image: {
      tError: '<a href="%url%">Image #%curr%</a> could not be loaded.'
    },
    removalDelay: 500, // Delay in milliseconds before popup is removed
    // Class that is added to body when popup is open.
    // make it unique to apply your CSS animations just to this exact popup
    mainClass: "mfp-zoom-in",
    callbacks: {
      beforeOpen: function() {
        // just a hack that adds mfp-anim class to markup
        this.st.image.markup = this.st.image.markup.replace(
          "mfp-figure",
          "mfp-figure mfp-with-anim"
        );
      }
    },
    closeOnContentClick: true,
    midClick: true // allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source.
  });

  // Add anchors for headings
  $('.page__content').find('h1, h2, h3, h4, h5, h6').each(function() {
    var id = $(this).attr('id');
    if (id) {
      var anchor = document.createElement("a");
      anchor.className = 'header-link';
      anchor.href = '#' + id;
      anchor.innerHTML = '<span class=\"sr-only\">Permalink</span><i class=\"fas fa-link\"></i>';
      anchor.title = "Permalink";
      $(this).append(anchor);
    }
  });
});
