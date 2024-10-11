window.addEventListener('DOMContentLoaded', function () {
    if ({% if current_user.is_authenticated %} true {% else %} false {% endif %}) {
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
