"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^entrytask/', include('entrytask.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from entrytask import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login', views.login),
    url(r'^admin/', admin.site.urls),
    url(r'^user', views.user),
    url(r'^files', views.files),
    url(r'^image/$', views.my_image),
]

