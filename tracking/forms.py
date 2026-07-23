from django import forms
from .models import FoodMoodLog, Emotion


class FoodMoodLogForm(forms.ModelForm):
    # The primary mood selected by the user.
    emotion = forms.ChoiceField(
        choices=Emotion.choices,
        widget=forms.HiddenInput,
    )
    # Sensory description of flavors, textures, or warmth.
    food_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe the flavors, the warmth...',
            'class': (
                'w-full h-32 bg-transparent border-0 border-b border-soft-sage/60 '
                'p-0 font-headline-sm text-2xl text-deep-forest '
                'placeholder:text-outline-variant focus:ring-0 focus:border-deep-forest '
                'transition-all resize-none'
            ),
            'rows': 4,
        }),
    )
    # Optional captured picture of the meal snapshot.
    food_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'absolute inset-0 opacity-0 cursor-pointer',
            'accept': 'image/*',
        }),
    )
    
    # The model fields to include in the form.
    class Meta:
        model = FoodMoodLog
        fields = ('emotion', 'food_description', 'food_image')
