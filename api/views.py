from django.db.models import Count
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.models import Tournaments, Camps, Leagues, TournamentsRegister, CampsRegister, LeaguesRegister, CampsChildRegister, LeagueSchedule, LeagueTeamStats, LeagueTeamMembers
from api.serializers import TournamentsSerializer, CampsSerializer, LeaguesSerializer, TournamentsRegisterSerializer, LeagueRegisterSerializer, CampRegisterSerializer, \
    LeagueScheduleSerializer, LeagueTeamStatsSchedule, LeagueTeamMembersSerializer


class TournamentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = timezone.now().date()
        queryset = Tournaments.objects.filter(openDate__lte=today, closeDate__gte=today)
        response = TournamentsSerializer(queryset, many=True).data
        for data in response:
            if request.user.is_authenticated and TournamentsRegister.objects.filter(user=request.user, tournament_id=data['id']):
                data['edit'] = True
            else:
                data['edit'] = False

        return Response(data=response, status=200)


class LeaguesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # today = timezone.now().date()
        # queryset = Leagues.objects.filter(openDate__lte=today, closeDate__gte=today)
        queryset = Leagues.objects.all()
        response = LeaguesSerializer(queryset, many=True).data
        for data in response:
            if request.user.is_authenticated and LeaguesRegister.objects.filter(user=request.user, league_id=data['id']):
                data['edit'] = True
            else:
                data['edit'] = False

        return Response(data=response, status=200)


class CampsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        today = timezone.now().date()
        queryset = Camps.objects.filter(openDate__lte=today, closeDate__gte=today)
        response = CampsSerializer(queryset, many=True).data
        for data in response:
            if request.user.is_authenticated and CampsRegister.objects.filter(user=request.user, camp_id=data['id']):
                data['edit'] = True
            else:
                data['edit'] = False

        return Response(data=response, status=200)


class GetRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if data['type'] == 'tournaments':
            response = TournamentsRegisterSerializer(
                TournamentsRegister.objects.filter(tournament_id=data['id'], user=request.user).last()
            ).data
        elif data['type'] == 'leagues':
            response = LeagueRegisterSerializer(
                LeaguesRegister.objects.filter(league_id=data['id'], user=request.user).last()
            ).data
        else:
            response = CampRegisterSerializer(
                CampsRegister.objects.filter(camp_id=data['id'], user=request.user).last()
            ).data

        return Response(data=response, status=200)


class CreateRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # try:
        user = request.user
        data = request.data
        id = data.pop('id')
        type = data.pop('type')

        if 'children' in data:
            children = data.pop('children')
        else:
            children = []

        if type == 'tournaments':
            TournamentsRegister.objects.create(user=user, tournament=Tournaments.objects.get(id=id), **data)
        elif type == 'leagues':
            LeaguesRegister.objects.create(user=user, league=Leagues.objects.get(id=id), **data)
        else:
            camp_register = CampsRegister.objects.create(user=user, camp=Camps.objects.get(id=id), **data)
            child_reg_arr = []
            for child in children:
                child_reg_arr.append(CampsChildRegister(camp_register=camp_register, name=child['name'], age=child['age']))

            CampsChildRegister.objects.bulk_create(child_reg_arr)

        return Response(data="Registration Successful", status=200)
    # except Exception as e:
    #     print(e)
    #     return Response(data="Failed to register", status=400)


class EditRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if data['type'] == 'tournaments':
            tournaments_register_serializer = TournamentsRegisterSerializer(
                TournamentsRegister.objects.get(id=data['id']), data=data, partial=True
            )

            tournaments_register_serializer.is_valid(raise_exception=True)
            tournaments_register_serializer.save()
        elif data['type'] == 'leagues':
            league_register_serializer = LeagueRegisterSerializer(
                LeaguesRegister.objects.get(id=data['id']), data=data, partial=True
            )

            league_register_serializer.is_valid(raise_exception=True)
            league_register_serializer.save()
        else:
            camp_register = CampsRegister.objects.get(id=data['id'])
            camp_register.parent_first_name = data['parent_first_name']
            camp_register.parent_last_name = data['parent_last_name']
            camp_register.email = data['email']
            camp_register.cell_number = data['cell_number']
            camp_register.save()

            children = data['children']
            CampsChildRegister.objects.filter(camp_register=camp_register).delete()
            child_reg_arr = []
            for child in children:
                child_reg_arr.append(CampsChildRegister(camp_register=camp_register, name=child['name'], age=child['age']))

            CampsChildRegister.objects.bulk_create(child_reg_arr)

        return Response({"message": "Information Saved"}, status=200)
    # except Exception as e:
    #     print(e)
    #     return Response({"error": "Could not save information"}, status=500)


class GetLeagueSchedule(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        id = data['id']

        img = LeagueScheduleSerializer(LeagueSchedule.objects.filter(league=id).last()).data['img']

        league = Leagues.objects.filter().last()

        teams = LeagueTeamStatsSchedule(LeagueTeamStats.objects.filter(leagues_register__league=id).order_by('-wins'), many=True).data

        data = {"name": league.name, "img": img, "teams": teams}

        return Response(data=data, status=200)


class GetTeamStats(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        id = data['id']

        data = []

        members = LeagueTeamMembers.objects.filter(leagues_register=id).values('name').annotate(dcount=Count('name'))

        for member in members:
            name = member['name']

            points = 0
            rebounds = 0
            assists = 0
            num = 0

            member_stats = LeagueTeamMembers.objects.filter(leagues_register=id, name=name)

            for member_stat in member_stats:
                points += member_stat.points
                rebounds += member_stat.rebounds
                assists += member_stat.assists
                num += 1

            if len(member_stats) > 0:
                data.append({
                    "name": member_stats[0].name,
                    "points": points / num,
                    "rebounds": rebounds / num,
                    "assists": assists / num
                })

        return Response(data=data, status=200)
