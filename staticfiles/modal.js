// Function to show the modal
function showModal(chineseElement) {
    const modalBody = document.querySelector('#strokeOrderModal .modal-body'); // Select the modal body
    modalBody.style.display = 'flex';
    modalBody.style.flexDirection = 'column';

    // Clear previous content
    const characterContainer = document.getElementById('hanzi-writer');
    characterContainer.innerHTML = ''; // Clear previous content

    // Get the character and its details
    const currentCharacter = chineseElement.textContent.trim();
    const pinyin = chineseElement.getAttribute('data-pinyin');
    const meaning = chineseElement.getAttribute('data-meaning');

    const modalPinyinElement = document.getElementById("modalPinyin");
    const modalMeaningElement = document.getElementById("modalMeaning");

    const pk = chineseElement.getAttribute('data-id');
    const detailLink = document.getElementById('modalDetailLink');
    detailLink.href = `/word/${pk}/`

    // Set Pinyin and Meaning in the modal
    if (modalPinyinElement && modalMeaningElement) {
        modalPinyinElement.textContent = pinyin;
        modalMeaningElement.textContent = meaning;
    } else {
        console.error('Modal elements not found:', {
            modalPinyinElement,
            modalMeaningElement
        });
        return; // Exit the function if elements are not found
    }

    const answers = currentCharacter.split('');

    const isDarkMode = localStorage.getItem('theme') === 'dark';
    const strokeColor = isDarkMode ? '#ffffff' : '#333333';
    const outlineColor = isDarkMode ? '#333333' : '#ffffff';

    // Create character elements and HanziWriter instances
    answers.forEach(function (char, idx) {
        var charTargetId = 'character-target-' + (idx + 1);
        var charDiv = document.createElement('div');
        charDiv.id = charTargetId;
        charDiv.style.width = '100px';
        charDiv.style.height = '100px';
        characterContainer.appendChild(charDiv); // Append to character container

        var writer = HanziWriter.create(charTargetId, char, {
            width: 100,
            height: 100,
            padding: 5,
            strokeAnimationSpeed: 1.5,
            delayBetweenStrokes: 20,
            strokeColor: strokeColor,
            outlineColor: outlineColor,
        });

        // Animate character on click
        charDiv.addEventListener('click', function () {
            writer.animateCharacter();
        });
    });

    // Show the Bootstrap modal
    $('#strokeOrderModal').modal('show');
}
