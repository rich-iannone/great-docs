/**
 * Content Area Gradient Style for Great Docs
 *
 * Reads the gd-content-style meta tag and applies a subtle radial
 * gradient glow at the top of the main content area using the
 * corresponding gradient preset colours.
 */
(function () {
  "use strict";

  var meta = document.querySelector('meta[name="gd-content-style"]');
  if (!meta) return;

  var preset = meta.getAttribute("data-preset") || "";
  if (!preset) return;

  var content = document.getElementById("quarto-content");
  if (content) {
    content.classList.add("gd-content-glow-" + preset);
  }
})();
