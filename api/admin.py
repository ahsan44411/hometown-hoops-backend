from django.contrib import admin
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


class CampsRulesInline(admin.TabularInline):
    model = CampsRules
    extra = 0


class CampsRulesAdmin(admin.ModelAdmin):
    inlines = [
        CampsRulesInline,
    ]


class LeaguesRulesInline(admin.TabularInline):
    model = LeaguesRules
    extra = 0


class LeaguesRulesAdmin(admin.ModelAdmin):
    inlines = [
        LeaguesRulesInline,
    ]


admin.site.register(Camps, CampsRulesAdmin)
admin.site.register(Leagues, LeaguesRulesAdmin)
