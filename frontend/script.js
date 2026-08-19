document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.header__list-link');
    const sections = document.querySelectorAll('main > section');

    function showSection(targetId) {
        sections.forEach(section => {
            section.classList.add('hidden');
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
        });

        const targetSection = document.querySelector(targetId);
        if (targetSection) {
            targetSection.classList.remove('hidden');
        }
    }

    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();

            const targetId = link.getAttribute('href');
            showSection(targetId);

            link.classList.add('active');
        })
    })
});