from django.contrib import admin
from .models import *
# Register your models here.

class NotesAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description']
    list_display_links = ['user']


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['user', 'subjects', 'title', 'due', 'is_finished']
    list_display_links = ['user']

admin.site.register(Notes, NotesAdmin)
admin.site.register(Homework, HomeworkAdmin)