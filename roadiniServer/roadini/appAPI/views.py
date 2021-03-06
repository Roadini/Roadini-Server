from .models import ListPostPhoto
from .models import PathsTable
from .models import PostFeed
from .models import UserAuth

from .serializers import PathsTableSerializer

from django.db import IntegrityError
from django.http import JsonResponse # Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from random import randint
from rest_framework import viewsets

import base64
import datetime
import http.cookiejar
import json
import os
import requests
import time




class PathsTableView(viewsets.ModelViewSet):
    queryset = PathsTable.objects.all()
    serializer_class = PathsTableSerializer

def logout(request, user_id):
    user = UserAuth.objects.get(userId=user_id)
    jsonLoaded = {"jwt":user.cookie}
    response = requests.post('http://auth_api:3000/auth/v1/logout', cookies=jsonLoaded)
    status = False
    if(response.status_code==200):
        try:
            status = True
            user.cookie = ""
            user.save()
        except IntegrityError as e:
            print(e)
    
    json_response = {}
    json_response["status"] = status
    response = JsonResponse(json_response, content_type='application/json')
    return response

@csrf_exempt
def edit_image(request):
    headers = {'Content-type': 'application/json'}
    data = request.FILES.get("photos")
    files = {'file': data}
    r1 = requests.post('http://cdnapiv2:8080/api/v2/',files=files)
    json_response = {}
    status = False
    if(r1.status_code==201):
        print("AQUI")
        print((json.loads(r1.text)["result"]).split(" ")[2])
        imageId = (json.loads(r1.text)["result"]).split(" ")[2]
        try:
            imageUrl = "http://engserv1-aulas.ws.atnog.av.it.pt/cdnapiv2/api/v2/" + imageId
            print(imageUrl)
            user = UserAuth.objects.get(userId=request.POST["userId"])
            user.image = imageUrl
            user.save()
            status = True
        except IntegrityError as e:
            print(e)

    json_response["status"] = status
    response = JsonResponse(json_response, content_type='application/json')
    return response


def feed(request, user_id):
    user = UserAuth.objects.get(userId=user_id)
    jsonLoaded = {"jwt":user.cookie}
    allFeed = PostFeed.objects.all()
    posts = []
    
    allUsers = UserAuth.objects.all()

    for u in allUsers:
        jsonData = {}
        jsonData["getby"] = "id"
        jsonData["value"] = u.userId
        response2 = requests.post('http://auth_api:3000/auth/v1/getusers', cookies=jsonLoaded, data=json.dumps(jsonData))
        r2 = json.loads(response2.text)[0]
        print(r2)

        jsonData = {}
        jsonData["id"] = u.userId
        response = requests.post('http://auth_api:3000/social/v1/publication/get', cookies=jsonLoaded, data=json.dumps(jsonData))
        r = json.loads(response.text)
        if r != []:
            for f in r:
                print(f["id"])
                if(PostFeed.objects.filter(authId = f["id"]).exists()):

                    try:
                        feedObject = PostFeed.objects.get(authId = f["id"])

                        jsonPost = {}
                        jsonPost["username"] = r2["name"]
                        jsonPost["location"] = feedObject.post_time.strftime("%B %d, %Y")
                        jsonPost["description"] = r2["name"] + " " + f["description"]
                        jsonPost["postId"] = feedObject.authId
                        jsonPost["ownerId"] = u.userId
                        jsonPost["urlImage"] = feedObject.urlStatic
                        jsonPost["photo"] = u.image 
                        jsonPost["date"] = feedObject.post_time 

                        posts.append(jsonPost)
                    except IntegrityError as e:
                        print("AQUI")
                        print(e)
    posts.sort(key=lambda x: x["date"], reverse=True)
    feed = {"feed" : posts }


    response = JsonResponse(feed, content_type='application/json')
    return response



