from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import *


# Register your models here.
class TournamentsRulesInline(admin.TabularInline):
    model = TournamentsRules
    extra = 0


class TournamentsRegisterInline(admin.TabularInline):
    model = TournamentsRegister
    extra = 0


class TournamentsRulesAdmin(admin.ModelAdmin):
    inlines = [
        TournamentsRulesInline,
        TournamentsRegisterInline
    ]


admin.site.register(Tournaments, TournamentsRulesAdmin)


class CampsChildRegisterInline(NestedStackedInline):
    model = CampsChildRegister
    extra = 0
    fk_name = 'camp_register'


class CampsRegisterInline(NestedStackedInline):
    model = CampsRegister
    extra = 0
    fk_name = 'camp'
    inlines = [CampsChildRegisterInline]


class CampsRulesInline(NestedStackedInline):
    model = CampsRules
    extra = 0
    fk_name = 'camp'


class CampsAdmin(NestedModelAdmin):
    model = Camps
    inlines = [CampsRulesInline, CampsRegisterInline]


admin.site.register(Camps, CampsAdmin)


class LeaguesRulesInline(NestedStackedInline):
    model = LeaguesRules
    extra = 0
    fk_name = 'league'


class LeagueTeamStatsInline(NestedStackedInline):
    model = LeagueTeamStats
    extra = 0
    fk_name = 'leagues_register'


class LeagueTeamMembersInline(NestedStackedInline):
    model = LeagueTeamMembers
    extra = 0
    fk_name = 'leagues_register'


class LeaguesRegisterInline(NestedStackedInline):
    model = LeaguesRegister
    extra = 0
    fk_name = 'league'
    inlines = [LeagueTeamStatsInline, LeagueTeamMembersInline]


class LeagueScheduleInline(NestedStackedInline):
    model = LeagueSchedule
    extra = 0
    fk_name = 'league'


class LeagueAdmin(NestedModelAdmin):
    model = Leagues
    inlines = [LeaguesRulesInline, LeagueScheduleInline, LeaguesRegisterInline]


admin.site.register(Leagues, LeagueAdmin)
