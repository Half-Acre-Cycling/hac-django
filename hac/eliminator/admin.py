from django.contrib import admin
from . import models

class AthleteAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Athlete, AthleteAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Category, CategoryAdmin)

class RoundAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Round, RoundAdmin)

class RaceResultAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.RaceResult, RaceResultAdmin)

class RaceAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Race, RaceAdmin)
