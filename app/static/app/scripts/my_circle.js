// Simple textarea auto-resize
const textarea = document.querySelector('textarea');

textarea.addEventListener('input', function() {

    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});


// Hover effect for side nav
const navItems = document.querySelectorAll('nav > div');

navItems.forEach(item => {

    item.addEventListener('mouseenter', () => {


        if (!item.classList.contains('text-primary')) {
            item.style.transform = 'translateX(4px)';
        
        }
    });

    item.addEventListener('mouseleave', () => {
        item.style.transform = 'translateX(0px)';
    });
});