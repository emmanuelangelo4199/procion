function toggleEmotion(button) {
    document.querySelectorAll('.emotion-chip').forEach(btn => {
        btn.classList.remove('active');
    });

    button.classList.add('active');

    const emotionInput = document.getElementById('id_emotion');
    if (emotionInput) {
        emotionInput.value = button.dataset.emotion || '';
    }
}

function restoreSelectedEmotion() {
    const emotionInput = document.getElementById('id_emotion');
    if (!emotionInput || !emotionInput.value) {
        return;
    }

    const selected = document.querySelector(
        `.emotion-chip[data-emotion="${emotionInput.value}"]`
    );
    if (selected) {
        selected.classList.add('active');
    }
}

function setupFoodImagePreview() {
    const input = document.getElementById('id_food_image');
    const preview = document.getElementById('food-image-preview');
    const icon = document.getElementById('food-image-icon');
    const label = document.getElementById('food-image-label');

    if (!input || !preview) {
        return;
    }

    input.addEventListener('change', () => {
        const file = input.files && input.files[0];
        if (!file) {
            preview.classList.add('hidden');
            preview.removeAttribute('src');
            if (icon) icon.classList.remove('hidden');
            if (label) label.classList.remove('hidden');
            return;
        }

        const objectUrl = URL.createObjectURL(file);
        preview.src = objectUrl;
        preview.classList.remove('hidden');
        if (icon) icon.classList.add('hidden');
        if (label) label.classList.add('hidden');
    });
}

function setupFormValidation() {
    const form = document.getElementById('restorative-entry-form');
    if (!form) {
        return;
    }

    form.addEventListener('submit', (event) => {
        const emotionInput = document.getElementById('id_emotion');
        if (emotionInput && emotionInput.value) {
            return;
        }

        event.preventDefault();

        let notice = document.getElementById('emotion-required-notice');
        if (!notice) {
            notice = document.createElement('p');
            notice.id = 'emotion-required-notice';
            notice.className = 'text-sm font-label-md text-error';
            notice.textContent = 'Choose how you are feeling before logging your reflection.';

            const emotionSection = form.querySelector('section');
            if (emotionSection) {
                emotionSection.appendChild(notice);
            }
        }

        const firstChip = form.querySelector('.emotion-chip');
        if (firstChip) {
            firstChip.focus();
        }
    });
}

window.addEventListener('load', () => {
    restoreSelectedEmotion();
    setupFoodImagePreview();
    setupFormValidation();

    const sections = document.querySelectorAll(
        'article > header, article > div, article section, article form'
    );
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
