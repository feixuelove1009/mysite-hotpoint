from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.Picture)