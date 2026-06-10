// Subtle interaction for inputs
const inputs = document.querySelectorAll('input');

inputs.forEach(input => {
    input.addEventListener('focus', () => {

        input.parentElement.querySelector('label').classList.add('text-primary');
    });
    input.addEventListener('blur', () => {
        if(!input.value) {
            input.parentElement.querySelector('label').classList.remove('text-primary');
        }
    });
});


// Atmospheric fade-in effect on load
window.addEventListener('load', () => {

    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 1s ease-in-out';

    requestAnimationFrame(() => {
        document.body.style.opacity = '1';
    });
});