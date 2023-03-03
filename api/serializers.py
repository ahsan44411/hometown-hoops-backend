from api.models import *
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

        rules = LeaguesRulesSerializer(
            LeaguesRules.objects.filter(league__id=response['id']), many=True
        ).data

        return {**response, "rules": rules}
