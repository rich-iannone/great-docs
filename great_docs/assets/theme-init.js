// Early theme initialization to prevent flash of wrong theme
(function() {
    var stored = localStorage.getItem('great-docs-theme');
    var theme = stored || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var html = document.documentElement;

    // Hide body until theme is fully applied to prevent flash
    html.classList.add('theme-loading');

    if (theme === 'dark') {
        html.classList.add('quarto-dark');
        html.setAttribute('data-bs-theme', 'dark');
    } else {
        html.classList.add('quarto-light');
        html.setAttribute('data-bs-theme', 'light');
    }

    // Reveal page once DOM is ready and styles are applied
    function revealPage() {
        // Small delay to ensure CSS is processed
        requestAnimationFrame(function() {
            html.classList.remove('theme-loading');
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', revealPage);
    } else {
        revealPage();
    }
})();
