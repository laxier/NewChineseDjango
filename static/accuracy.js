window.addEventListener('DOMContentLoaded', function () {
    if (isAuthenticated) {
        const accuracyCells = document.querySelectorAll('.percent');
        accuracyCells.forEach(function (cell) {
            const accuracy = parseInt(cell.textContent);
            if (accuracy >= 80) {
                cell.classList.add('green');
            } else if (accuracy >= 60) {
                cell.classList.add('yellow');
            } else if (accuracy >= 20) {
                cell.classList.add('red');
            }
        });
    }
});
