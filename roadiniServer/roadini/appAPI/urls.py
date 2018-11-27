from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pathsTable', views.PathsTableView)

urlpatterns = [
        path('',include(router.urls)),
        path('feed', views.feed, name='feed'),
        path('postImage', views.save_on_cdn, name='save_on_cdn'),
        
        #GEO URLS
        path('magicRoute', views.magic_route, name='magic_route'),
        path('personalTrips', views.personalTrips, name='personalTrips'),
        path('ownLists/<int:user_id>', views.get_user_lists, name='get_user_lists'),
        path('createList', views.create_list, name='create_list'),
        path('nearPlaces', views.near_places, name='near_places'),
        path('listName/<int:user_id>', views.list_name, name='list_name'),
        path('addItem', views.add_item_list, name='add_item_list'),

        #AUTH
        path('createUser', views.create_user, name='create_user'),
        path('userInfo/<int:user_id>', views.user_info, name='user_info'),

]
