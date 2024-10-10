from django.contrib import admin
from .models import MindMap, Category, ChineseWord, WordInMindMap

@admin.register(MindMap)
class MindMapAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'mind_map')
    search_fields = ('name',)
    list_filter = ('mind_map',)

@admin.register(ChineseWord)
class ChineseWordAdmin(admin.ModelAdmin):
    list_display = ('simplified', 'traditional', 'pinyin', 'meaning')
    search_fields = ('simplified', 'traditional', 'pinyin', 'meaning')
    list_filter = ('simplified',)

@admin.register(WordInMindMap)
class WordInMindMapAdmin(admin.ModelAdmin):
    list_display = ('word', 'mind_map', 'parent')
    search_fields = ('word__simplified', 'word__pinyin', 'mind_map__title')
    list_filter = ('mind_map', 'parent')
    filter_horizontal = ('categories',)