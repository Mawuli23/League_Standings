from django import forms
from .models import Team, Match
from django.core.exceptions import ValidationError


class MatchTypeForm(forms.Form):
    match_type = forms.ChoiceField(
        choices=[('single', 'Single-leg'), ('double', 'Double-leg')],
        label="Select Match Type",
        widget=forms.RadioSelect
    )


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


"""
class ScoreForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_score', 'away_score', 'played']
        widgets = {
            'played': forms.HiddenInput(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.played = True  # Set played to True when saving the form
        if commit:
            instance.save()
        return instance
"""


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_score', 'away_score']
        widgets = {
            'home_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'away_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    """def clean_home_score(self):
        home_score = self.cleaned_data.get('home_score')
        if home_score < 0:
            raise ValidationError("Home score cannot be negative.")
        return home_score

    def clean_away_score(self):
        away_score = self.cleaned_data.get('away_score')
        if away_score < 0:
            raise ValidationError("Away score cannot be negative.")
        return away_score"""

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.played = True  # Automatically mark as played when the form is saved
        if commit:
            instance.save()
        return instance

