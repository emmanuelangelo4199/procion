// Simple toggle logic for the switches
document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {

    checkbox.addEventListener('change', function() {

        const parent = this.closest('section');
        if (this.checked) {
            console.log('Setting enabled');
        } 
        else {

            console.log('Setting disabled');
        }
    });
});


// Ambient hover effects for ritual cards
const ritualCards = document.querySelectorAll('.bg-surface');
ritualCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-4px)';
    });
    card.addEventListener('mouseleave', () => {

        card.style.transform = 'translateY(0px)';
    });
});