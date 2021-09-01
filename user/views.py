from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        redirectUrl=request.POST.get("redirectUrl")
        print(username,password)
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({"success":False})
        print(user.password)
        if user.password == password:
            request.session['is_login'] = True
            request.session['username'] = username
            print(request.session.session_key,1)
            if not request.session.session_key:
                request.session.save()
            return JsonResponse({'sessionid':request.session.session_key,'redirectUrl':redirectUrl})
    elif request.method == "GET":
        return JsonResponse({'redirectUrl':""})
    return JsonResponse({"success":False})
@csrf_exempt
def index(request):
    sessionid=request.GET.get('sessionid')

    print(request.session.keys())
    return JsonResponse({'pos':'index'})


def register(request):
    return HttpResponseRedirect('../index')
    pass



def logout(request):
    request.session.flush()
    return HttpResponseRedirect('login')
    pass


def change_password(request):
    pass