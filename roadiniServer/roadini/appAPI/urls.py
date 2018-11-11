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

]
