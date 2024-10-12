function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function initializeQuiz(rows, progressBarId, userId, deckId, onEnd) {
    const progressBar = document.getElementById(progressBarId);
    progressBar.ariaValueMax = rows.length;
    const increment = 100 / rows.length;
    let progress = 0;
    let currentFlashcardIndex = 0;
    let countRight = 0;
    let isQuizEnding = false;

    displayFlashcard(currentFlashcardIndex, rows);

    // Add event listeners
    document.getElementById("flashcard").addEventListener("click", function (event) {
        if (event.target.tagName === 'BUTTON') {
            return; // Prevent toggle if button is clicked
        }
        toggleFlashcard();
    });

    function toggleFlashcard() {
        const front = document.querySelector('#flashcard .front');
        const back = document.querySelector('#flashcard .back');
        front.style.display = (front.style.display === "none") ? "flex" : "none";
        back.style.display = (back.style.display === "none") ? "flex" : "none";
    }

    function displayFlashcard(index) {
        const front = document.querySelector('#flashcard .front');
        const back = document.querySelector('#flashcard .back');
        front.style.display = "flex";
        back.style.display = "none";
        const currentRow = rows[index];

        document.getElementById("front-character").textContent = currentRow.querySelector('.simplified').textContent;
        document.getElementById("back-pronunciation").textContent = currentRow.querySelector('.pinyin').textContent;
        document.getElementById("back-translation").textContent = currentRow.querySelector('.meaning').textContent;
    }

    function getNextFlashcard() {
        if (currentFlashcardIndex < rows.length - 1) {
            currentFlashcardIndex++;
            progress += increment;
            progressBar.style.width = `${progress}%`;
            displayFlashcard(currentFlashcardIndex);
        } else {
            endQuiz(); // End the quiz when all flashcards have been displayed
        }
    }

    function endQuiz() {
        if (isQuizEnding) return; // Prevent executing if already ending the quiz
        isQuizEnding = true;

        // Animate progress bar to 100%
        progress = 100;
        progressBar.style.width = `${progress}%`;
        setTimeout(function () {
            alert("Больше нет слов, перезапускаю\n" + `${Math.round(countRight / rows.length * 100)}%`);
            onEnd(countRight);
        }, 500); // 500ms delay (adjust as needed)
    }

    // Attach event listeners for correct/incorrect answers
    document.getElementById("quiz-right").addEventListener('click', markCorrect);
    document.getElementById("quiz-wrong").addEventListener('click', markIncorrect);

    function markCorrect() {
        rows[currentFlashcardIndex].classList.add("green");
        countRight++;
        sendResultToAPI(true);
        getNextFlashcard();
    }

    function markIncorrect() {
        rows[currentFlashcardIndex].classList.add("red");
        sendResultToAPI
