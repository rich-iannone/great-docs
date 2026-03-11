/**
 * Announcement Banner for Great Docs
 *
 * Renders a site-wide banner above the navbar. Supports dismiss with
 * sessionStorage so the banner stays hidden for the current browsing session.
 */
(function () {
  "use strict";

  var meta = document.querySelector('meta[name="gd-announcement"]');
  if (!meta) return;

  var content = meta.getAttribute("data-content") || "";
  if (!content) return;

  var type = meta.getAttribute("data-type") || "info";
  var dismissable = meta.getAttribute("data-dismissable") !== "false";
  var url = meta.getAttribute("data-url") || "";
  var style = meta.getAttribute("data-style") || "";

  // Build a storage key from the banner content so a *new* announcement
  // is shown even if the user dismissed a previous one.
  var storageKey = "gd-announcement-dismissed-" + content.length + "-" + hashCode(content);

  if (dismissable && sessionStorage.getItem(storageKey) === "1") {
    return;
  }

  // ── colour map ──
  var colours = {
    info:    { bg: "#0d6efd", fg: "#ffffff" },
    warning: { bg: "#ffc107", fg: "#000000" },
    success: { bg: "#198754", fg: "#ffffff" },
    danger:  { bg: "#dc3545", fg: "#ffffff" },
  };
  var scheme = colours[type] || colours.info;

  // ── build banner element ──
  var banner = document.createElement("div");
  banner.className = "gd-announcement-banner gd-announcement-" + type;
  if (style) {
    banner.className += " gd-gradient-" + style;
  }
  banner.setAttribute("role", "status");

  if (style) {
    // Gradient preset — background/color come from CSS class
    banner.style.cssText =
      "text-align:center;padding:8px 40px;font-size:0.92em;position:relative;";
  } else {
    // Solid colour from type map
    banner.style.cssText =
      "background:" + scheme.bg + ";color:" + scheme.fg +
      ";text-align:center;padding:8px 40px;font-size:0.92em;" +
      "position:relative;";
  }

  // Content (optionally wrapped in a link)
  var inner;
  if (url) {
    inner = document.createElement("a");
    inner.href = url;
    inner.style.cssText = "color:inherit;text-decoration:underline;";
    inner.innerHTML = content;
  } else {
    inner = document.createElement("span");
    inner.innerHTML = content;
  }
  banner.appendChild(inner);

  // Dismiss button
  if (dismissable) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.setAttribute("aria-label", "Dismiss announcement");
    btn.style.cssText =
      "position:absolute;right:12px;top:50%;transform:translateY(-50%);" +
      "background:none;border:none;color:inherit;font-size:1.2em;cursor:pointer;" +
      "opacity:0.8;padding:0 4px;line-height:1;";
    btn.textContent = "\u00d7"; // ×
    btn.addEventListener("click", function () {
      var h = banner.offsetHeight;
      banner.remove();
      sessionStorage.setItem(storageKey, "1");
      // Shrink body padding back down
      var cur = parseFloat(
        window.getComputedStyle(document.body).paddingTop
      ) || 0;
      document.body.style.paddingTop = Math.max(0, cur - h) + "px";
    });
    banner.appendChild(btn);
  }

  // ── insert into the fixed header, above the navbar ──
  var header = document.getElementById("quarto-header");
  if (header && header.firstChild) {
    header.insertBefore(banner, header.firstChild);
  } else {
    // Fallback: prepend to body
    document.body.insertBefore(banner, document.body.firstChild);
  }

  // Adjust body padding to account for the banner height
  requestAnimationFrame(function () {
    var bannerHeight = banner.offsetHeight;
    var currentPadding = parseFloat(
      window.getComputedStyle(document.body).paddingTop
    ) || 0;
    document.body.style.paddingTop = (currentPadding + bannerHeight) + "px";
  });

  // Simple string hash for storage key uniqueness
  function hashCode(str) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0;
    }
    return Math.abs(hash).toString(36);
  }
})();
