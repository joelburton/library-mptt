from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Folder, Document


class FolderListView(generic.ListView):
    model = Folder


class FolderDetailView(generic.DetailView):
    model = Folder


class DocumentDetailView(generic.DetailView):
    model = Document

    def get_context_data(self, **kwargs):
        """Drilldown relies on the folder being called 'folder' in the context"""

        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['folder'] = self.object.folder
        return context


def library_traverse(request, path):
    elems = path.strip('/').split('/')
    first, rest = elems[0], elems[1:]
    child = get_object_or_404(Folder, slug=first)
    for elem in rest:
        try:
            child = Folder.objects.get(slug=elem, parent=child)
        except Folder.DoesNotExist:
            doc = get_object_or_404(Document, slug=elem, folder=child)
            return document_detail_view(request, pk=doc.id)

    return folder_detail_view(request, pk=child.id)

folder_detail_view = FolderDetailView.as_view()
document_detail_view = DocumentDetailView.as_view()
