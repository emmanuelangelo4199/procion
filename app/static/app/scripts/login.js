// Subtle micro-interaction for input fieldsv
document.querySelectorAll('input').forEach(input => {

    input.addEventListener('focus', () => {
        input.parentElement.querySelector('label').style.color = '#061b0e';
    });

    input.addEventListener('blur', () => {
        input.parentElement.querySelector('label').style.color = '';
    });
});

// Atmospheric parallax effect on image (throttle for performance)
const editorialSection = document.querySelector('section img');
if (editorialSection) {

    window.addEventListener('mousemove', (e) => {
        
        const moveX = (e.clientX - window.innerWidth / 2) / 100;
        const moveY = (e.clientY - window.innerHeight / 2) / 100;
        editorialSection.style.transform = `scale(1.1) translate(${moveX}px, ${moveY}px)`;
    });
}