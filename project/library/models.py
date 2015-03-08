from django.db import models
from django.db.models import Model

from mptt.models import MPTTModel, TreeForeignKey


class Folder(MPTTModel):
    """Library folder (topic). Can be nested and each level can contain documents."""

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

    class Meta:
        unique_together = [['slug', 'parent'], ['title', 'parent']]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """URL is derived from pre-calculated path."""

        return "/library/" + self.path + "/"

    def save(self, *args, **kwargs):
        """Save, updating slugs of our descendant folders and documents."""

        def _get_path(obj):
            """Returns path to folder from top of library, eg 'folder-a/folder-b/folder-c'."""
            return ("/".join(a.slug for a in obj.get_ancestors()) + "/" + obj.slug).strip('/')

        update_descendants = False
        add_path_after_save = False

        if self.pk:
            # since we already exist, find out if out path changed
            new_path = _get_path(self)
            if self.path != new_path:
                # our path changed, so save the new path, and we'll fix descendants after our save
                self.path = new_path
                update_descendants = True
        else:
            # we're not in database, so save, then fix up the path
            add_path_after_save = True

        super(Folder, self).save(*args, **kwargs)

        if update_descendants:
            # our path changed, so the paths of all the folders/documents under us must change

            # update our documents:
            for doc in self.documents.all():
                doc.path = self.path + "/" + doc.slug
                doc.save(update_fields=['path'])

            # update our descendants (& their documents)
            for subfolder in self.get_descendants():
                subfolder.path = _get_path(subfolder)
                subfolder.save(update_fields=['path'])
                for doc in subfolder.documents.all():
                    doc.path = subfolder.path + "/" + doc.slug
                    doc.save(update_fields=['path'])

        if add_path_after_save:
            # We were being added for first time, so we can only get our ancenstors after
            # we're saved. Now we can add our path.
            self.path = _get_path(self)
            super(Folder, self).save(*args, **kwargs)


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

    class Meta:
        unique_together = [['slug', 'folder'], ['title', 'folder']]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """URL is derived from parent folder's path."""

        return "/library/" + self.path + "/"

    def save(self, *args, **kwargs):
        """Update path on save."""

        self.path = self.folder.path + "/" + self.slug
        super(Document, self).save(*args, **kwargs)
