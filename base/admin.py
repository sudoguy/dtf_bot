from django.contrib import admin

from .models import Comment, Entry


@admin.register(Comment)
class ComentAdmin(admin.ModelAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass
