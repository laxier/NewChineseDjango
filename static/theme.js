function getTheme() {
    return localStorage.getItem('theme') || 'light';
}

function toggleTheme() {
    const body = document.body;
    const checkbox = document.getElementById('darkSwitch');
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
        checkbox.checked = false;
    } else {
        body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
        checkbox.checked = true;
    }
}

window.addEventListener('DOMContentLoaded', function () {
    const theme = getTheme();
    if (theme === 'dark') {
        document.body.classList.add('dark-theme');
        document.getElementById('darkSwitch').checked = true;
    }
});
