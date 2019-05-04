from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Poll, Question, Choice


# Register your models here.

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class PollAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_date', 'end_date', 'del_flag']
    list_per_page = 10

    list_filter = ['start_date', 'end_date', 'del_flag']
    search_fields = ['title']

    fieldsets = [
        (None, {'fields': ['title', 'del_flag']}),
        ('Active Duration', {'fields': ['start_date', 'end_date'], 'classes': ['collapse']})
    ]

    inlines = [QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'poll', 'text']
    list_per_page = 10

    inlines = [ChoiceInline]

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text', 'value']
    list_per_page = 10


admin.site.register(Permission)
admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)

