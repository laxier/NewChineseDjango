function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Global variable to store CSRF token and current word ID
const csrftoken = getCookie('csrftoken');
let currentWordId;

// Function to update the favorite button appearance
function updateFavoriteButton(button, isFavorite) {
    if (isFavorite) {
        button.textContent = 'Unfavorite'; // Set text to "Unfavorite"
        button.classList.remove('btn-danger');
        button.classList.add('btn-secondary'); // Change to secondary color for "Unfavorite"
        button.setAttribute('data-favorite-status', 'true'); // Set favorite status
    } else {
        button.textContent = 'Favorite'; // Set text to "Favorite"
        button.classList.remove('btn-secondary');
        button.classList.add('btn-danger'); // Change back to original color for "Favorite"
        button.setAttribute('data-favorite-status', 'false'); // Set non-favorite status
    }
}

// Function to fetch favorite status from the API
async function getFavoriteStatus(wordId) {
    try {
        const response = await fetch(`/api/v1/words/${wordId}/favorite-status/`);
        if (!response.ok) throw new Error('Error fetching favorite status');

        const data = await response.json(); // Assume the API returns a JSON object with favorite status
        return data.is_favorite; // Adjust based on your API response structure
    } catch (error) {
        console.error('Error fetching favorite status:', error);
        return false; // Default to not favorite in case of an error
    }
}

// Function to populate the modal with character details
function populateModalContent(chineseElement) {
    const currentCharacter = chineseElement.textContent.trim();
    const pinyin = chineseElement.getAttribute('data-pinyin');
    const meaning = chineseElement.getAttribute('data-meaning');

    currentWordId = chineseElement.getAttribute('data-id'); // Set currentWordId here

    document.getElementById("modalPinyin").textContent = pinyin;
    document.getElementById("modalMeaning").textContent = meaning;
    document.getElementById('modalDetailLink').href = `/word/${currentWordId}/`;

    return currentCharacter; // Return the current character for further processing
}

// Function to create character elements and animate them
function createCharacterElements(answers) {
    const characterContainer = document.getElementById('hanzi-writer');
    const isDarkMode = localStorage.getItem('theme') === 'dark';
    const strokeColor = isDarkMode ? '#ffffff' : '#333333';
    const outlineColor = isDarkMode ? '#333333' : '#ffffff';

    answers.forEach((char, idx) => {
        const charTargetId = 'character-target-' + (idx + 1);
        const charDiv = document.createElement('div');
        charDiv.id = charTargetId;
        charDiv.style.width = '100px';
        charDiv.style.height = '100px';
        characterContainer.appendChild(charDiv); // Append to character container

        // Create a HanziWriter instance for the character
        const writer = HanziWriter.create(charTargetId, char, {
            width: 100,
            height: 100,
            padding: 5,
            strokeAnimationSpeed: 1.5,
            delayBetweenStrokes: 20,
            strokeColor: strokeColor,
            outlineColor: outlineColor,
        });

        // Animate character on click
        charDiv.addEventListener('click', () => {
            writer.animateCharacter();
        });
    });
}

// Function to show the modal
async function showModal(chineseElement) {
    const modalBody = document.querySelector('#strokeOrderModal .modal-body');
    modalBody.style.display = 'flex';
    modalBody.style.flexDirection = 'column';

    // Clear previous content
    document.getElementById('hanzi-writer').innerHTML = '';

    // Populate the modal with content
    const currentCharacter = populateModalContent(chineseElement);

    // Get the favorite status from the API
    const isFavorite = await getFavoriteStatus(currentWordId);

    // Update the favorite button based on the fetched status
    const favoriteButton = document.getElementById("favorite-button");
    updateFavoriteButton(favoriteButton, isFavorite);

    // Create character elements and HanziWriter instances
    createCharacterElements(currentCharacter.split(''));

    // Show the Bootstrap modal
    $('#strokeOrderModal').modal('show');
}

// Function to toggle favorite status
function toggleFavorite(wordId) {
    const favoriteButton = document.getElementById("favorite-button");
    const isCurrentlyFavorite = favoriteButton.getAttribute('data-favorite-status') === 'true';

    fetch(`/api/v1/words/${wordId}/favorite/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, // Ensure you have the CSRF token defined
        },
    })
        .then(response => {
            if (response.ok) {
                // Update the button state based on the new favorite status
                updateFavoriteButton(favoriteButton, !isCurrentlyFavorite); // Toggle the status
                // Update the favorite status on the word element if necessary
                document.querySelector(`[data-id="${wordId}"]`).setAttribute('data-favorite', !isCurrentlyFavorite);
            } else {
                console.error('Error toggling favorite:', response.statusText);
            }
        })
        .catch(error => console.error('Error:', error));
}
