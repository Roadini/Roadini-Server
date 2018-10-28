from rest_framework import serializers
from .models import PathsTable

class PathsTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathsTable
        fields = ('socialID','pathID')

