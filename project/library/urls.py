from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.FolderListView.as_view(), name='folder_list'),
    url(r'^(?P<path>.+)$', views.library_traverse),
]
