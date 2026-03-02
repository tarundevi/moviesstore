from django.contrib import admin
from .models import Movie, Review, Report, TopCommenter
from django.contrib.auth.models import User
from django.db.models import Count
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
class TopCommenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'comment_count']

admin.site.register(Movie,MovieAdmin)
admin.site.register(Review)
admin.site.register(Report)
admin.site.register(TopCommenter, TopCommenterAdmin)
# Register your models here.
