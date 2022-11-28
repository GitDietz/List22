from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views

from .views_list import (items_list, item_create,
                         list_detail, user_lists)

app_name = 'lists'

urlpatterns = [
    path('user_lists', user_lists, name='user_lists'),
    # path(group_remove_self/(?P<pk>\d+)', StockNoteCreateView.as_view(), name='note_create'),
    # path('note_update_ajax', note_update_ajax, name='note_update_ajax'),
    path('list_create', list_detail, name='list_create'),
    re_path(r'list_detail/(?P<pk>\d+)/(?P<list_obj>)', list_detail, name='list_detail'),

    re_path(r'item_create/(?P<pk>\d+)', item_create, name='item_create'),

    re_path('items_list/(?P<pk>\d+)', items_list, name='items_list'),
    ]
