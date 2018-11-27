from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PathsTableSerializer

from random import randint
import requests
import http.cookiejar
import json
import os
import base64

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse # Create your views here.
from django.db import IntegrityError
from django.shortcuts import render_to_response

from .models import PathsTable
from .models import ListPostPhoto
from .models import UserAuth




class PathsTableView(viewsets.ModelViewSet):
    queryset = PathsTable.objects.all()
    serializer_class = PathsTableSerializer


def feed(request):
    
    feed = {"feed" :[ {"username" : "Tiago Ramalho", "location" : "Croacia", "description" : "Esta viagem foi muito fixe", "postId" : "1", "ownerId" : "1", "urlImage" : "https://scontent.flis7-1.fna.fbcdn.net/v/t1.0-9/20258438_1893652067570862_4019107659665964412_n.jpg?_nc_cat=111&oh=b69b337a86923445d87ed7b445acd224&oe=5C4F4156" },
        {"username" : "Luís Silva", "location" : "Belgica", "description" : "Esta viagem foi muito fixe", "postId" : "1", "ownerId" : "2", "urlImage" : "https://scontent.flis7-1.fna.fbcdn.net/v/t31.0-8/23735995_1674280279312175_7527285910664902411_o.jpg?_nc_cat=100&oh=52a827ec4e8488cf3664c944853e0d1c&oe=5C4C4ADB"}]}

    response = JsonResponse(feed, content_type='application/json')
    return response



def personalTrips(request):

    trips = {"trips" :[ {"name" : "Tiago Ramalho", "location" : "Croacia", "description" : "Um dos destinos de praia queridinhos dos viajantes low-cost é a Croácia, famosa pelas praias paradisíacas e águas cristalinas com preços muito mais atrativos que a Grécia e Itália. Fizemos uma viagem de 7 dias cruzando o país todinho e separamos aqui o roteiro completinho pra vocês.", "postId" : 1, "ownerId" : 1, "stars" : 72, "urlImage" : "http://3.bp.blogspot.com/-TmtrrRFfyic/UwUEz55bHkI/AAAAAAAAHxE/zrWxzfiKL9s/s1600/Navigator-Split-Return_mapa.jpg" },
  {"username" : "Tiago Ramalho", "location" : "Londres", "description" : " Nosso roteiro de 3 em Londres começa pela Tower Bridge, ponte que se levanta para passagens de barcos grandes, e pela Torre de Londres, um castelo medieval que abriga, entre outras coisas, a jóias da Coroa. Siga até a Catedral de Saint Paul, onde foi realizado o casamento Príncipe Charles e a Princesa Diana.  Você pode entrar na Catedral pra ver as criptas, e subir até o Domo (que tem uma vista linda de Londres). Em tempo, o caminho da Torre de Londres para a Catedral é bem bonito, com construções tradicionalmente inglesas misturadas com arranha-céus modernos. Catedral visitada, atravesse a Millennium Bridge vá explorar o Borough Market,um mercado bem típico de Londres. Você pode almoçar aqui, inclusive.", "postId" : 2, "ownerId" : 1, "stars" : 125, "urlImage" : "https://minhasviagensedestinos.files.wordpress.com/2012/07/roteiro-londres.jpg" },
  {"username" : "Tiago Ramalho", "location" : "Barcelona", "description" : "Plaça de La Catedral: é onde fica a Catedral de Barcelona. É cheia de gente e animada a qualquer hora. a Plaça Reial, que fica próxima as Ramblas e é uma pedida para sair a noite. Anote que os arredores da Plaça Reial estão cheios de bons restaurantes para uma pausa pro almoço. Uma das indicações é o Los Caracoles, com pratos típicos catalões Els Quatre Gats: o bar inspirado no Le Chat Noir de Paris teve entre seus frequentadores Pablo Picasso e Antoni Gaudi. É um clássico, e que serve delicias ", "postId" : 3, "ownerId" : 1, "stars" :93, "urlImage" : "http://www.mundoemprosa.com.br/site/wp-content/uploads/2016/05/roteiro-barri-gotic.jpg" } ]}

    response = JsonResponse(trips, content_type='application/json')
    return response

##GEO

