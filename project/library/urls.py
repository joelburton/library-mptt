from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.FolderListView.as_view(), name='folder_list'),

    # THis should come last, as it captures everything else. It's used to traverse into the
    # library using the paths of folder/documents.
    url(r'^(?P<path>.+)/$', views.library_traverse),
]
