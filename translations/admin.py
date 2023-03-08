from django.contrib import admin

from translations import models

admin.site.register(models.Language)
admin.site.register(models.Project)
admin.site.register(models.Section)
admin.site.register(models.Record)
admin.site.register(models.RecordValue)
