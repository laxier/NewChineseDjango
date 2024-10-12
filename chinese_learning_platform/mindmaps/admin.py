from django.contrib import admin
from django import forms
from .models import MindMap, WordInMindMap


class WordInMindMapInline(admin.TabularInline):
    model = WordInMindMap
    extra = 1  # Number of empty forms to display
    autocomplete_fields = ['word', 'parent']

@admin.register(MindMap)
class MindMapAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    inlines = [WordInMindMapInline]

@admin.register(WordInMindMap)
class WordInMindMapAdmin(admin.ModelAdmin):
    list_display = ('word', 'mind_map', 'parent')
    search_fields = ('word__simplified', 'word__pinyin', 'mind_map__title')
    list_filter = ('mind_map', 'parent')
