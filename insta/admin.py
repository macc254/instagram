from django.contrib import admin

# Register your models here.
from .models import Image,Profile,Comment,Follow,Preference,NewsLetterRecipients

admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Preference)
admin.site.register(NewsLetterRecipients)
admin.site.register(Follow)


