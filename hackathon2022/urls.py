"""hackathon2022 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from main.views import *
urlpatterns = [
    path('payments',payments,name='payments'),
    path('customerhistory',customerhistory,name="customerhistory"),
    path('feedback',feedback,name="feedback"),
    path('ownerequest',ownerequest,name="ownerequest"),
    path('reqc',reqc,name="req"),
    path('reqp',reqp,name="reqp"),
    path('ownerhistory',ownerhistory,name="ownerhistory"),
    path('tocmrit',tocmrit,name="tocmrit"),
    path('tohome',tohome,name="tohome"),
    path('admin/', admin.site.urls),
    path('cregister',cregister,name="cregister"),
    path('chome',chome,name="chome"),
    path('clogin',clogin,name="clogin"),
    path('',index,name="index"),
    path('register',register,name="register"),
    path('home',home,name="home"),
    path('index',index,name="index"),
    path('vehicleDetails',vehicleDetails,name="vehicleDetails"),
    path('otrip',otrip,name="otrip"),
    path('login',login,name="login"),
]
