from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pathsTable', views.PathsTableView)

urlpatterns = [
        path('',include(router.urls)),
        path('feed', views.feed, name='feed'),
        path('magicRoute', views.magicRoute, name='magicRoute'),
        path('personalTrips', views.personalTrips, name='personalTrips'),
        path('ownLists', views.get_user_lists, name='user_lists'),
        path('postImage', views.save_on_cdn, name='save_on_cdn'),
        path('createList', views.create_list, name='create_list'),
        path('nearPlaces', views.near_places, name='near_places'),
        path('listName/<int:user_id>', views.list_name, name='list_name'),
        path('addItem', views.add_item_list, name='add_item_list'),

]
