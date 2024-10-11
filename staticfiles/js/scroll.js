let prevScrollPos = window.scrollY;
let isScrollingUp = false;
let hideHeaderTimeout;

window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    const currentScrollPos = window.scrollY;

    if (window.innerWidth <= 768) {
        if (prevScrollPos > currentScrollPos) {
            // Scroll up
            isScrollingUp = true;
            header.classList.remove('hide');
            clearTimeout(hideHeaderTimeout);
        } else if (currentScrollPos > 0) {
            // Scroll down
            isScrollingUp = false;
            hideHeaderTimeout = setTimeout(() => {
                header.classList.add('hide');
            }, 300); // Delay before hiding header
        }

        prevScrollPos = currentScrollPos;
    } else {
        // Always show header on larger screens
        header.classList.remove('hide');
    }

    // Show header if at top of page
    if (currentScrollPos === 0 && isScrollingUp) {
        header.classList.remove('hide');
        isScrollingUp = false;
        clearTimeout(hideHeaderTimeout);
    }
});
