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

]
