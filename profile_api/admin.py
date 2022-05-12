from django.contrib import admin

# Register your models here.

from profile_api import models

admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
