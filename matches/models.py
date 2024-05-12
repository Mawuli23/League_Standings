from django.core.validators import MinValueValidator
from django.db import models


class League(models.Model):
    name = models.CharField(max_length=50, unique=True)
    number_of_teams = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    goals_against = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    goal_difference = models.IntegerField(default=0)

    class Meta:
        unique_together = ('name', 'league')

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
        for match in self.home_games.filter(completed=True):
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

        for match in self.away_games.filter(completed=True):
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
    league = models.ForeignKey(League, related_name='matches', on_delete=models.CASCADE)
    date = models.DateField()
    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    home_score = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    away_score = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.completed:
            self.home_team.recalculate_stats()
            self.away_team.recalculate_stats()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"

