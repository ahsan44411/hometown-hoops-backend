from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers import TournamentsSerializer, CampsSerializer, LeaguesSerializer
from api.models import Tournaments, Camps, Leagues, TournamentsRegister, CampsRegister, LeaguesRegister


class TournamentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = timezone.now().date()
        queryset = Tournaments.objects.filter(openDate__lte=today, closeDate__gte=today)
        response = TournamentsSerializer(queryset, many=True).data
        return Response(data=response, status=200)

    def post(self, request):
        try:
            user = request.user
            data = request.data
            tournament = Tournaments.objects.get(id=data['tournament_id'])

            data.pop('tournament_id')

            TournamentsRegister.objects.create(user=user, tournament=tournament, **data)
            return Response(data="Registration Successful", status=200)
        except Exception as e:
            print(e)
            return Response(data="Failed to register", status=400)


class CampsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = timezone.now().date()
        queryset = Camps.objects.filter(openDate__lte=today, closeDate__gte=today)
        response = CampsSerializer(queryset, many=True).data
        return Response(data=response, status=200)

    def post(self, request):
        try:
            user = request.user
            data = request.data
            camp = Camps.objects.get(id=data['camp_id'])

            data.pop('camp_id')

            CampsRegister.objects.create(user=user, camp=camp, **data)
            return Response(data="Registration Successful", status=200)
        except Exception as e:
            print(e)
            return Response(data="Failed to register", status=400)


class LeaguesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = timezone.now().date()
        queryset = Leagues.objects.filter(openDate__lte=today, closeDate__gte=today)
        response = LeaguesSerializer(queryset, many=True).data
        return Response(data=response, status=200)

    def post(self, request):
        try:
            user = request.user
            data = request.data
            league = Leagues.objects.get(id=data['league_id'])

            data.pop('league_id')

            LeaguesRegister.objects.create(user=user, league=league, **data)
            return Response(data="Registration Successful", status=200)
        except Exception as e:
            print(e)
            return Response(data="Failed to register", status=400)
