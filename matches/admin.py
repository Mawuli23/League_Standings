from django.contrib import admin
from .models import League, Team, Match


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "number_of_teams",
        "start_date",
        "end_date"
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'league',
        'games_played'
    )


@admin.register(Match)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "league",
        "home_team",
        "home_score",
        "away_score",
        "away_team",
        "completed",
    )

