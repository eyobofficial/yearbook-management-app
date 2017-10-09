from django.contrib import admin

# Import models
from .models import (Yearbook, StudentYearbook,
                    Poll,
                    PollChoice,
                    Vote,
                    Event,
                    Program)

@admin.register(Yearbook)
class YearbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'end_date', 'active',)
    list_filter = ('active',)

@admin.register(StudentYearbook)
class StudentYearbookAdmin(admin.ModelAdmin):
    list_display = ('student', 'yearbook', 'submit', 'submitted_date',)
    list_filter = ('submit',)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('poll_text', 'active', 'created_at', 'updated_at', 'end_at',)
    list_filter = ('active', 'end_at',)

@admin.register(PollChoice)
class PollChoiceAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice_text',)
    list_filter = ('poll',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'student', 'choice', 'submitted_date',)
    list_filter = ('poll', 'student', 'choice',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'event_datetime', 'publish',)
    list_filter = ('publish',)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'start_at', 'end_at',)
    list_filter = ('event',)