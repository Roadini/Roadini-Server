from django.shortcuts import render
from rest_framework import viewsets
from .models import PathsTable
from .serializers import PathsTableSerializer


from django.http import JsonResponse
# Create your views here.

class PathsTableView(viewsets.ModelViewSet):
    queryset = PathsTable.objects.all()
    serializer_class = PathsTableSerializer


def feed(request):
    
    feed = {"feed" :[ {"username" : "Tiago Ramalho", "location" : "Croacia", "description" : "Esta viagem foi muito fixe", "postId" : "1", "ownerId" : "1", "urlImage" : "https://scontent.flis7-1.fna.fbcdn.net/v/t1.0-9/20258438_1893652067570862_4019107659665964412_n.jpg?_nc_cat=111&oh=b69b337a86923445d87ed7b445acd224&oe=5C4F4156" },
        {"username" : "Luís Silva", "location" : "Belgica", "description" : "Esta viagem foi muito fixe", "postId" : "1", "ownerId" : "2", "urlImage" : "https://scontent.flis7-1.fna.fbcdn.net/v/t31.0-8/23735995_1674280279312175_7527285910664902411_o.jpg?_nc_cat=100&oh=52a827ec4e8488cf3664c944853e0d1c&oe=5C4C4ADB"}]}

    response = JsonResponse(feed, content_type='application/json')
    return response
