from django.contrib import admin
from .models import UserProfile, ArtistActivity

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(ArtistActivity)
class ArtistActivityAdmin(admin.ModelAdmin):
    pass