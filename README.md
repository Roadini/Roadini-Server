# Roadini Server

Roadini server, developed in Django, joins all services created by roadini team and give the contents to roadini application. 

## Development

Build image from docker file

```
docker build . -tag=roadini_api
```

The composer create the docker network:
```
roadiniserver_proxynet
```

Finnaly
```
docker-compose up -d
```