def personalTrips(request):

    trips = {"trips" :[ {"name" : "Tiago Ramalho", "location" : "Croacia", "description" : "Um dos destinos de praia queridinhos dos viajantes low-cost é a Croácia, famosa pelas praias paradisíacas e águas cristalinas com preços muito mais atrativos que a Grécia e Itália. Fizemos uma viagem de 7 dias cruzando o país todinho e separamos aqui o roteiro completinho pra vocês.", "postId" : 1, "ownerId" : 1, "stars" : 72, "urlImage" : "http://3.bp.blogspot.com/-TmtrrRFfyic/UwUEz55bHkI/AAAAAAAAHxE/zrWxzfiKL9s/s1600/Navigator-Split-Return_mapa.jpg" },
  {"username" : "Tiago Ramalho", "location" : "Londres", "description" : " Nosso roteiro de 3 em Londres começa pela Tower Bridge, ponte que se levanta para passagens de barcos grandes, e pela Torre de Londres, um castelo medieval que abriga, entre outras coisas, a jóias da Coroa. Siga até a Catedral de Saint Paul, onde foi realizado o casamento Príncipe Charles e a Princesa Diana.  Você pode entrar na Catedral pra ver as criptas, e subir até o Domo (que tem uma vista linda de Londres). Em tempo, o caminho da Torre de Londres para a Catedral é bem bonito, com construções tradicionalmente inglesas misturadas com arranha-céus modernos. Catedral visitada, atravesse a Millennium Bridge vá explorar o Borough Market,um mercado bem típico de Londres. Você pode almoçar aqui, inclusive.", "postId" : 2, "ownerId" : 1, "stars" : 125, "urlImage" : "https://minhasviagensedestinos.files.wordpress.com/2012/07/roteiro-londres.jpg" },
  {"username" : "Tiago Ramalho", "location" : "Barcelona", "description" : "Plaça de La Catedral: é onde fica a Catedral de Barcelona. É cheia de gente e animada a qualquer hora. a Plaça Reial, que fica próxima as Ramblas e é uma pedida para sair a noite. Anote que os arredores da Plaça Reial estão cheios de bons restaurantes para uma pausa pro almoço. Uma das indicações é o Los Caracoles, com pratos típicos catalões Els Quatre Gats: o bar inspirado no Le Chat Noir de Paris teve entre seus frequentadores Pablo Picasso e Antoni Gaudi. É um clássico, e que serve delicias ", "postId" : 3, "ownerId" : 1, "stars" :93, "urlImage" : "http://www.mundoemprosa.com.br/site/wp-content/uploads/2016/05/roteiro-barri-gotic.jpg" } ]}

    response = JsonResponse(trips, content_type='application/json')
    return response

##GEO

def magic_route(request,user_id, lat, lng):
    print(lat)
    print(lng)

    headers = {'Content-type': 'application/json'}
    r = requests.get('http://geoclust_api:3001/api/v1/magic?lat='+lat+"&lng="+lng+"&user="+str(user_id), headers=headers)
    print(r.status_code)
    print(r.text)
    if(r.status_code==200):
        json_response = {}
        json_data = json.loads(r.text) 
        list_magic = []
        for l in json_data["result"]:
            json_tmp = {}
            json_tmp["categoryName"] = l["primary_type"]
            json_tmp["placeName"] = l["name"]
            json_tmp["placeId"] = str(l["id"])
            json_tmp["placeDescription"] = l["address"]
            json_tmp["lat"] = l["lat"]
            json_tmp["lng"] = l["lng"]
            json_tmp["urlImage"] = "http://engserv1-aulas.ws.atnog.av.it.pt/geoclust/" + str(l["id"]) + ".jpeg"
            list_magic.append(json_tmp)

        route = {"route":list_magic}


    response = JsonResponse(route, content_type='application/json')
    return response
def change_magic(request, lat, lng, place_id):
    print(lat)
    print(lng)

    headers = {'Content-type': 'application/json'}
    r = requests.get('http://geoclust_api:3001/api/v1/magic/change?lat='+lat+"&lng="+lng+"&place_id="+place_id, headers=headers)
    if(r.status_code==200):
        print(r.text)
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
            json_tmp["urlImage"] = "http://engserv1-aulas.ws.atnog.av.it.pt/geoclust/" + str(l["id"]) + ".jpeg"
            list_magic.append(json_tmp)

        route = {"route":list_magic}
    print(r.status_code)


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
                            json_tmp1["urlImage"] = listIds.imageId
                        else:
                            json_tmp1["urlImage"] = "http://engserv1-aulas.ws.atnog.av.it.pt/geoclust/" + str(l1["internal_id_place"]) + ".jpeg"

                    list_items.append(json_tmp1)
            json_tmp["listItem"] = list_items
            list_lists.append(json_tmp)
        json_response["result"] = list_lists
        response = JsonResponse(json_response, content_type='application/json')
    return response

def near_places(request,lat, lng):
    print(lat)
    print(lng)

    headers = {'Content-type': 'application/json'}
    r = requests.get(' http://geoclust_api:3001/api/v1/gspots?lat='+lat+"&lng="+lng, headers=headers)
    print(r)
    print(r.text)
    if(r.status_code==200):
        json_response = {}
        json_data = json.loads(r.text) 
        json_response["listPlaces"] = json_data["result"]
        response = JsonResponse(json_response, content_type='application/json')
    response = JsonResponse(json_response, content_type='application/json')
    return response

