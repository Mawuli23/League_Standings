from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import HttpResponseRedirect
from itertools import permutations, combinations
from django.db.models import F, Sum, Count
from django.contrib import messages
from django.forms import modelformset_factory
import datetime
from django.urls import reverse_lazy, reverse
from .models import League, Team, Match
from django.views.generic import View, ListView, TemplateView, CreateView, FormView, DeleteView, UpdateView
from .forms import MatchTypeForm, ScoreUpdateForm, TeamForm


class HomePageView(TemplateView):
    template_name = 'matches/home.html'


class CreateLeagueView(CreateView):
    model = League
    template_name = 'matches/createLeague.html'
    fields = ['name', 'number_of_teams', 'start_date', 'end_date']
    success_url = reverse_lazy('createLeague')


class DeleteLeagueView(DeleteView):
    model = League
    template_name = 'matches/confirmDelete.html'
    success_url = reverse_lazy('allLeague')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete League'
        return context


class ShowLeagueView(ListView):
    model = League
    template_name = 'matches/showLeague.html'
    context_object_name = 'leagues'


class CreateTeamView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'matches/createTeam.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league_id = self.kwargs.get('league_id')
        if league_id:
            context['league'] = League.objects.get(id=league_id)
        return context

    def get_initial(self):
        initial = super().get_initial()
        league_id = self.kwargs.get('league_id')
        if league_id:
            initial['league'] = League.objects.get(id=league_id)
        return initial

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('createTeam', kwargs={'league_id': self.kwargs.get('league_id')})


class DeleteTeamView(DeleteView):
    model = Team
    template_name = 'matches/confirmDelete.html'
    success_url = reverse_lazy('allLeague')
    context_object_name = 'teams'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = 'Delete Team'
        return context


class GenerateMatchesView(FormView):
    template_name = 'matches/generateMatches.html'
    form_class = MatchTypeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['league'] = League.objects.get(pk=self.kwargs.get('league_id'))
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.league = get_object_or_404(League, pk=self.kwargs['league_id'])  # Accessing league_id from URL kwargs
        return kwargs

    def form_valid(self, form):
        league = self.league
        match_type = form.cleaned_data['match_type']
        teams = list(league.teams.all())

        Match.objects.filter(league=league).delete()

        for team in teams:
            team.reset_stats()

        if match_type == 'double':
            match_pairs = permutations(teams, 2)
        else:
            match_pairs = combinations(teams, 2)

        with transaction.atomic():
            for home_team, away_team in match_pairs:
                Match.objects.create(
                    league=league,
                    home_team=home_team,
                    away_team=away_team,
                    date=datetime.date.today(),
                    home_score=0,
                    away_score=0,
                    completed=False
                )

        return HttpResponseRedirect(reverse_lazy('matchList', kwargs={'league_id': league.id}))

    def form_invalid(self, form):
        return super().form_invalid(form)


class MatchListView(ListView):
    model = Match
    context_object_name = 'matches'
    template_name = 'matches/leagueMatches.html'

    def get_queryset(self):
        league_id = self.kwargs.get('league_id')
        return Match.objects.filter(league__id=league_id).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league_id = self.kwargs.get('league_id')
        context['league'] = get_object_or_404(League, pk=league_id)
        return context


class TeamListView(ListView):
    model = Team
    context_object_name = 'teams'
    template_name = 'matches/leagueTeams.html'

    def get_queryset(self):
        league_id = self.kwargs.get('league_id')
        return Team.objects.filter(league__id=league_id).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league_id = self.kwargs.get('league_id')
        context['league'] = get_object_or_404(League, pk=league_id)
        return context


class TeamMatchesListView(ListView):
    model = Match
    template_name = 'matches/teamMatches.html'
    context_object_name = 'matches'

    def get_queryset(self):
        league_id = self.kwargs.get('league_id')
        team_id = self.kwargs.get('team_id')
        league = get_object_or_404(League, pk=league_id)
        team = get_object_or_404(Team, pk=team_id, league=league)
        return Match.objects.filter(league=league).filter(away_team=team, home_team=team).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['league'] = get_object_or_404(League, pk=self.kwargs.get('league_id'))
        context['team'] = get_object_or_404(Team, pk=self.kwargs.get('team_id'))
        return context


class ListAndUpdateMatchesView(View):
    template_name = 'matches/updateLeagueScore.html'

    def get(self, request, *args, **kwargs):
        league_id = self.kwargs['league_id']
        league = get_object_or_404(League, pk=league_id)
        matches = Match.objects.filter(league=league).order_by('date')
        return render(request, self.template_name, {'matches': matches, 'league': league})

    def post(self, request, *args, **kwargs):
        league_id = self.kwargs['league_id']
        league = get_object_or_404(League, pk=league_id)
        match_id = request.POST.get('match_id')
        if match_id:
            match = get_object_or_404(Match, pk=match_id, league=league)
            form = ScoreUpdateForm(request.POST, instance=match)
            if form.is_valid():
                match.completed = True
                form.save()
                return redirect('updateLeagueMatches', league_id=league_id)
            else:
                print("Form errors:", form.errors)
        else:
            print("Match ID not provided in POST data")
        matches = Match.objects.filter(league=league).order_by('date')
        return render(request, self.template_name, {'matches': matches, 'league': league})


class LeagueStandingsView(ListView):
    model = Team
    template_name = 'matches/leagueStandings.html'
    context_object_name = 'teams'

    def get_queryset(self):
        league_id = self.kwargs.get('league_id')
        return Team.objects.filter(league__id=league_id).order_by('-points', '-goal_difference', '-goals_for', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['league'] = League.objects.get(pk=self.kwargs.get('league_id'))
        return context


class AllLeagueStandingsView(ListView):
    model = League
    template_name = 'matches/allLeagueStandings.html'
    context_object_name = 'leagues'

    def get_queryset(self):
        leagues = League.objects.annotate(
            teams_count=Count('teams')
        ).prefetch_related('teams')

        for league in leagues:
            league.sorted_teams = league.teams.annotate(
                total_points=Sum('points'),
                total_goals_for=Sum('goals_for'),
                total_goals_against=Sum('goals_against'),
                goal_differences=F('total_goals_for') - F('total_goals_against')
            ).order_by('-total_points', '-goal_difference', '-total_goals_for', 'name')

        return leagues
