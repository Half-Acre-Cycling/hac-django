from django.contrib import admin
from . import models

class AthleteAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Athlete, AthleteAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Category, CategoryAdmin)