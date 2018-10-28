from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('pathsTable', views.PathsTableView)

urlpatterns = [
        path('',include(router.urls)),
        path('feed_App', views.feed, name='feed_App')

]
