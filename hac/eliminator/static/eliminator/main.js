
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.rider').forEach((el) => {
        const header = el.querySelector('.header');
        header.addEventListener('click', () => {
            if (el.classList.contains('expanded')) {
                el.classList.replace('expanded', 'unexpanded');
            } else el.classList.replace('unexpanded', 'expanded');
        });
    });
});