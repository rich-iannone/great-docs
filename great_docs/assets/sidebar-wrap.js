/**
 * Sidebar Smart Wrap for Great Docs
 *
 * Inserts <wbr> (word break opportunity) elements into long sidebar item
 * names so the browser can break lines at aesthetically pleasing points:
 *   - After dots:        store.DuckDBStore  →  break after each "."
 *   - After underscores: retrieve_bm25      →  break after "_"
 *   - After open paren:  connect()          →  break after "("
 *   - At camelCase:      DuckDBStore        →  break before uppercase runs
 *
 * The <wbr> tag is invisible and zero-width; the browser only uses it as a
 * line-break opportunity when the text overflows its container.
 */

(function () {
    'use strict';

    /**
     * Insert <wbr> elements at smart break points in a text node.
     *
     * Break opportunities are placed:
     *   1. After every "."  (module separators)
     *   2. After every "_"  (snake_case boundaries)
     *   3. After every "("  (before argument lists)
     *   4. Before a run of uppercase letters preceded by a lowercase letter
     *      (camelCase → camel + Case), but only when the run is followed by
     *      a lowercase letter (e.g. "DBStore" keeps "DB" together and breaks
     *      before "Store").
     *
     * The regex uses zero-width look-behind/ahead so the actual characters
     * are preserved in the output — only <wbr> tags are inserted.
     */
    function insertSmartBreaks(text) {
        // Split text at break-opportunity points.
        // The regex captures the delimiter so we can reassemble with <wbr>
        // after each delimiter character.
        //
        // Pattern pieces:
        //   ([._])          – capture a dot or underscore
        //   (\()            – capture an opening paren
        //   (?<=[a-z])(?=[A-Z])  – zero-width camelCase boundary
        //
        // We use a two-pass approach because JS regex has limited support
        // for look-behind in older runtimes.

        var result = document.createDocumentFragment();
        // Pattern: split around ".", "_", "(", and camelCase transitions
        // Two camelCase lookarounds:
        //   (?<=[a-z])(?=[A-Z])       – lowercase-to-uppercase: "Duck|DB"
        //   (?<=[A-Z])(?=[A-Z][a-z])  – end of acronym run:    "DB|Document"
        var parts = text.split(/([._()])|(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])/);
        // Filter out empty/undefined entries produced by the regex split
        var filtered = parts.filter(function (p) { return p !== undefined && p !== ''; });
        for (var i = 0; i < filtered.length; i++) {
            result.appendChild(document.createTextNode(filtered[i]));
            // Insert <wbr> between every pair of adjacent parts.
            // Each split boundary is a valid break opportunity (dot, underscore,
            // paren, or camelCase transition), so a <wbr> between every pair
            // covers all cases — including acronym→word boundaries like DB|Document.
            if (i < filtered.length - 1) {
                result.appendChild(document.createElement('wbr'));
            }
        }
        return result;
    }

    /**
     * Process all <span class="menu-text"> elements inside the sidebar.
     */
    function processSidebar() {
        var sidebar = document.getElementById('quarto-sidebar');
        if (!sidebar) return;

        var spans = sidebar.querySelectorAll('.menu-text');
        for (var i = 0; i < spans.length; i++) {
            var span = spans[i];
            var text = span.textContent;
            if (!text) continue;
            // Only process items that contain separator characters or camelCase /
            // acronym boundaries (skip plain short words like "API", "Classes")
            if (!/[._()]/.test(text) && !/[a-z][A-Z]/.test(text) && !/[A-Z]{2,}[a-z]/.test(text)) continue;
            // Replace the text content with smart-break nodes
            var fragment = insertSmartBreaks(text);
            span.textContent = '';
            span.appendChild(fragment);
        }
    }

    // Run after DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', processSidebar);
    } else {
        processSidebar();
    }
})();
