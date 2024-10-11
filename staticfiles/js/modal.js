let currentIndex = 0;
let isChildClicked = false;

function showModal(answer, index, chineseElements, isChildClicked) {
    const modalBody = document.querySelector('.modal-body');
    modalBody.innerHTML = ''; // Clear previous content
    modalBody.style.display = 'flex';
    modalBody.style.flexDirection = 'column';

    const controlsContainer = document.createElement('div');
    controlsContainer.classList.add('controls-container');
    controlsContainer.innerHTML = `
        <button class="control-button prev-button">&lt;</button>
        <button class="control-button next-button">&gt;</button>
    `;
    modalBody.appendChild(controlsContainer);

    // Additional code for HanziWriter and fetching translations goes here

    $('#modal').modal('show');

    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');

    if (index === 0) {
        prevButton.style.display = 'none';
    } else {
        prevButton.style.display = 'block';
    }

    if (index === chineseElements.length - 1) {
        nextButton.style.display = 'none';
    } else {
        nextButton.style.display = 'block';
    }

    prevButton.addEventListener('click', prevHandler);
    nextButton.addEventListener('click', nextHandler);
}

function fetchTranslation(char) {
    return fetch('/api/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'char': char })
    })
    .then(response => response.json())
    .catch(error => console.error('Ошибка:', error));
}

// Event handlers for prevHandler and nextHandler go here

document.addEventListener('keydown', keyHandler);