def magic_route(request):

    headers = {'Content-type': 'application/json'}
    r = requests.get('http://geoclust_api:3001/api/v1/magic', headers=headers)
    if(r.status_code==200):
        json_response = {}
        json_data = json.loads(r.text) 
        list_magic = []
        for l in json_data["result"]:
            json_tmp = {}
            json_tmp["categoryName"] = l["primary_type"]
            json_tmp["placeName"] = l["name"]
            json_tmp["placeId"] = l["google_place_id"]
            json_tmp["placeDescription"] = l["address"]
            json_tmp["lat"] = l["lat"]
            json_tmp["lng"] = l["lng"]
            json_tmp["urlImage"] = "http://engserv-1-aulas.ws.atnog.av.it.pt/geoclust/" + str(l["id"]) + ".jpeg"
            list_magic.append(json_tmp)

        route = {"route":list_magic}


    response = JsonResponse(route, content_type='application/json')
    return response

def get_user_lists(request, user_id):
    headers = {'Content-type': 'application/json'}
    r = requests.get('http://geoclust_api:3001/api/v1/lists/user/' + str(user_id), headers=headers)
    if(r.status_code==200):
        json_response = {}
        json_data = json.loads(r.text) 
        list_lists = []
        for l in json_data["result"]:
            json_tmp = {}
            json_tmp["listName"] = l["list_name"]
            json_tmp["listId"] = l["id"]
            json_tmp["userId"] = l["user_id"]

            url1 = 'http://geoclust_api:3001/api/v1/visits/list/' + str(l["id"])
            r1 = requests.get(url1, headers=headers)
            list_items = []
            if(r1.status_code == 200):
                json_data1 = json.loads(r1.text)
                for l1 in json_data1["result"]:
                    json_tmp1 = {}
                    if(l1["review"] != ""):
                        description = l1["review"] 
                    else:
                        description = None 


                    url2 = 'http://geoclust_api:3001/api/v1/gspots/' + str(l1["internal_id_place"])
                    r2 = requests.get(url2, headers=headers)
                    if(r2.status_code == 200):
                        json_data2 = json.loads(r2.text)
                        l2 = json_data2["result"]
                        json_tmp1["location"] = l2["address"]
                        json_tmp1["name"] = l2["name"]
                        json_tmp1["listId"] = l["id"]
                        json_tmp1["stars"] = randint(0, 9)
                        json_tmp1["postId"] = l2["id"]
                        json_tmp1["description"] = description

                        if(ListPostPhoto.objects.filter(listId=l["id"], postId=l2["id"]).exists()):
                            listIds = ListPostPhoto.objects.get(listId=l["id"], postId=l2["id"])
                            url3 = 'http://cdnapi:8080/api/v1/user/' + listIds.imageId
                            r3 = requests.get(url3, headers=headers)
                            print(json.loads(r3.text)["url"])
                            print("EXISTE")
                            json_tmp1["urlImage"] = json.loads(r3.text)["url"]
                        else:
                            json_tmp1["urlImage"] = "http://engserv-1-aulas.ws.atnog.av.it.pt/geoclust/" + str(l1["internal_id_place"]) + ".jpeg"

                        print(json_tmp1)
                    list_items.append(json_tmp1)
            json_tmp["listItem"] = list_items
            list_lists.append(json_tmp)
        json_response["result"] = list_lists
        response = JsonResponse(json_response, content_type='application/json')
    return response

def near_places(request):
    headers = {'Content-type': 'application/json'}
    r = requests.get(' http://geoclust_api:3001/api/v1/gspots', headers=headers)
    if(r.status_code==200):
        json_response = {}
        json_data = json.loads(r.text) 


        json_response["listPlaces"] = json_data["result"]
        response = JsonResponse(json_response, content_type='application/json')
    response = JsonResponse(json_response, content_type='application/json')
    return response

def list_name(request, user_id):
    headers = {'Content-type': 'application/json'}
    r = requests.get('http://geoclust_api:3001/api/v1/lists/user/1', headers=headers)
    if(r.status_code==200):
        json_response = {}
        json_data = json.loads(r.text) 
        list_lists = []
        for l in json_data["result"]:
            json_tmp = {}
            json_tmp["listName"] = l["list_name"]
            json_tmp["listId"] = l["id"]
            json_tmp["userId"] = l["user_id"]
            list_lists.append(json_tmp)

        json_response["result"] = list_lists
        response = JsonResponse(json_response, content_type='application/json')
    return response