def list_name(request, user_id):
    headers = {'Content-type': 'application/json'}
    r = requests.get('http://geoclust_api:3001/api/v1/lists/user/'+str(user_id), headers=headers)
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
    status = False
    if(r.status_code == 200):
        json_data = json.loads(r.text) 
        status = True
        json_data["status"]=status
        
    else:
        json_data = {"status":status}
    


    if(status):
        user = UserAuth.objects.get(userId=request.POST["userId"])
        jsonLoaded = {"jwt":user.cookie}
        jsonData = {}
        jsonData["description"] = "added a new item to personal list \" " + request.POST["listName"] + " \""
        response2 = requests.post('http://auth_api:3000/social/v1/publication/create', cookies=jsonLoaded, data=json.dumps(jsonData))
        r1 = json.loads(response2.text)
        if(response2.status_code == 200):
            try:
                date = datetime.datetime.now()
                PostFeed.objects.create(
                        userId=request.POST["userId"],
                        urlStatic="http://engserv1-aulas.ws.atnog.av.it.pt/geoclust/" + request.POST["itemId"] + ".jpeg",
                        post_time=date,
                        authId=r1["code"],
                        localsIds= "none",)
                status=True

            except IntegrityError as e:
                print(e)
    response = JsonResponse(json_data, content_type='application/json')
    return response


@csrf_exempt
def create_list(request):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    name = request.POST["name"];
    new_list = {"user_id":int(request.POST["user_id"]), "list_name":name}
    jsonData = json.dumps(new_list)
    r = requests.post('http://geoclust_api:3001/api/v1/lists', data=jsonData, headers=headers)
 
    if(r.status_code == 200):
        json_data = json.loads(r.text) 
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
    status = False
    if(r.status_code == 200):
        data = request.FILES.get("photos")
        files = {'file': data}
        r1 = requests.post('http://cdnapiv2:8080/api/v2/',files=files)
        print(r1)
        print(r1.text)

        if(r1.status_code==201):

            try:
                imageId = (json.loads(r1.text)["result"]).split(" ")[2]

                listIds = ListPostPhoto.objects.filter(listId=listId, postId=postId)
                if(listIds.exists()):
                    listIds = ListPostPhoto.objects.get(listId=listId, postId=postId)
                    listIds.imageId= 'http://engserv1-aulas.ws.atnog.av.it.pt/cdnapiv2/api/v2/' + imageId
                    listIds.save()

                else:
                    ListPostPhoto.objects.create(
                            listId=listId,
                            postId=postId,
                            imageId='http://engserv1-aulas.ws.atnog.av.it.pt/cdnapiv2/api/v2/' + imageId,
                            )
                status = True
                json_data = {"status":status}

            except IntegrityError as e:
                print(e)

    if(status):


        user = UserAuth.objects.get(userId=request.POST["userId"])
        jsonLoaded = {"jwt":user.cookie}
        jsonData = {}
        jsonData["description"] = "added a new item to personal list \" " + request.POST["listName"] + " \""
        response2 = requests.post('http://auth_api:3000/social/v1/publication/create', cookies=jsonLoaded, data=json.dumps(jsonData))
        r11 = json.loads(response2.text)
        if(response2.status_code == 200):
            try:

                date = datetime.datetime.now()
                PostFeed.objects.create(
                        userId=request.POST["userId"],
                        urlStatic='http://engserv1-aulas.ws.atnog.av.it.pt/cdnapiv2/api/v2/' + imageId,
                        post_time=date,
                        authId=r11["code"],
                        localsIds= "none",)
                status=True

            except IntegrityError as e:
                print(e)

    json_data = {"status":status}
    response = JsonResponse(json_data, content_type='application/json')
    return response

@csrf_exempt
def discover_place(request):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = request.FILES.get("photos")
    files = {'file': data}
    r1 = requests.post('http://imagerecognition:8080/api/v1/recognize/',files=files)
    if(r1.status_code==200):
        try:

            json_return = json.loads(r1.text)
            json_return["status"] =True
            response = JsonResponse(json_return, content_type='application/json')
            return response

        except IntegrityError as e:
            print(e)

    json_data = {"status":False}
    response = JsonResponse(json_data, content_type='application/json')
    return response

###AUTH
@csrf_exempt
def create_user(request):
    jwt = request.POST["cookie"][4:]
    jsonLoaded = {"jwt":jwt}
    response = requests.post('http://auth_api:3000/auth/v1/getselfuser', cookies=jsonLoaded)
    user = {}
    if(response.status_code):
        try:
            user = json.loads(response.text)[0]
            print(user["id"])

            if(UserAuth.objects.filter(userId=user["id"]).exists()):
                userExist = UserAuth.objects.get(userId=user["id"])
                userExist.cookie= jwt
                userExist.save()
            else:
                UserAuth.objects.create(
                        userId=user["id"],
                        cookie=jwt,
                        image= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRx-RKT_MyU2F4V6i3z2TIZ2Y_VNP3u7tkrPJvpQH5kFuj5-7XEiQ",
                        )
            user["status"]=True
            response = JsonResponse(user, content_type='application/json')
            return response
        except IntegrityError as e:
            print(e)
            user["status"]=False
            response = JsonResponse(user, content_type='application/json')
    else:
        user["status"]=False
        response = JsonResponse(user, content_type='application/json')
        return response

