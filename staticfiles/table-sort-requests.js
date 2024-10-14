// table-sort.js
let currentSort = { column: '', order: 'asc' };

function sortTable(column) {
    const url = new URL(window.location);
    const params = new URLSearchParams(url.search);

    if (currentSort.column === column) {
        currentSort.order = currentSort.order === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.order = 'asc';
    }

    params.set('sort_by', currentSort.column);
    params.set('sort_order', currentSort.order);
    window.location.search = params.toString();

    updateHeaderStyles(column);
}

function updateHeaderStyles(column) {
    // Common header styles logic
    const percentHeader = document.querySelector('.percent-header');
    const dateHeader = document.querySelector('.date-header');

    percentHeader.classList.remove('ascending', 'descending');
    dateHeader.classList.remove('ascending', 'descending');

    if (currentSort.column === 'accuracy_percentage') {
        percentHeader.classList.add(currentSort.order === 'asc' ? 'ascending' : 'descending');
    } else if (currentSort.column === 'next_review_date') {
        dateHeader.classList.add(currentSort.order === 'asc' ? 'ascending' : 'descending');
    }
}

function setInitialSortStyles() {
    const urlParams = new URLSearchParams(window.location.search);
    const sortBy = urlParams.get('sort_by');
    const sortOrder = urlParams.get('sort_order');

    if (sortBy) {
        currentSort.column = sortBy;
        currentSort.order = sortOrder || 'asc';
        updateHeaderStyles(currentSort.column);
    }
}

window.onload = setInitialSortStyles;
