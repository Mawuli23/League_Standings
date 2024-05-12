from django.urls import path
from .views import HomePageView, CreateLeagueView, ShowLeagueView, CreateTeamView, GenerateMatchesView
from .views import MatchListView, ListAndUpdateMatchesView, LeagueStandingsView, DeleteLeagueView, TeamListView
from .views import AllLeagueStandingsView, TeamMatchesListView

urlpatterns = [
    path("", HomePageView.as_view(), name='index'),
    path("leagues", CreateLeagueView.as_view(), name='createLeague'),
    path('league/<int:pk>/delete/', DeleteLeagueView.as_view(), name='deleteLeague'),
    path("all-leagues", ShowLeagueView.as_view(), name='allLeague'),
    path('create-team/<int:league_id>/', CreateTeamView.as_view(), name='createTeam'),
    path('teams/<int:league_id>/allTeams', TeamListView.as_view(), name='teamList'),
    path('league/<int:league_id>/generate-matches/', GenerateMatchesView.as_view(), name='generateMatches'),
    path('matches/<int:league_id>/allMatches', MatchListView.as_view(), name='matchList'),
    path('league/<int:league_id>/update-matches/', ListAndUpdateMatchesView.as_view(), name='updateLeagueMatches'),
    path('league/<int:league_id>/standings/', LeagueStandingsView.as_view(), name='leagueStandings'),
    path('all/leagues/standings/', AllLeagueStandingsView.as_view(), name='allLeagueStandings'),
    path('leagues/<int:league_id>/teams/<int:team_id>/matches/', TeamMatchesListView.as_view(), name='teamMatches'),
]
