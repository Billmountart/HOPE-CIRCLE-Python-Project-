"""
URL configuration for ngo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from ngoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('ngoReg',views.ngoReg),
    path('volReg',views.volReg),
    path('donReg',views.donReg),
    path('login',views.login),
    path('blog',views.blog),


    path('adminHome',views.adminHome),
    path('adminngo',views.adminngo),
    path('adminvol',views.adminvol),
    path('admindon',views.admindon),
    path('adminOpen',views.adminOpen),
    path('adminActive',views.adminActive),
    path('adminActiveVol',views.adminActiveVol),
    path('adminActiveDon',views.adminActiveDon),
    path('adminActivity',views.adminActivity),
    path('adminActVol',views.adminActVol),
    path('adminActDon',views.adminActDon),
    path('adminChat',views.adminChat),
    path('adminBlog',views.adminBlog),
    path('blogDelet',views.blogDelet),
    path('adminReport',views.adminReport),


    path('ngoHome',views.ngoHome),
    path('ngoActivity',views.ngoActivity),
    path('ngoVolRequest',views.ngoVolRequest),
    path('ngoAcceptVol',views.ngoAcceptVol),
    path('ngoDonations',views.ngoDonations),
    path('ngoBlog',views.ngoBlog),


    path('volunteerHome',views.volunteerHome),
    path('volActivity',views.volActivity),
    path('volRequest',views.volRequest),
    path('volApplied',views.volApplied),
    path('VolSubscribe',views.VolSubscribe),
    path('volChat',views.volChat),
    path('volSub',views.volSub),
    path('chatbot-response/', views.chatbot_response, name='chatbot-response'),
    
    path('donorHome',views.donorHome),
    path('donEvents',views.donEvents),
    path('DonSubscribe',views.DonSubscribe),
    path('donConfirm',views.donConfirm),
    path('donHistory',views.donHistory),
    path('donReciept',views.donReciept),
    path('donSub',views.donSub),
    path('payment',views.payment),

]

