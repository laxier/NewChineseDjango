from django.contrib import admin
from .models import MindMap, Category, WordInMindMap, ChineseWord

class WordInMindMapInline(admin.TabularInline):
    model = WordInMindMap
    extra = 1  # Number of empty forms to display
    autocomplete_fields = ['word']  # Enable autocomplete for selecting ChineseWord

@admin.register(MindMap)
class MindMapAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    inlines = [WordInMindMapInline]  # Add the inline to MindMapAdmin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'mind_map')
    search_fields = ('name',)
    list_filter = ('mind_map',)

@admin.register(WordInMindMap)
class WordInMindMapAdmin(admin.ModelAdmin):
    list_display = ('word', 'mind_map', 'parent')
    search_fields = ('word__simplified', 'word__pinyin', 'mind_map__title')
    list_filter = ('mind_map', 'parent')
    filter_horizontal = ('categories',)