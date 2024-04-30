from django.urls import path
from .views import standings, add_match, team_detail

urlpatterns = [
    path('', standings, name='standings'),
    path('add/', add_match, name='add_match'),
    path('team/<int:team_id>/', team_detail, name='team_detail')
]