def user_info(request, user_id, other_id):
    status = False
    user = UserAuth.objects.get(userId=user_id)
    jsonLoaded = {"jwt":user.cookie}
    jsonData = {}
    jsonData["getby"] = "id"
    jsonData["value"] = other_id
    response = requests.post('http://auth_api:3000/auth/v1/getusers', cookies=jsonLoaded, data=json.dumps(jsonData))
    r = json.loads(response.text)[0]
    if(response.status_code == 200):
        status = True
        r['status'] = status
        try:
            user = UserAuth.objects.get(userId=other_id)
            print("IMAGE")
            print(type(user.image))
            print(user.image)
            r["urlImage"] = user.image
        except IntegrityError as e:
            print(e)


        jsonData={}
        jsonData["id"]=other_id
        response1 = requests.post('http://auth_api:3000/social/v1/follows/getfollowers', cookies=jsonLoaded, data=json.dumps(jsonData))
        r1 = json.loads(response1.text)
        if(response1.status_code == 200):
            r["followers"]= r1 if r1 != None else []
            response2 = requests.post('http://auth_api:3000/social/v1/follows/getfollowing', cookies=jsonLoaded, data=json.dumps(jsonData))
            r2 = json.loads(response2.text)
            if(response.status_code == 200):
                r["following"] = r2 if r2 != None else []

        response = JsonResponse(r, content_type='application/json')
        return response


def search(request, user_id, pattern):
    user = UserAuth.objects.get(userId=user_id)
    jsonLoaded = {"jwt":user.cookie}
    status = False
    response = requests.post('http://auth_api:3000/auth/v1/getallusers', cookies=jsonLoaded)
    r = json.loads(response.text)
    json_response = []
    if(response.status_code == 200):
        for l in r:
            if(l["name"].lower().find(pattern.lower())!= -1):
                newL = l
                jsonData = {}
                jsonData["id"]=l["id"]
                u = UserAuth.objects.get(userId=l["id"])
                response1 = requests.post('http://auth_api:3000/social/v1/follows/getfollowers', cookies=jsonLoaded, data=json.dumps(jsonData))
                r1 = json.loads(response1.text)
                print(u.image)
                newL["image"] = u.image
                if(response1.status_code == 200):
                    newL["followers"]= r1 if r1 != None else []
                    response2 = requests.post('http://auth_api:3000/social/v1/follows/getfollowing', cookies=jsonLoaded, data=json.dumps(jsonData))
                    r2 = json.loads(response2.text)
                    if(response.status_code == 200):
                        newL["following"] = r2 if r2 != None else []

                json_response.append(newL)
    json_return = {}
    json_return["allUsers"] = json_response
    response = JsonResponse(json_return, content_type='application/json')
    return response

def follow(request, user_id, other_id):
    user = UserAuth.objects.get(userId=user_id)
    jsonLoaded = {"jwt":user.cookie}
    jsonData = {}
    jsonData["id"] = other_id
    response = requests.post('http://auth_api:3000/social/v1/follows/follow', cookies=jsonLoaded, data=json.dumps(jsonData))
    r1 = json.loads(response.text)
    response = JsonResponse(r1, content_type='application/json')
    return response

def unfollow(request, user_id, other_id):
    user = UserAuth.objects.get(userId=user_id)
    jsonLoaded = {"jwt":user.cookie}
    jsonData = {}
    jsonData["id"] = other_id
    response = requests.post('http://auth_api:3000/social/v1/follows/stopfollowing', cookies=jsonLoaded, data=json.dumps(jsonData))
    r1 = json.loads(response.text)
    response = JsonResponse(r1, content_type='application/json')
    return response

@csrf_exempt
def add_route_to_feed(request, user_id):
    urlStatic = request.POST["urlStatic"]
    localsIds = request.POST["localsIds"]
    user = UserAuth.objects.get(userId=user_id)
    jsonLoaded = {"jwt":user.cookie}
    jsonData = {}
    jsonData["description"] = "added a new route for him"
    response = requests.post('http://auth_api:3000/social/v1/publication/create', cookies=jsonLoaded, data=json.dumps(jsonData))
    r1 = json.loads(response.text)
    print(r1)
    status = False
    try:
        date = datetime.datetime.now()
        PostFeed.objects.create(
                userId=user_id,
                urlStatic=urlStatic,
                post_time=date,
                authId=r1["code"],
                localsIds= localsIds,)
        status=True

    except IntegrityError as e:
        print(e)
    json_data = {"status":status}
    response = JsonResponse(json_data, content_type='application/json')
    print(json_data)
    return response