@csrf_exempt
def add_item_list(request):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    new_list = {"list_id":int(request.POST["listId"]), "internal_id_place":int(request.POST["itemId"]), "review": request.POST["review"]}
    jsonData = json.dumps(new_list)
    r = requests.post('http://geoclust_api:3001/api/v1/visits', data=jsonData, headers=headers)
    if(r.status_code == 200):
        json_data = json.loads(r.text) 
    else:
        json_data = {"status":False}
    
    response = JsonResponse(json_data, content_type='application/json')
    return response


@csrf_exempt
def create_list(request):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    name = request.POST["name"];
    new_list = {"user_id":1, "list_name":name}
    jsonData = json.dumps(new_list)
    r = requests.post('http://geoclust_api:3001/api/v1/lists', data=jsonData, headers=headers)
 
    if(r.status_code == 200):
        json_data = json.loads(r.text) 
        print(json_data)
    else:
        json_data = {"status":False}
        response = JsonResponse(json_data, content_type='application/json')
        return response
    response = JsonResponse(json_data, content_type='application/json')
    return response

##CDN

@csrf_exempt
def save_on_cdn(request):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    listId = int(request.POST["listId"])
    postId = int(request.POST["itemId"])
    new_list = {"list_id":listId, "internal_id_place":postId, "review": request.POST["review"]}
    jsonData = json.dumps(new_list)
    r = requests.post('http://geoclust_api:3001/api/v1/visits', data=jsonData, headers=headers)
    if(r.status_code == 200):
        data = request.FILES.get("photos")
        files = {'file': data}
        r1 = requests.post('http://cdnapi:8080/api/v1/user/',files=files)

        if(r1.status_code==201):

            try:

                listIds = ListPostPhoto.objects.filter(listId=listId, postId=postId)
                if(listIds.exists()):
                    listIds = ListPostPhoto.objects.get(listId=listId, postId=postId)
                    listIds.imageId= (json.loads(r1.text)["result"]).split(" ")[1]

                else:
                    ListPostPhoto.objects.create(
                            listId=listId,
                            postId=postId,
                            imageId=(json.loads(r1.text)["result"]).split(" ")[1],
                            )
                json_data = {"status":True}
                response = JsonResponse(json_data, content_type='application/json')
                return response
                listIds.save()

            except IntegrityError as e:
                print(e)

    json_data = {"status":False}
    response = JsonResponse(json_data, content_type='application/json')
    return response

###AUTH
@csrf_exempt
def create_user(request):
    jwt = request.POST["cookie"][4:]
    print(jwt)
    jsonLoaded = {"jwt":jwt}
    response = requests.post('http://auth_api:3000/auth/v1/getselfuser', cookies=jsonLoaded)
    user = {}
    if(response.status_code):
        try:
            user = json.loads(response.text)[0]

            if(UserAuth.objects.filter(userId=user["id"]).exists()):
                userExist = UserAuth.objects.get(userId=user["id"])
                userExist.cookie= jwt
            else:
                UserAuth.objects.create(
                        userId=user["id"],
                        cookie=jwt,
                        )
            user["status"]=True
            response = JsonResponse(user, content_type='application/json')
            return response
        except:
            user["status"]=False
            response = JsonResponse(user, content_type='application/json')
    else:
        user["status"]=False
        response = JsonResponse(user, content_type='application/json')
        return response

def user_info(request, user_id):
    user = UserAuth.objects.get(userId=user_id)
    jsonLoaded = {"jwt":user.cookie}
    followers = 0
    following = 0
    status = False
    response = requests.post('http://auth_api:3000/social/v1/follows/getfollowers', cookies=jsonLoaded)
    r = json.loads(response.text)
    print(r)
    if(response.status_code == 200):
        followers = r if r != None else 0
        response = requests.post('http://auth_api:3000/social/v1/follows/getfollowing', cookies=jsonLoaded)
        r = json.loads(response.text)
        if(response.status_code == 200):
            following = r if r != None else 0
            status = True

    json_response = {}
    json_response["followers"] = followers
    json_response["following"] = following
    json_response["status"] = status
    response = JsonResponse(json_response, content_type='application/json')
    return response





