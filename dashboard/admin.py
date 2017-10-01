from django.contrib import admin

# Import models
from .models import (Yearbook, StudentYearbook,
                    Poll,
                    PollChoice,
                    PollResult,
                    Event,
                    Program)

@admin.register(Yearbook)
class YearbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'end_date', 'active',)
    list_filter = ('active',)

@admin.register(StudentYearbook)
class StudentYearbookAdmin(admin.ModelAdmin):
    list_display = ('student', 'yearbook', 'submit', 'submitted_date',)
    lisst_filter = ('submit',)