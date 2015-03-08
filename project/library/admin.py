from django.contrib import admin
from django.contrib.admin import ModelAdmin
from mptt.admin import MPTTModelAdmin

from .models import Folder, Document


@admin.register(Folder)
class FolderAdmin(MPTTModelAdmin):
    exclude = ['path']
    prepopulated_fields = {"slug": ("title",)}
    mptt_level_indent = 20


@admin.register(Document)
class DocumentAdmin(ModelAdmin):
    exclude = ['path']
    prepopulated_fields = {"slug": ("title",)}
