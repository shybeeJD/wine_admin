from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
import json
from django.views.decorators.csrf import csrf_exempt

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

def uploadPics(request):
    imgs=request.FILES.getlist('fileList')
    for img in imgs:
        with open(img.name,"wb") as f:
            for c in img.chunks():
                f.write()
    return JsonResponse({
        "success":True
    })

def createWine(request):

    pass

def acceptOrder(request):
    _id=request.GET.get('_id')
    ACCESS_TOKEN = getAccessToken()
    url = f'https://api.weixin.qq.com/tcb/databaseupdate?access_token={ACCESS_TOKEN}'
    query = "db.collection('order').where({'_id':'%s'}).update({'data':{'status':3}})" % (_id)
    data = {
        "env": settings.ENV,
        "query": query
    }
    res = requests.post(url, data=json.dumps(data))
    return JsonResponse(res.json())
def refuseOrder(request):
    _id = request.GET.get('_id')
    if _id:
        ACCESS_TOKEN = getAccessToken()
        url = f'https://api.weixin.qq.com/tcb/invokecloudfunction?access_token={ACCESS_TOKEN}&env={settings.ENV}&name=quickstartFunctions'


        data = {
            "type": "refuseOrder",
            "_id":_id
        }
        res = requests.post(url, data=json.dumps(data))
        return JsonResponse(res.json())
    return JsonResponse({'success':False,'msg':'no _id'})
def getNewOrder(request):
    ACCESS_TOKEN = getAccessToken()
    limit=request.GET.get('limit')
    offset=request.GET.get('offset')
    url = f'https://api.weixin.qq.com/tcb/invokecloudfunction?access_token={ACCESS_TOKEN}&env={settings.ENV}&name=quickstartFunctions'
    query = "db.collection('order').where({status:5}).get()"

    data = {
        "type": "updateStatus"
    }
    res = requests.post(url, data=json.dumps(data))
    print(res.json())

    url = f'https://api.weixin.qq.com/tcb/databasequery?access_token={ACCESS_TOKEN}'
    query = "db.collection('order').where({status:5}).get()"

    data = {
        "env": settings.ENV,
        "query": query
    }

    res = requests.post(url, data=json.dumps(data))
    return JsonResponse(res.json())

def getAllWines(request):
    ACCESS_TOKEN = getAccessToken()
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    category_name=request.GET.get('category_name')
    if  limit==None:
        limit=10
    if  offset==None:
        offset=0

    url = f'https://api.weixin.qq.com/tcb/databasequery?access_token={ACCESS_TOKEN}'
    if category_name:
        query = "db.collection('wine').where({category_name:'%s'}).limit(%d).skip(%d).get()"%(category_name,int(limit),int(offset))
    else:
        query = "db.collection('wine').limit(%d).skip(%d).get()" % (int(limit),int(offset))

    data = {
        "env": settings.ENV,
        "query": query
    }

    res = requests.post(url, data=json.dumps(data))
    return JsonResponse(res.json())
def getAllOrders(request):
    ACCESS_TOKEN = getAccessToken()
    limit = request.GET.get('limit')
    offset = request.GET.get('offset')
    status =request.GET.get('status')
    if  limit==None:
        limit=10
    if  offset==None:
        offset=0

    url = f'https://api.weixin.qq.com/tcb/databasequery?access_token={ACCESS_TOKEN}'
    if status:
        query = "db.collection('order').where({status:%d}).limit(%d).skip(%d).get()"%(int(status),int(limit),int(offset))
    else:
        query = "db.collection('order').limit(%d).skip(%d).get()" % (int(limit),int(offset))

    data = {
        "env": settings.ENV,
        "query": query
    }

    res = requests.post(url, data=json.dumps(data))
    return JsonResponse(res.json())

def changeStocks(request):
    _id = request.GET.get('_id')
    stock=request.GET.get('stock')
    ACCESS_TOKEN = getAccessToken()
    url = f'https://api.weixin.qq.com/tcb/databaseupdate?access_token={ACCESS_TOKEN}'
    query = "db.collection('wine').where({'_id':'%s'}).update({'data':{'stock':%d}})" % (_id,int(stock))
    data = {
        "env": settings.ENV,
        "query": query
    }
    res = requests.post(url, data=json.dumps(data))
    return JsonResponse(res.json())

def getAddress(request):
    address = request.GET.get('address')
    if address:
        ACCESS_TOKEN = getAccessToken()
        url = f'https://api.weixin.qq.com/tcb/databasequery?access_token={ACCESS_TOKEN}'
        query = "db.collection('address').where({_id:'%s'}).get()"%(address)
        data = {
            "env": settings.ENV,
            "query": query
        }
        res = requests.post(url, data=json.dumps(data))
        return JsonResponse(res.json())

    return JsonResponse({'success':False,'msg':'no address'})

def getShops(request):
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    ACCESS_TOKEN = getAccessToken()
    if  limit==None:
        limit=10
    if  offset==None:
        offset=0
    print(offset,limit)
    url = f'https://api.weixin.qq.com/tcb/databasequery?access_token={ACCESS_TOKEN}'

    query = "db.collection('shop').limit(%d).skip(%d).get()" % (int(limit), int(offset))

    data = {
        "env": settings.ENV,
        "query": query
    }

    res = requests.post(url, data=json.dumps(data))
    return JsonResponse(res.json())
def getOrders(request):
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    status = request.GET.get('status')
    ACCESS_TOKEN = getAccessToken()
    if limit == None:
        limit = 10
    if offset == None:
        offset = 0
    url = f'https://api.weixin.qq.com/tcb/databasequery?access_token={ACCESS_TOKEN}'
    if(status):
        query = "db.collection('order').where({status:%d}).limit(%d).skip(%d).get()" % (
        int(status), int(limit), int(offset))
    else:

        query = "db.collection('order').limit(%d).skip(%d).get()" % (int(limit), int(offset))

    data = {
        "env": settings.ENV,
        "query": query
    }
    res = requests.post(url, data=json.dumps(data))
    return JsonResponse(res.json())
@csrf_exempt
def updateShop(request):
    print(request.POST)
    data=(json.loads(request.body))
    data=json.loads(data)
    print(data)
    if id not in data:
        data['id']=None
    req={
        '_id':data['id'],
        'name':data['name'],
        'freight':data['freight'],
        'category':data['category'],
        'longitude':(data['mapData'][0][0]),
        'latitude':(data['mapData'][0][1]),
        'address':data['mapData'][1],
        'maxrange':data['max_range']

    }
    print(req)
    ACCESS_TOKEN = getAccessToken()
    url = f'https://api.weixin.qq.com/tcb/invokecloudfunction?access_token={ACCESS_TOKEN}&env={settings.ENV}&name=quickstartFunctions'

    data = {
        "type": "createShop"
    }
    req['type']="createShop"
    res = requests.post(url, data=json.dumps(req))
    print(res.json())

    return JsonResponse(res.json())

@csrf_exempt
def uploadpics(request):
    for key in request.FILES:
        print(key)

    file=request.FILES.get('file')
    if not file:
        return JsonResponse({'success':False})
    f= open('pic/'+file.name,'wb+')
    for chunk in file.chunks():
        f.write(chunk)
    f.close()

    return JsonResponse({'success':True,'name':file.name})