from django.contrib import admin
from .models import Prefecture, Goal, Impression, Changeapplication, Changedhistory

# Register your models here.
admin.site.register(Prefecture)
admin.site.register(Goal)
admin.site.register(Impression)
admin.site.register(Changeapplication)
admin.site.register(Changedhistory)


