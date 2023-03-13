from api.models import *
from django.utils import timezone
from rest_framework import serializers


class TournamentsRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentsRules
        fields = "__all__"


class TournamentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournaments
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)

        rules = TournamentsRulesSerializer(
            TournamentsRules.objects.filter(tournament__id=response['id']), many=True
        ).data

        return {**response, "rules": rules}


class TournamentsRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentsRegister
        fields = "__all__"


class LeagueRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaguesRegister
        fields = "__all__"


class CampsRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampsRules
        fields = "__all__"


class CampsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camps
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)

        rules = CampsRulesSerializer(
            CampsRules.objects.filter(camp__id=response['id']), many=True
        ).data

        return {**response, "rules": rules}


class CampsChildRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampsChildRegister
        fields = "__all__"


class CampRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampsRegister
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['children'] = CampsChildRegisterSerializer(
            CampsChildRegister.objects.filter(camp_register_id=response['id']), many=True
        ).data

        return response


class LeaguesRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaguesRules
        fields = "__all__"


class LeaguesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leagues
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)

        league = Leagues.objects.filter(id=response['id']).last()
        today = timezone.now().date()

        if today > league.closeDate:
            response['closed'] = True
        else:
            response['closed'] = False

        rules = LeaguesRulesSerializer(
            LeaguesRules.objects.filter(league__id=response['id']), many=True
        ).data

        return {**response, "rules": rules}


class LeagueScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeagueSchedule
        fields = "__all__"


class LeagueTeamStatsSchedule(serializers.ModelSerializer):
    leagues_register = LeagueRegisterSerializer()

    class Meta:
        model = LeagueTeamStats
        fields = "__all__"


class LeagueTeamMembersSerializer(serializers.ModelSerializer):
    leagues_register = LeagueRegisterSerializer()

    class Meta:
        model = LeagueTeamMembers
        fields = "__all__"
