from django import forms
from .models import Match, Team


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team1', 'team2', 'goals_team1', 'goals_team2', 'match_date']

