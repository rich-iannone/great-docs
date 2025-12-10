// Early theme initialization to prevent flash of wrong theme
(function() {
    var stored = localStorage.getItem('great-docs-theme');
    var theme = stored || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var html = document.documentElement;
    if (theme === 'dark') {
        html.classList.add('quarto-dark');
        html.setAttribute('data-bs-theme', 'dark');
    } else {
        html.classList.add('quarto-light');
        html.setAttribute('data-bs-theme', 'light');
    }
})();
