from django.contrib import admin
from django.contrib.admin import ModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import Folder, Document


admin.site.register(Folder, MPTTModelAdmin)

admin.site.register(Document, ModelAdmin)