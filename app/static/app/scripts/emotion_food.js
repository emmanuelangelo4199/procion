function toggleEmotion(button) {

    document.querySelectorAll('.emotion-chip').forEach(btn => {
        btn.classList.remove('active');
    });
    
    button.classList.add('active');
}


window.addEventListener('load', () => {
    const sections = document.querySelectorAll('article > header, article section, article > div');
    sections.forEach((el, index) => {

        el.style.opacity = '0';
        el.style.transform = 'translateY(15px)';

        setTimeout(() => {

            el.classList.add('step-transition');
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
            }, 150 * (index + 1));
        });
});