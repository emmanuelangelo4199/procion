// Micro-interactions for micro-habits checklist
document.querySelectorAll('ul li').forEach(item => {
    item.addEventListener('click', function() {
        const circle = this.querySelector('div');
        const text = this.querySelector('span');
        const iconSpan = document.createElement('span');
        
        if (circle.innerHTML === '') {
            circle.classList.remove('border-earth-gray/30');
            circle.classList.add('border-seafoam-mist', 'bg-seafoam-mist', 'text-deep-forest');
            iconSpan.className = 'material-symbols-outlined text-xs';
            iconSpan.textContent = 'check';
            iconSpan.style.fontVariationSettings = "'FILL' 1";
            circle.appendChild(iconSpan);
            text.classList.add('line-through', 'opacity-60');
        } else {
            circle.innerHTML = '';
            circle.classList.remove('border-seafoam-mist', 'bg-seafoam-mist', 'text-deep-forest');
            circle.classList.add('border-earth-gray/30');
            text.classList.remove('line-through', 'opacity-60');
        }
    });
});

// Atmospheric touch: Fade in elements on scroll
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('opacity-100', 'translate-y-0');
            entry.target.classList.remove('opacity-0', 'translate-y-4');
        }
    });
}, observerOptions);

document.querySelectorAll('section, div.lg\\:col-span-8, div.lg\\:col-span-4').forEach(el => {
    el.classList.add('transition-all', 'duration-700', 'ease-out', 'opacity-0', 'translate-y-4');
    observer.observe(el);
});
