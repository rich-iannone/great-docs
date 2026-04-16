/**
 * Version Selector Widget for Great Docs
 *
 * Provides a navbar dropdown for switching between documentation versions.
 * Reads version metadata from _version_map.json (embedded as a meta tag).
 *
 * Features:
 * - Dropdown in the navbar showing all configured versions
 * - Pre-release and end-of-life indicators
 * - Graceful fallback when a page doesn't exist in the target version
 * - localStorage persistence of selected version
 * - URL parameter override (?v=0.2)
 * - Keyboard accessible
 */

(function () {
  "use strict";

  // Configurable storage key
  var STORAGE_KEY = "great-docs-version";

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function getVersionMap() {
    try {
      var meta = document.querySelector('meta[name="gd-version-map"]');
      return meta ? JSON.parse(meta.getAttribute("content")) : null;
    } catch (e) {
      return null;
    }
  }

  function getStoredVersion() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function setStoredVersion(tag) {
    try {
      localStorage.setItem(STORAGE_KEY, tag);
    } catch (e) {
      // localStorage not available
    }
  }

  /**
   * Determine the current version tag by inspecting the URL path.
   * If the path starts with /v/<tag>/, return that tag.  Otherwise return
   * the tag of whichever version has an empty path_prefix (latest).
   */
  function detectCurrentVersion(versionMap) {
    var path = window.location.pathname;

    for (var i = 0; i < versionMap.versions.length; i++) {
      var v = versionMap.versions[i];
      if (v.path_prefix && path.indexOf("/" + v.path_prefix + "/") === 0) {
        return v.tag;
      }
    }

    // No prefix matched — we're on the latest (root) version
    for (var j = 0; j < versionMap.versions.length; j++) {
      if (versionMap.versions[j].latest) {
        return versionMap.versions[j].tag;
      }
    }

    return versionMap.versions.length ? versionMap.versions[0].tag : null;
  }

  /**
   * Build the URL for a given page path under a specific version.
   */
  function buildVersionUrl(versionMap, targetTag, currentRelPath) {
    var targetVersion = null;
    for (var i = 0; i < versionMap.versions.length; i++) {
      if (versionMap.versions[i].tag === targetTag) {
        targetVersion = versionMap.versions[i];
        break;
      }
    }
    if (!targetVersion) return null;

    var basePath = window.location.pathname.replace(/\/[^/]*$/, "");

    // Strip current version prefix to get the relative page path
    var pagePath = currentRelPath;

    // Check if the page exists in the target version
    var pageExists =
      versionMap.pages &&
      versionMap.pages[pagePath] &&
      versionMap.pages[pagePath].indexOf(targetTag) !== -1;

    if (!pageExists && versionMap.fallbacks && versionMap.fallbacks[pagePath]) {
      pagePath = versionMap.fallbacks[pagePath];
    } else if (!pageExists) {
      // Ultimate fallback: version root
      pagePath = "index.html";
    }

    var prefix = targetVersion.path_prefix;
    if (prefix) {
      return "/" + prefix + "/" + pagePath;
    }
    return "/" + pagePath;
  }

  /**
   * Get the current page's relative path (without version prefix).
   */
  function getCurrentRelPath(versionMap) {
    var path = window.location.pathname;

    // Strip version prefix if present
    for (var i = 0; i < versionMap.versions.length; i++) {
      var v = versionMap.versions[i];
      if (v.path_prefix && path.indexOf("/" + v.path_prefix + "/") === 0) {
        return path.substring(v.path_prefix.length + 2); // +2 for leading and trailing /
      }
    }

    // No prefix — strip leading /
    return path.substring(1) || "index.html";
  }

  // ---------------------------------------------------------------------------
  // Widget creation
  // ---------------------------------------------------------------------------

  function createVersionSelector(versionMap) {
    var currentTag = detectCurrentVersion(versionMap);
    var currentRelPath = getCurrentRelPath(versionMap);

    // Find current version entry
    var currentVersion = null;
    for (var i = 0; i < versionMap.versions.length; i++) {
      if (versionMap.versions[i].tag === currentTag) {
        currentVersion = versionMap.versions[i];
        break;
      }
    }
    if (!currentVersion) return;

    // Create container
    var container = document.createElement("div");
    container.className = "gd-version-selector";
    container.setAttribute("role", "navigation");
    container.setAttribute("aria-label", "Version selector");

    // Create toggle button
    var toggle = document.createElement("button");
    toggle.className = "gd-version-toggle";
    toggle.setAttribute("aria-haspopup", "listbox");
    toggle.setAttribute("aria-expanded", "false");
    toggle.innerHTML =
      '<span class="gd-version-label">v' +
      currentVersion.tag +
      "</span>" +
      '<span class="gd-version-chevron">&#9662;</span>';

    // Create dropdown
    var dropdown = document.createElement("ul");
    dropdown.className = "gd-version-dropdown";
    dropdown.setAttribute("role", "listbox");
    dropdown.style.display = "none";

    for (var j = 0; j < versionMap.versions.length; j++) {
      var v = versionMap.versions[j];
      var item = document.createElement("li");
      item.setAttribute("role", "option");
      item.className = "gd-version-item";
      if (v.tag === currentTag) {
        item.classList.add("gd-version-current");
        item.setAttribute("aria-selected", "true");
      }

      var indicator = "";
      if (v.prerelease) indicator = '<span class="gd-vi gd-vi-pre">●</span>';
      else if (v.eol) indicator = '<span class="gd-vi gd-vi-eol">⚠</span>';
      else if (v.tag === currentTag)
        indicator = '<span class="gd-vi gd-vi-cur">✓</span>';

      var link = document.createElement("a");
      link.href = buildVersionUrl(versionMap, v.tag, currentRelPath) || "#";
      link.innerHTML = indicator + v.label;
      link.setAttribute("data-version", v.tag);

      link.addEventListener(
        "click",
        (function (tag) {
          return function (e) {
            setStoredVersion(tag);
          };
        })(v.tag)
      );

      item.appendChild(link);
      dropdown.appendChild(item);
    }

    container.appendChild(toggle);
    container.appendChild(dropdown);

    // Toggle dropdown on click
    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var expanded = dropdown.style.display !== "none";
      dropdown.style.display = expanded ? "none" : "block";
      toggle.setAttribute("aria-expanded", String(!expanded));
    });

    // Close on outside click
    document.addEventListener("click", function () {
      dropdown.style.display = "none";
      toggle.setAttribute("aria-expanded", "false");
    });

    // Keyboard navigation
    container.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        dropdown.style.display = "none";
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });

    // Insert into navbar
    var navbar = document.querySelector(".navbar-nav.navbar-nav-scroll");
    if (!navbar) navbar = document.querySelector("nav.navbar .container-fluid");
    if (navbar) {
      navbar.appendChild(container);
    }
  }

  // ---------------------------------------------------------------------------
  // Warning banners
  // ---------------------------------------------------------------------------

  function injectWarningBanner(versionMap) {
    var currentTag = detectCurrentVersion(versionMap);
    var currentVersion = null;
    var latestVersion = null;

    for (var i = 0; i < versionMap.versions.length; i++) {
      if (versionMap.versions[i].tag === currentTag)
        currentVersion = versionMap.versions[i];
      if (versionMap.versions[i].latest)
        latestVersion = versionMap.versions[i];
    }

    if (!currentVersion || currentVersion.latest) return;
    if (!latestVersion) return;

    var banner = document.createElement("div");
    banner.className = "gd-version-banner";

    var currentRelPath = getCurrentRelPath(versionMap);
    var latestUrl =
      buildVersionUrl(versionMap, latestVersion.tag, currentRelPath) || "/";

    if (currentVersion.eol) {
      banner.classList.add("gd-version-banner-eol");
      banner.innerHTML =
        '<span class="gd-vb-icon">⛔</span> ' +
        "Version " +
        currentVersion.label +
        " is no longer supported. " +
        '<a href="' +
        latestUrl +
        '">Switch to ' +
        latestVersion.label +
        " →</a>";
    } else if (currentVersion.prerelease) {
      banner.classList.add("gd-version-banner-pre");
      banner.innerHTML =
        '<span class="gd-vb-icon">🔬</span> ' +
        "Pre-release documentation (" +
        currentVersion.label +
        "). May contain unreleased features. " +
        '<a href="' +
        latestUrl +
        '">Switch to stable →</a>';
    } else {
      banner.classList.add("gd-version-banner-old");
      banner.innerHTML =
        '<span class="gd-vb-icon">⚠️</span> ' +
        "You are viewing documentation for version " +
        currentVersion.label +
        ". " +
        '<a href="' +
        latestUrl +
        '">Switch to ' +
        latestVersion.label +
        " (latest) →</a>";
    }

    // Insert before main content
    var main =
      document.querySelector("#quarto-content") || document.querySelector("main");
    if (main && main.parentNode) {
      main.parentNode.insertBefore(banner, main);
    }
  }

  // ---------------------------------------------------------------------------
  // Init
  // ---------------------------------------------------------------------------

  function init() {
    var versionMap = getVersionMap();
    if (!versionMap || !versionMap.versions || !versionMap.versions.length) return;

    createVersionSelector(versionMap);

    // Check if warning banners are enabled (meta tag)
    var bannerMeta = document.querySelector(
      'meta[name="gd-version-warning-banner"]'
    );
    var showBanner = !bannerMeta || bannerMeta.getAttribute("content") !== "false";
    if (showBanner) {
      injectWarningBanner(versionMap);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
