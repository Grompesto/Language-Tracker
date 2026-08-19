document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.header__list-link');
    const sections = document.querySelectorAll('main > section');
    const sectionLinks = document.querySelectorAll('a[href^="#"]');

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

    sectionLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();

            const targetId = link.getAttribute('href');
            showSection(targetId);

            if (link.classList.contains('header__list-link'))
            {
                link.classList.add('active');
            }
        });
    });
});