from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Song, Album, Play, Artist


class AlbumInLine(admin.TabularInline):
    model = Album


class SongInLine(admin.TabularInline):
    model = Song


class PlayAdmin(admin.ModelAdmin):
    list_display = ('time_stamp', 'user', 'song', 'device')
    search_fields = ['song', 'user', 'device']
    list_filter = ['user']
    # inlines = [SongInLine]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined')


class SongAdmin(admin.ModelAdmin):
    list_display = ('song_name', 'artist_id', 'album_id')
    search_fields = ['song_name']


class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['artist_name']
    inlines = [AlbumInLine, SongInLine]


class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['artist_name']
    inlines = [SongInLine]

admin.site.register(Song, SongAdmin)
admin.site.register(Play, PlayAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)

