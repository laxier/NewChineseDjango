from django.contrib import admin
from .models import RelatedWord, Sentence

class RelatedWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'related_word')  # Assuming these fields are in RelatedWord model
    search_fields = ('word__simplified', 'related_word__simplified')

class SentenceAdmin(admin.ModelAdmin):
    list_display = ('content', 'chinese_word')
    search_fields = ('content', 'chinese_word__simplified')

# Register only the RelatedWord and Sentence models
admin.site.register(RelatedWord, RelatedWordAdmin)
admin.site.register(Sentence, SentenceAdmin)