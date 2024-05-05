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




"""
class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de l'équipe")
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)

    def update_stats(self, goals_for, goals_against):
        logger.info(f"Updating stats for {self.name} - Goals For: {goals_for}, Goals Against: {goals_against}")
        self.games_played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        self.goal_difference = self.goals_for - self.goals_against

        if goals_for > goals_against:
            self.wins += 1
            self.points += 3
        elif goals_for == goals_against:
            self.draws += 1
            self.points += 1
        else:
            self.losses += 1

        self.save()

    def __str__(self):
        return self.name
"""

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
        return f"{self.home_team} vs {self.away_team} on {self.date}"




"""
        # Using transaction.atomic ensures that all changes are only committed if all parts succeed
        with transaction.atomic():
            existing_played = None
            if self.pk:
                existing_played = Match.objects.get(pk=self.pk).played

            super().save(*args, **kwargs)  # Save the match first

            # Only update team stats if the match has just been played or replayed status changes
            if self.played and (existing_played is None or existing_played != self.played):
                self.home_team.update_stats(self.home_score, self.away_score)
                self.away_team.update_stats(self.away_score, self.home_score)
                logger.info(f"Updated stats for Match {self.pk}")

        logger.info(f"Post-save for Match {self.pk}: successfully saved.")

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"




    def save(self, *args, **kwargs):
        print("Saving Match:", self.pk)
        logger.info(f"Saving match {self.id}, played: {self.played}")
        if self.played:  # Ensure that updates only happen if the match is actually played
            # Save the match first to ensure you have an ID and everything is in order
            super(Match, self).save(*args, **kwargs)
            # Update stats for both teams
            self.home_team.update_stats(self.home_score, self.away_score)
            self.away_team.update_stats(self.away_score, self.home_score)
        else:
            super(Match, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date}"
"""