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

def magicRoute(request):

    route = {"route" : [ {"categoryName" : "Restaurant", "categoryId" : "1", "placeName" : "Azur", "placeId" : "23", "placeDescription" : "This superbly located newbie sits by the entrance of Buža II, and quickly went to number one on TripAdvisor in its very first season. Here you can tuck into a reasonably priced, Med-and-Asian-influenced main here – fragrant meatballs in a chicken-coconut broth, perhaps, or Adriatic prawn pouches on grilled aubergine in a red-curry-and-coconut sauce – before an afternoon's sunbathing or nightcap overlooking the waves. Starters include mussels in beer butter and chili, and Dalmatian tom yum soup.", "urlImage" : "https://media.timeout.com/images/102323695/380/285/image.jpg" },
  {"categoryName" : "Beaches", "categoryId" : "2", "placeName" : "Banje Beach", "placeId" : "40", "placeDescription" : "Located in the extreme south coast of Croatia, Dubrovnik is one the country’s top travel destinations, in part because of the city’s many beaches. Banja Beach, located to the east of the city’s Old Town district, is particularly popular. The pebble beach is surrounded by some of Dubrovnik’s best hotels and is equipped with all the amenities that upscale travelers expect, including deck chairs, umbrellas and ranging rooms equipped with showers. The beach favored by celebrities is a great in-town spot to enjoy water sports like jet skiing and paragliding too.", "urlImage" : "https://www.touropia.com/gfx/d/best-beaches-in-croatia/banje_beach.jpg?v=1" } ]}

    response = JsonResponse(route, content_type='application/json')
    return response


def personalTrips(request):

    trips = {"trips" :[ {"name" : "Tiago Ramalho", "location" : "Croacia", "description" : "Um dos destinos de praia queridinhos dos viajantes low-cost é a Croácia, famosa pelas praias paradisíacas e águas cristalinas com preços muito mais atrativos que a Grécia e Itália. Fizemos uma viagem de 7 dias cruzando o país todinho e separamos aqui o roteiro completinho pra vocês.", "postId" : 1, "ownerId" : 1, "stars" : 72, "urlImage" : "http://3.bp.blogspot.com/-TmtrrRFfyic/UwUEz55bHkI/AAAAAAAAHxE/zrWxzfiKL9s/s1600/Navigator-Split-Return_mapa.jpg" },
  {"username" : "Tiago Ramalho", "location" : "Londres", "description" : " Nosso roteiro de 3 em Londres começa pela Tower Bridge, ponte que se levanta para passagens de barcos grandes, e pela Torre de Londres, um castelo medieval que abriga, entre outras coisas, a jóias da Coroa. Siga até a Catedral de Saint Paul, onde foi realizado o casamento Príncipe Charles e a Princesa Diana.  Você pode entrar na Catedral pra ver as criptas, e subir até o Domo (que tem uma vista linda de Londres). Em tempo, o caminho da Torre de Londres para a Catedral é bem bonito, com construções tradicionalmente inglesas misturadas com arranha-céus modernos. Catedral visitada, atravesse a Millennium Bridge vá explorar o Borough Market,um mercado bem típico de Londres. Você pode almoçar aqui, inclusive.", "postId" : 2, "ownerId" : 1, "stars" : 125, "urlImage" : "https://minhasviagensedestinos.files.wordpress.com/2012/07/roteiro-londres.jpg" },
  {"username" : "Tiago Ramalho", "location" : "Barcelona", "description" : "Plaça de La Catedral: é onde fica a Catedral de Barcelona. É cheia de gente e animada a qualquer hora. a Plaça Reial, que fica próxima as Ramblas e é uma pedida para sair a noite. Anote que os arredores da Plaça Reial estão cheios de bons restaurantes para uma pausa pro almoço. Uma das indicações é o Los Caracoles, com pratos típicos catalões Els Quatre Gats: o bar inspirado no Le Chat Noir de Paris teve entre seus frequentadores Pablo Picasso e Antoni Gaudi. É um clássico, e que serve delicias ", "postId" : 3, "ownerId" : 1, "stars" :93, "urlImage" : "http://www.mundoemprosa.com.br/site/wp-content/uploads/2016/05/roteiro-barri-gotic.jpg" } ]}

    response = JsonResponse(trips, content_type='application/json')
    return response
