/**
 * Navbar Gradient Style for Great Docs
 *
 * Reads the gd-navbar-style meta tag and applies the corresponding
 * animated gradient CSS class to the navbar element.
 */
(function () {
  "use strict";

  var meta = document.querySelector('meta[name="gd-navbar-style"]');
  if (!meta) return;

  var preset = meta.getAttribute("data-preset") || "";
  if (!preset) return;

  var navbar = document.querySelector(".navbar");
  if (navbar) {
    navbar.classList.add("gd-gradient-" + preset);
  }
})();

/**
 * Sticky navbar on desktop — keep sidebars positioned below the header.
 *
 * Quarto's headroom.js hides the navbar on scroll-down and shifts sidebars
 * (top: 0) to fill the vacated space. Our CSS keeps the navbar visible on
 * desktop (>= 992px), so we must also prevent the sidebar repositioning.
 * Listens for the quarto-hrChanged event that fires after every headroom
 * pin/unpin and re-applies the correct sidebar top/maxHeight.
 */
(function () {
  "use strict";

  var mql = window.matchMedia("(min-width: 992px)");

  function fixSidebars() {
    if (!mql.matches) return;

    var header = document.querySelector("#quarto-header");
    if (!header) return;
    var h = header.offsetHeight;

    var els = document.querySelectorAll(".sidebar, .headroom-target");
    els.forEach(function (el) {
      el.style.top = h + "px";
      el.style.maxHeight = "calc(100vh - " + h + "px)";
    });
  }

  window.addEventListener("quarto-hrChanged", fixSidebars);
  mql.addEventListener("change", fixSidebars);
})();
