from django.contrib import admin

from .models import Date


class DateAdmin(admin.ModelAdmin):
    search_fields = ['date', 'text']


admin.site.register(Date, DateAdmin)