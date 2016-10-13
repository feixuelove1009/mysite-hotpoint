"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/', views.index),
    url(r'^register/', views.register),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^publish/', views.publish),
    url(r'^publish_text/', views.publish_text),
    url(r'^gain/', views.gain),
    url(r'^login_confirm/', views.login_confirm),
    url(r'^recommend/', views.recommend),
    url(r'^favorite/', views.favorite),
    url(r'^comment/', views.comment),
    url(r'^make_comment/', views.make_comment),
    url(r'^page/', views.page),
]
