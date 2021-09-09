from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import datetime

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
@csrf_exempt
def createWine(request):
    data = (json.loads(request.body))
    data = json.loads(data)
    brand= data['brand'] if 'brand' in data else ""
    category_name = data['category_name'] if 'category' in data else ""
    degrees = data['degrees'] if 'degrees' in data else ""
    isShowHP = data['isShowHP'] if 'isShowHP' in data else False
    capacity = data['capacity'] if 'capacity' in data else ""
    item = data['item'] if 'item' in data else ""
    marketPrice = data['marketPrice'] if 'marketPrice' in data else 0
    origin = data['origin'] if 'origin' in data else ""
    packingsPrice = data['packingsPrice'] if 'packingsPrice' in data else 0
    pic_array1 = data['pic_array1'] if 'pic_array1' in data else []
    pic_array2 = data['pic_array2'] if 'pic_array2' in data else []
    price = data['price'] if 'price' in data else 0
    sale_count = data['sale_count'] if 'sale_count' in data else 0
    shop = data['shop'] if 'shop' in data else ""
    stock = int(data['stock']) if 'stock' in data else 0
    thumb_url = data['thumb_url'] if 'thumb_url' in data else ""
    title = data['title'] if 'title' in data else ""


    req={
        'brand':brand,
        'category_name':category_name,
        'marketPrice':marketPrice,
        'item':item,
        'origin':origin,
        'packingsPrice':packingsPrice,
        'pic_array':pic_array1,
        'product_desc_url':pic_array2,
        'price':price,
        'shop':shop,
        'specification':degrees+'度，'+capacity+'mL',
        'stock':stock,
        'thumb_url':thumb_url,
        'title':title,
        'recommend':isShowHP

    }
    ACCESS_TOKEN = getAccessToken()
    url = f'https://api.weixin.qq.com/tcb/invokecloudfunction?access_token={ACCESS_TOKEN}&env={settings.ENV}&name=quickstartFunctions'

    req['type'] = "createWine"
    print(req)
    res = requests.post(url, data=json.dumps(req))
    print(res.json())

    return JsonResponse(res.json())


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

@csrf_exempt
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
    uploadname = file.name
    f= open('pic/'+file.name,'wb+')
    for chunk in file.chunks():
        f.write(chunk)
    f.close()
    ACCESS_TOKEN = getAccessToken()
    time = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    img_url = 'pic/'+file.name  # 待上传的文件
    url1 = 'https://api.weixin.qq.com/tcb/uploadfile?access_token=' + ACCESS_TOKEN
    data = {
        "env": settings.ENV,
        "path": 'pic/' + time + '.' + img_url.split('.')[-1]  # 保证相同的文件格式
    }
    res = requests.post(url1, data=json.dumps(data)).json()
    print(res)
    file = {"file": open(img_url, "rb")}
    data = {
        'key': 'pic/' + time + '.' + img_url.split('.')[-1],
        'Signature': res['authorization'],
        'x-cos-security-token': res['token'],
        'x-cos-meta-fileid': res['cos_file_id']
    }
    res2=requests.post(res['url'], data=data, files=file)
    print(res2)
    return JsonResponse({'success':True,'name':res['file_id']})
def deletePic(request):
    pic=request.GET.get('pic')
    ACCESS_TOKEN = getAccessToken()
    print(pic)
    url=f'https://api.weixin.qq.com/tcb/batchdeletefile?access_token={ACCESS_TOKEN}'
    data={
        "env": settings.ENV,
        "fileid_list":[pic]
    }
    res = requests.post(url, data=json.dumps(data)).json()
    return JsonResponse(res)

def showPic(request):
    pic=request.GET.getlist('pic')
    respPic = []

    for item in pic:
        respPic.append({'fileid': item, 'max_age': 7200})
    ACCESS_TOKEN = getAccessToken()
    url = f'https://api.weixin.qq.com/tcb/batchdownloadfile?access_token={ACCESS_TOKEN}'
    data2 = {
        "env": settings.ENV,
        "file_list": respPic
    }
    res = requests.post(url, data=json.dumps(data2)).json()
    return JsonResponse(res)