from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'rating', 'date')
    fields = ('first_name', 'last_name', 'email', 'service_category', 'rating', 'feedback', 'date')
    readonly_fields = ('service_category', 'rating', 'feedback', 'date')
    search_fields = ('email',)
    ordering = ('-date',)
    list_per_page = 15
    list_filter = ('rating', 'service_category')
    empty_value_display = "Не указано"


