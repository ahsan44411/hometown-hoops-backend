from api.views import *
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('get-tournament/', GetTournamentView.as_view()),
    path('create-tournament/', CreateTournamentView.as_view()),

    path('get-camps/', GetCampsView.as_view()),
    path('create-camps/', CreateCampsView.as_view()),

    path('get-leagues/', GetLeaguesView.as_view()),
    # path('create-leagues/', CreateLeaguesView.as_view()),
]
