// Main script file
document.addEventListener('DOMContentLoaded', function () {
    console.log('Sentinela App Loaded');

    // Add active class to current nav item (handled in backend but good for client-side interactions)
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
