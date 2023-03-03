from api.views import *
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('tournaments/', TournamentView.as_view()),

    path('camps/', CampsView.as_view()),

    path('leagues/', LeaguesView.as_view()),
]
