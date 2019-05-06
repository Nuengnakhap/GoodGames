
from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from goodgames.forms import UserAdminChangeForm, UserAdminCreationForm
from goodgames.models import Player, Organizer, Categories, Tournament, Team, Appointment, Match


class PlayerAdmin(UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['id', 'username', 'email', 'firstName', 'lastName']
    list_per_page = 10

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('firstName', 'lastName', 'sex', 'birthday', 'phone1', 'phone2', 'province', 'team')}),
        ('Permissions', {'fields': ('groups', 'user_permissions', 'active', 'admin', 'staff')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    search_fields = ('username',)
    list_filter = []
    # list_filter = ['start_date', 'end_date', 'del_flag']
    # search_fields = ['title']
    #
    # fieldsets = [
    #     (None, {'fields': ['title', 'del_flag']}),
    #     ('Active Duration', {'fields': ['start_date', 'end_date'], 'classes': ['collapse']})
    # ]


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'firstName', 'lastName']
    list_per_page = 10


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']
    list_per_page = 10


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'organizer', 'categories', 'start_date', 'end_date']
    list_per_page = 10


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_name', 'phone']
    list_per_page = 10


class MatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_teams', 'score_home', 'score_away', 'winner', 'loser', 'tournament']
    list_per_page = 10


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_teams', 'start_date', 'end_date']
    list_per_page = 10


admin.site.register(Permission)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Appointment, AppointmentAdmin)
