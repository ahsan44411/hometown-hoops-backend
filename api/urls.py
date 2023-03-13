from api.views import *
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('tournaments/', TournamentView.as_view()),
    path('leagues/', LeaguesView.as_view()),
    path('camps/', CampsView.as_view()),

    path('get-register/', GetRegisterView.as_view()),
    path('create-register/', CreateRegisterView.as_view()),
    path('edit-register/', EditRegisterView.as_view()),

    path('get-league-schedule/', GetLeagueSchedule.as_view()),
    path('get-team-stats/', GetTeamStats.as_view())
]
