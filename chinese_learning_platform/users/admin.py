from django.contrib import admin
from .models import Deck, WordPerformance, DeckPerformance, DeckWord

class DeckWordInline(admin.TabularInline):
    model = DeckWord
    extra = 1

    def get_queryset(self, request):
        # Use select_related for foreign keys in DeckWord to optimize query
        queryset = super().get_queryset(request)
        return queryset.select_related('deck', 'word')


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator',)
    search_fields = ('name', 'creator__username')
    inlines = [DeckWordInline]

@admin.register(WordPerformance)
class WordPerformanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'right', 'wrong', 'timestamp', 'next_review_date')
    search_fields = ('user__username', 'word__character')
    list_filter = ('user',)

@admin.register(DeckPerformance)
class DeckPerformanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'deck', 'percent_correct', 'test_date')
    search_fields = ('user__username', 'deck__name')
    list_filter = ('user',)
