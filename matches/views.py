from django.shortcuts import render, redirect, get_object_or_404
from .forms import TeamForm, ScoreForm, MatchTypeForm
from .models import Team, Match
from itertools import permutations, combinations
import datetime
from django.db import transaction
# Create your views here.


def index(request):
    return render(request, 'matches/index.html')


def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Rediriger vers la page d'accueil ou une autre page appropriée
    else:
        form = TeamForm()
    return render(request, 'matches/add_team.html', {'form': form})


def list_teams(request):
    teams = Team.objects.all().order_by('name')
    return render(request, 'matches/list_teams.html', {'teams': teams})


def team_detail(request, team_id=None):
    team = get_object_or_404(Team, pk=team_id)
    matches = Match.objects.filter(home_team=team) | Match.objects.filter(away_team=team)
    return render(request, 'matches/team_detail.html', {'team':team, 'matches':matches})

def generate_matches(request):
    if request.method == 'POST':
        form = MatchTypeForm(request.POST)
        if form.is_valid():
            match_type = form.cleaned_data['match_type']
            teams = Team.objects.all()
            for team in teams:
                team.reset_stats()

            Match.objects.all().delete()

            today = datetime.date.today()
            match_pairs = permutations(teams, 2) if match_type == 'double' else combinations(teams, 2)

            with transaction.atomic():
                for home_team, away_team in match_pairs:
                    Match.objects.create(
                        home_team=home_team,
                        away_team=away_team,
                        date=today,
                        home_score=None,
                        away_score=None,
                        played=False
                    )
                    if match_type == 'double':
                        # Create the reverse match for double-leg
                        Match.objects.create(
                            home_team=away_team,
                            away_team=home_team,
                            date=today,  # You might want to set a different date for the return leg
                            home_score=None,
                            away_score=None,
                            played=False
                        )

            return redirect('list_and_update_matches')
    else:
        form = MatchTypeForm()

    return render(request, 'matches/generate_matches.html', {'form': form})


"""
def generate_matches(request):
    #teams = list(Team.objects.all())
    teams = Team.objects.all()

    for team in teams:
        team.reset_stats()

    Match.objects.all().delete()  # Optionnel : Supprimer tous les matchs existants avant de générer de nouveaux

    # Générer des matchs aller-retour
    today = datetime.date.today()
    for home_team, away_team in permutations(teams, 2):
        Match.objects.create(home_team=home_team, away_team=away_team, date=today)
        #today += datetime.timedelta(days=1)  # Assigne chaque match à un jour différent, à ajuster selon le besoin

    matches = Match.objects.all()
    return render(request, 'matches/generate_matches.html', {'matches': matches})


def update_match_score(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=match)
        if form.is_valid():
            match = form.save(commit=False)
            match.played = True  # Set played to True before saving the match
            match.save()
            return redirect('list_matches')  # Redirect to an appropriate URL
    else:
        form = ScoreForm(instance=match)
    return render(request, 'matches/update_score.html', {'form': form, 'match': match})


def list_matches(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if request.method == 'POST':
        form = ScoreForm(request.POST, instance=match)
        if form.is_valid():
            match = form.save(commit=False)
            match.played = True  # Set played to True before saving the match
            match.save()
            return redirect('list_matches')  # Redirect to an appropriate URL
    else:
        form = ScoreForm(instance=match)

    ##############
    matches = Match.objects.all().order_by('date')  # Assurez-vous que les matchs sont triés par date
    return render(request, 'matches/list_matches.html', {'form': form, 'match': match, 'matches': matches})
"""

def view_standings(request):
    standings = Team.objects.order_by('-points', '-goal_difference', 'name')
    return render(request, 'matches/team_standings.html', {'standings': standings})


"""def list_and_update_matches(request, match_id=None):
    if match_id:
        match = get_object_or_404(Match, pk=match_id)
        if request.method == 'POST':
            form = ScoreForm(request.POST, instance=match)
            if form.is_valid():
                form.save()
                return redirect('list_and_update_matches')  # Redirect to the same page to see the updated list
        else:
            form = ScoreForm(instance=match)
    else:
        form = None
        match = None

    matches = Match.objects.all().order_by('date')
    return render(request, 'matches/list_and_update_matches.html', {
        'matches': matches,
        'form': form,
        'current_match': match
    })"""


def list_and_update_matches(request, match_id=None):
    if request.method == 'POST':
        match_id = request.POST.get('match_id')
        if match_id:
            match = get_object_or_404(Match, pk=match_id)
            form = ScoreForm(request.POST, instance=match)
            if form.is_valid():
                form.save()
                return redirect('list_and_update_matches')
            else:
                print("Form errors:", form.errors)
        else:
            print("Match ID not provided in POST data")
    matches = Match.objects.all().order_by('date')
    return render(request, 'matches/list_and_update_matches.html', {'matches': matches})
