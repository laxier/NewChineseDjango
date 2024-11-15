from django.contrib import admin
from .models import ChineseWord


@admin.register(ChineseWord)
class ChineseWordAdmin(admin.ModelAdmin):
    list_display = ('simplified', 'traditional', 'pinyin', 'meaning', 'hsk_level')
    search_fields = ('simplified', 'traditional', 'pinyin', 'meaning')
    list_filter = ('hsk_level',)

    # Define the actions
    actions = [
        'set_hsk_level_0',
        'set_hsk_level_1',
        'set_hsk_level_2',
        'set_hsk_level_3',
        'set_hsk_level_4',
        'set_hsk_level_5',
        'set_hsk_level_6',
    ]

    # Define the action methods
    def set_hsk_level_0(self, request, queryset):
        """Set HSK level to 0 for the selected words."""
        updated_count = queryset.update(hsk_level='0')
        self.message_user(request, f"{updated_count} words updated to HSK level 0.")

    def set_hsk_level_1(self, request, queryset):
        """Set HSK level to 1 for the selected words."""
        updated_count = queryset.update(hsk_level='1')
        self.message_user(request, f"{updated_count} words updated to HSK level 1.")

    def set_hsk_level_2(self, request, queryset):
        """Set HSK level to 2 for the selected words."""
        updated_count = queryset.update(hsk_level='2')
        self.message_user(request, f"{updated_count} words updated to HSK level 2.")

    def set_hsk_level_3(self, request, queryset):
        """Set HSK level to 3 for the selected words."""
        updated_count = queryset.update(hsk_level='3')
        self.message_user(request, f"{updated_count} words updated to HSK level 3.")

    def set_hsk_level_4(self, request, queryset):
        """Set HSK level to 4 for the selected words."""
        updated_count = queryset.update(hsk_level='4')
        self.message_user(request, f"{updated_count} words updated to HSK level 4.")

    def set_hsk_level_5(self, request, queryset):
        """Set HSK level to 5 for the selected words."""
        updated_count = queryset.update(hsk_level='5')
        self.message_user(request, f"{updated_count} words updated to HSK level 5.")

    def set_hsk_level_6(self, request, queryset):
        """Set HSK level to 6 for the selected words."""
        updated_count = queryset.update(hsk_level='6')
        self.message_user(request, f"{updated_count} words updated to HSK level 6.")

    # Optional: Customize the description of each action in the admin panel
    set_hsk_level_0.short_description = "Set HSK level to 0"
    set_hsk_level_1.short_description = "Set HSK level to 1"
    set_hsk_level_2.short_description = "Set HSK level to 2"
    set_hsk_level_3.short_description = "Set HSK level to 3"
    set_hsk_level_4.short_description = "Set HSK level to 4"
    set_hsk_level_5.short_description = "Set HSK level to 5"
    set_hsk_level_6.short_description = "Set HSK level to 6"
