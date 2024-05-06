from django.urls import path
from .views import index, add_team, list_teams, generate_matches, view_standings
from .views import list_and_update_matches, team_detail

urlpatterns = [
    path("", index, name='index'),
    path("addteam", add_team, name='add_team'),
    path("LesTeams", list_teams, name='listTeam'),
    path('generate_matches/', generate_matches, name='generate_matches'),
    path('standings/', view_standings, name='view_standings'),
    path('matches/', list_and_update_matches, name='list_and_update_matches'),
    path('matches/<int:match_id>/', list_and_update_matches, name='list_and_update_matches'),
    path('team/<int:team_id>/', team_detail, name='team_detail')

]
