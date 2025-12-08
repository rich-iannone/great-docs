/**
 * Reference Switcher Widget
 *
 * Adds a dropdown switcher above the sidebar to toggle between
 * API Reference and CLI Reference documentation.
 *
 * This widget is automatically injected when CLI documentation is enabled.
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initReferenceSwitcher);
    } else {
        initReferenceSwitcher();
    }

    function initReferenceSwitcher() {
        // Check if we're on a reference page
        const path = window.location.pathname;
        const isApiReference = path.includes('/reference/') && !path.includes('/reference/cli/');
        const isCliReference = path.includes('/reference/cli/');

        if (!isApiReference && !isCliReference) {
            return; // Not on a reference page
        }

        // Find the sidebar
        const sidebar = document.querySelector('.sidebar');
        if (!sidebar) {
            return;
        }

        // Check if CLI reference exists by looking for the link in navigation
        const cliNavLink = document.querySelector('a[href*="/reference/cli/"]');
        const apiNavLink = document.querySelector('a[href*="/reference/"][href$="index.qmd"], a[href*="/reference/"][href$="index.html"]');

        // Only show switcher if both references exist
        if (!cliNavLink && !apiNavLink) {
            return;
        }

        // Create the switcher container
        const switcherContainer = document.createElement('div');
        switcherContainer.className = 'reference-switcher-container';

        // Determine current reference type
        const currentType = isCliReference ? 'cli' : 'api';

        // Create switcher HTML
        switcherContainer.innerHTML = `
            <div class="reference-switcher">
                <button class="reference-switcher-btn ${currentType === 'api' ? 'active' : ''}"
                        data-ref="api"
                        title="API Reference">
                    <i class="bi bi-code-square"></i>
                    <span>API</span>
                </button>
                <button class="reference-switcher-btn ${currentType === 'cli' ? 'active' : ''}"
                        data-ref="cli"
                        title="CLI Reference">
                    <i class="bi bi-terminal"></i>
                    <span>CLI</span>
                </button>
            </div>
        `;

        // Insert at the top of the sidebar-menu-container, before the filter if it exists
        const menuContainer = sidebar.querySelector('.sidebar-menu-container');
        if (!menuContainer) {
            return;
        }

        const filterContainer = menuContainer.querySelector('.sidebar-filter-container');
        if (filterContainer) {
            // Insert before the filter
            menuContainer.insertBefore(switcherContainer, filterContainer);
        } else {
            // Insert at the beginning of the menu container
            menuContainer.insertBefore(switcherContainer, menuContainer.firstChild);
        }

        // Add click handlers
        const buttons = switcherContainer.querySelectorAll('.reference-switcher-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', function() {
                const refType = this.dataset.ref;
                navigateToReference(refType);
            });
        });
    }

    function navigateToReference(refType) {
        const basePath = window.location.pathname.split('/reference/')[0];

        if (refType === 'cli') {
            window.location.href = basePath + '/reference/cli/index.html';
        } else {
            window.location.href = basePath + '/reference/index.html';
        }
    }
})();
