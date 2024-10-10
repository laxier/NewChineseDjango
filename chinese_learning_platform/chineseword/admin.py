from django.contrib import admin
from .models import ChineseWord
@admin.register(ChineseWord)
class ChineseWordAdmin(admin.ModelAdmin):
    list_display = ('simplified', 'traditional', 'pinyin', 'meaning')
    search_fields = ('simplified', 'traditional', 'pinyin', 'meaning')
    list_filter = ('simplified',)
