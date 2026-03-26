/**
 * Responsive Tables for Great Docs
 *
 * Enhances table display on narrow viewports with:
 * - Horizontal scroll containers for wide tables
 * - Touch-friendly scroll indicators
 * - Consistent dark mode styling
 *
 * Uses double-wrapper structure for Safari compatibility:
 * - Outer wrapper (.gd-table-responsive) has position:relative for indicators
 * - Inner wrapper (.gd-table-scroll) has overflow-x:auto for scrolling
 */
(function () {
  "use strict";

  // Minimum width difference to consider a table "wide"
  var OVERFLOW_THRESHOLD = 20;

  /**
   * Wrap a table in a responsive scroll container
   */
  function wrapTable(table) {
    // Skip if already wrapped
    if (table.closest(".gd-table-responsive")) {
      return;
    }

    // Skip tables inside code blocks or other special contexts
    if (table.closest("pre, code, .sourceCode")) {
      return;
    }

    // Create outer wrapper (for indicator positioning)
    var outerWrapper = document.createElement("div");
    outerWrapper.className = "gd-table-responsive";

    // Create inner scroll container
    var scrollContainer = document.createElement("div");
    scrollContainer.className = "gd-table-scroll";
    scrollContainer.setAttribute("tabindex", "0");
    scrollContainer.setAttribute("role", "region");
    scrollContainer.setAttribute("aria-label", "Scrollable table");

    // Insert outer wrapper and move table inside inner container
    table.parentNode.insertBefore(outerWrapper, table);
    scrollContainer.appendChild(table);
    outerWrapper.appendChild(scrollContainer);

    // Add scroll indicators to outer wrapper (not inside scroll container)
    var indicatorLeft = document.createElement("div");
    indicatorLeft.className = "gd-table-scroll-indicator gd-table-scroll-left";
    indicatorLeft.innerHTML = '<span class="gd-scroll-arrow">&lsaquo;</span>';
    outerWrapper.appendChild(indicatorLeft);

    var indicatorRight = document.createElement("div");
    indicatorRight.className = "gd-table-scroll-indicator gd-table-scroll-right";
    indicatorRight.innerHTML = '<span class="gd-scroll-arrow">&rsaquo;</span>';
    outerWrapper.appendChild(indicatorRight);

    // Update scroll indicator visibility based on scroll position
    function updateScrollIndicators() {
      var scrollLeft = scrollContainer.scrollLeft;
      var maxScroll = scrollContainer.scrollWidth - scrollContainer.clientWidth;

      // Only show indicators if scrollable
      if (maxScroll <= OVERFLOW_THRESHOLD) {
        indicatorLeft.classList.remove("visible");
        indicatorRight.classList.remove("visible");
        return;
      }

      // Show/hide based on scroll position
      indicatorLeft.classList.toggle("visible", scrollLeft > OVERFLOW_THRESHOLD);
      indicatorRight.classList.toggle("visible", scrollLeft < maxScroll - OVERFLOW_THRESHOLD);
    }

    // Debounced scroll handler
    var scrollTimeout;
    scrollContainer.addEventListener("scroll", function () {
      if (scrollTimeout) {
        clearTimeout(scrollTimeout);
      }
      scrollTimeout = setTimeout(updateScrollIndicators, 50);
    });

    // Click to scroll
    indicatorLeft.addEventListener("click", function () {
      scrollContainer.scrollBy({ left: -150, behavior: "smooth" });
    });

    indicatorRight.addEventListener("click", function () {
      scrollContainer.scrollBy({ left: 150, behavior: "smooth" });
    });

    // Initial indicator update
    setTimeout(updateScrollIndicators, 100);

    // Update on resize
    var resizeObserver;
    if (typeof ResizeObserver !== "undefined") {
      resizeObserver = new ResizeObserver(function () {
        updateScrollIndicators();
      });
      resizeObserver.observe(scrollContainer);
    }

    return outerWrapper;
  }

  /**
   * Initialize responsive tables
   */
  function init() {
    // Find all tables in the content area
    var content = document.querySelector("#quarto-content, .content, main, article");
    if (!content) {
      content = document.body;
    }

    var tables = content.querySelectorAll("table");
    for (var i = 0; i < tables.length; i++) {
      wrapTable(tables[i]);
    }

    // Handle dynamically added tables (e.g., from AJAX)
    if (typeof MutationObserver !== "undefined") {
      var observer = new MutationObserver(function (mutations) {
        for (var i = 0; i < mutations.length; i++) {
          var mutation = mutations[i];
          for (var j = 0; j < mutation.addedNodes.length; j++) {
            var node = mutation.addedNodes[j];
            if (node.nodeType === 1) {
              // Element node
              if (node.tagName === "TABLE") {
                wrapTable(node);
              } else {
                var nestedTables = node.querySelectorAll
                  ? node.querySelectorAll("table")
                  : [];
                for (var k = 0; k < nestedTables.length; k++) {
                  wrapTable(nestedTables[k]);
                }
              }
            }
          }
        }
      });

      observer.observe(document.body, {
        childList: true,
        subtree: true,
      });
    }
  }

  // Run after DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
