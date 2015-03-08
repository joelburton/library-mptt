from django.db import models
from django.db.models import Model

from mptt.models import MPTTModel, TreeForeignKey


class Folder(MPTTModel):
    """Folder in library. Acts like a topic. Can be nested and each level can contain documents."""
    slug = models.SlugField(
        max_length=50,
    )

    title = models.CharField(
        max_length=50,
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children'
    )

    # Keep a pre-calculated path to this folder for fast URL-generation and URL lookup
    path = models.CharField(
        max_length=254,
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """URL is derived from pre-calculated path."""

        return "/library/" + self.path + "/"

    def save(self, *args, **kwargs):
        """Save, updating slugs of our descendant folders and documents."""

        new_path = "/".join(a.slug for a in self.get_ancestors()) + "/" + self.slug

        if self.path != new_path:
            # our slug must have changed
            self.path = new_path
            update_descendants = True
        else:
            update_descendants = False

        super(Folder, self).save(*args, **kwargs)

        if update_descendants:
            for i in self.get_descendants():
                i.path = "/".join(a.slug for a in self.get_ancestors(include_self=True))
                i.save(update_fields=['path'])
                for d in i.documents.all():
                    d.path = i.path + "/" + d.slug
                    d.save(update_fields=['path'])


class Document(Model):
    """Document in library. Stored inside of a folder."""

    slug = models.SlugField(
        max_length=50,
    )

    title = models.CharField(
        max_length=50,
    )

    folder = TreeForeignKey(
        Folder,
        related_name='documents'
    )

    # Keep a pre-calculated path to this document for fast URL-generation and URL lookup
    path = models.CharField(
        max_length=254,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """URL is derived from parent folder's path."""

        return "/library/" + self.path + "/"

    def save(self, *args, **kwargs):
        """Update path on save."""

        self.path = self.folder.path + "/" + self.slug
        super(Document, self).save(*args, **kwargs)
