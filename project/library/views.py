from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Folder, Document


class FolderListView(generic.ListView):
    """View of library."""

    model = Folder


class FolderDetailView(generic.DetailView):
    """View of an individual folder."""

    model = Folder

# pre-generate this so we can use it in library_traverse
folder_detail_view = FolderDetailView.as_view()


class DocumentDetailView(generic.DetailView):
    """View of an individual document."""

    model = Document

    def get_context_data(self, **kwargs):
        """Drilldown relies on the folder being called 'folder' in the context"""

        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['folder'] = self.object.folder
        return context

# pre-generate this so we can use it in library_traverse
document_detail_view = DocumentDetailView.as_view()


def library_traverse(request, path):
    """View that traverses to correct folder/document.

    This view turns a path like 'folder-a/folder-b/document' into the end document-view, and a path
    like 'folder-a/folder-b' into the end folder-view.
    """

    try:
        folder = Folder.objects.get(path=path)
        return folder_detail_view(request, pk=folder.id)
    except Folder.DoesNotExist:
        doc = get_object_or_404(Document, path=path)
        return document_detail_view(request, pk=doc.id)

