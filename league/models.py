from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=200)
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    goals_against = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    goals_difference = models.IntegerField(default=0)

    def update_stats(self, goals_for, goals_against):
        self.games_played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        self.goals_difference = self.goals_for - self.goals_against

        if goals_for > goals_against:
            self.wins += 1
            self.points += 3
        elif goals_for == goals_against :
            self.draws += 1
            self.points += 1
        else:
            self.losses += 1

        self.save()

    def __str__(self):
        return self.name


class Match(models.Model):
    team1 = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    goals_team1 = models.IntegerField(validators=[MinValueValidator(0)])
    goals_team2 = models.IntegerField(validators=[MinValueValidator(0)])
    match_date = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.team1.update_stats(self.goals_team1, self.goals_team2)
        self.team2.update_stats(self.goals_team2, self.goals_team1)
