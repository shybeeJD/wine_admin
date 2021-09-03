"""wine_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from wxcloud import views
from user import views as user_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login',user_views.login),
    path('user/logout', user_views.logout),
    path('index',user_views.index),
    path('user/register',user_views.register),
    path('api/test', views.getAccessToken),
    path('api/getAllTypes', views.getAllTypes),
    path('api/updateAllTypes',views.updateAllTypes),
    path('api/getNewOrder',views.getNewOrder),
    path('api/getAllWines',views.getAllWines),
    path('api/getAllOrders',views.getAllOrders),
    path('api/changeStocks',views.changeStocks),

]
