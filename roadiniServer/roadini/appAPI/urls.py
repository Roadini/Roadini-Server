from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pathsTable', views.PathsTableView)

urlpatterns = [
        path('',include(router.urls)),
        path('feed/<int:user_id>', views.feed, name='feed'),
        path('postImage', views.save_on_cdn, name='save_on_cdn'),
        path('discoverPlace', views.discover_place, name='discover_place'),
        path('logout/<int:user_id>', views.logout, name='logout'),
        path('editImage', views.edit_image, name='edit_image'),
        
        #GEO URLS
        path('magicRoute/<int:user_id>/<str:lat>/<str:lng>', views.magic_route, name='magic_route'),
        path('changeMagic/<str:lat>/<str:lng>/<str:place_id>', views.change_magic, name='change_magic'),
        path('personalTrips', views.personalTrips, name='personalTrips'),
        path('ownLists/<int:user_id>', views.get_user_lists, name='get_user_lists'),
        path('createList', views.create_list, name='create_list'),
        path('nearPlaces/<str:lat>/<str:lng>', views.near_places, name='near_places'),
        path('listName/<int:user_id>', views.list_name, name='list_name'),
        path('addItem', views.add_item_list, name='add_item_list'),


        #AUTH
        path('createUser', views.create_user, name='create_user'),
        path('userInfo/<int:user_id>/<int:other_id>', views.user_info, name='user_info'),
        path('search/<int:user_id>/<str:pattern>', views.search, name='search'),
        path('follow/<int:user_id>/<int:other_id>', views.follow, name='follow'),
        path('unfollow/<int:user_id>/<int:other_id>', views.unfollow, name='unfollow'),
        path('saveRoute/<int:user_id>', views.add_route_to_feed, name='add_route_to_feed'),

]
