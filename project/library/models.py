from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Model
from mptt.models import MPTTModel, TreeForeignKey


class Folder(MPTTModel):
    slug = models.SlugField(
        max_length=50,
    )

    title = models.CharField(
        max_length=50,
        unique=True,
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/library/%s/" % "/".join(a.slug for a in self.get_ancestors(include_self=True))


class Document(Model):
    slug = models.SlugField(
        max_length=50,
    )

    title = models.CharField(
        max_length=50,
        unique=True,
    )

    folder = TreeForeignKey(
        Folder,
        related_name='documents'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "%s%s/" % (self.folder.get_absolute_url(), self.slug)