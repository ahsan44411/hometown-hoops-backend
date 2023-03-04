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


# class CampsRulesInline(admin.TabularInline):
#     model = CampsRules
#     extra = 0
#
#
# class CampsRegisterInline(admin.TabularInline):
#     model = CampsRegister
#     extra = 0
#     show_change_link = True
#
#
# class CampsChildrenRegisterInline(admin.TabularInline):
#     model = CampsChildRegister
#     extra = 0
#
#
# class CampsRegisterAdmin(admin.ModelAdmin):
#     inlines = [
#         CampsChildrenRegisterInline
#     ]
#
#
# class CampsRulesAdmin(admin.ModelAdmin):
#     inlines = [
#         CampsRulesInline,
#         CampsRegisterInline,
#     ]
#
#
# admin.site.register(CampsChildRegister)
# admin.site.register(Camps, CampsRulesAdmin)

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


class LeaguesRulesInline(admin.TabularInline):
    model = LeaguesRules
    extra = 0


class LeaguesRegisterInline(admin.TabularInline):
    model = LeaguesRegister
    extra = 0


class LeaguesRulesAdmin(admin.ModelAdmin):
    inlines = [
        LeaguesRegisterInline,
        LeaguesRulesInline,
    ]


admin.site.register(Leagues, LeaguesRulesAdmin)
