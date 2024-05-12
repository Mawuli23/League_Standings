from django import forms
from .models import Team, Match, League


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'league']

    def clean(self):
        cleaned_data = super().clean()
        league = cleaned_data.get('league')

        if league:
            current_teams_count = Team.objects.filter(league=league).count()
            if current_teams_count >= league.number_of_teams:
                raise forms.ValidationError({
                    'league': f"This league has already reached its maximum number of teams ({league.number_of_teams})."
                })
        return cleaned_data


class MatchTypeForm(forms.Form):
    match_type = forms.ChoiceField(
        choices=[('single', 'Single-leg'), ('double', 'Double-leg')],
        label="Select Match Type",
        widget=forms.RadioSelect
    )


class ScoreUpdateForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_score', 'away_score', 'completed']

