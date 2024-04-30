from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Team, Match
from .forms import MatchForm

# Create your views here.


def standings(request):
    teams = Team.objects.order_by('-points', '-goals_difference', '-name')
    return render(request, 'league/standings.html', context={'teams': teams})


def add_match(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Match bien ajouté.')
            return redirect('add_match')
        else:
            return render(request, 'league/add_match.html', context={'form': form})
    else:
        form = MatchForm()
    return render(request, 'league/add_match.html', context={'form': form})


def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    matches = Match.objects.filter(team1=team) | Match.objects.filter(team2=team)
    return render(request, 'league/team_detail.html', {'team':team, 'matches':matches})

