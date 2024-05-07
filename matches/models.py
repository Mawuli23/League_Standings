from django.db import models, transaction
import logging
from django.core.validators import MinValueValidator
logger = logging.getLogger(__name__)
# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de l'équipe")
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    goals_against = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    goal_difference = models.IntegerField(default=0)

    def reset_stats(self):
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0
        self.save()

    def recalculate_stats(self):
        # Reset stats
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        self.goal_difference = 0

        # Recalculate from all played games
        for match in self.home_games.filter(played=True):
            self.games_played += 1
            self.goals_for += match.home_score
            self.goals_against += match.away_score
            if match.home_score > match.away_score:
                self.wins += 1
                self.points += 3
            elif match.home_score == match.away_score:
                self.draws += 1
                self.points += 1
            else:
                self.losses += 1

        for match in self.away_games.filter(played=True):
            self.games_played += 1
            self.goals_for += match.away_score
            self.goals_against += match.home_score
            if match.away_score > match.home_score:
                self.wins += 1
                self.points += 3
            elif match.away_score == match.home_score:
                self.draws += 1
                self.points += 1
            else:
                self.losses += 1

        self.goal_difference = self.goals_for - self.goals_against
        self.save()

    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    home_score = models.IntegerField(null=True, blank=True,verbose_name="Score Équipe Domicile", validators=[MinValueValidator(0)])
    away_score = models.IntegerField(null=True, blank=True,verbose_name="Score Équipe Extérieur", validators=[MinValueValidator(0)])
    date = models.DateField(verbose_name="Date du match")
    played = models.BooleanField(default=False, verbose_name="Match Joué")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.played:
            self.home_team.recalculate_stats()
            self.away_team.recalculate_stats()

    def __str__(self):
        #f"{self.home_team} vs {self.away_team} on {self.date}"
        return f"{self.home_team} vs {self.away_team}"


