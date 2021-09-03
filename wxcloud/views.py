from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
import json

def getAccessToken():

    url= f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={settings.APPID}&secret={settings.APPSECRET}'
    res=requests.get(url)
    print(res.text)
    return res.json()['access_token']



def login(request):
    pass




def getAllTypes(request):

    ACCESS_TOKEN=getAccessToken()
    url=f'https://api.weixin.qq.com/tcb/databasequery?access_token={ACCESS_TOKEN}'
    query = "db.collection('winTypes').get()"

    data={
        "env": settings.ENV,
        "query": query
    }

    res=requests.post(url,data=json.dumps(data))
    if res.json()['errcode']==0:
        types=res.json()['data'][0]
        types=json.loads(types)
        all_type=types["type"].split(',')
        resp={
            'errcode':0,
            'data':all_type
        }
        return JsonResponse(resp)


    return JsonResponse(res.json())


def updateAllTypes(request):
    ACCESS_TOKEN = getAccessToken()
    url=f'https://api.weixin.qq.com/tcb/databaseupdate?access_token={ACCESS_TOKEN}'
    types=request.GET.getlist('types')
    print(types)
    all_type=",".join(types)

    query = "db.collection('winTypes').where({'name':'type'}).update({'data':{'type':'%s'}})"%(all_type)
    print(query)

    data = {
        "env": settings.ENV,
        "query": query
    }

    res = requests.post(url, data=json.dumps(data))
    return JsonResponse(res.json())
    #return JsonResponse({"test":'1'})
