"""scraping URL Configuration

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
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from raspagem import views

urlpatterns = [
    url(r'^$',views.index,name='ind'),
    url(r'^questao1/$',views.questao_um, name='questao1'),
    url(r'^questao2/$', views.questao_dois, name='questao2'),
    url(r'^questao3/$', views.questao_tres, name = 'questao3'),
    url(r'^questao4/$', views.questao_quatro, name = 'questao4'),
    url(r'^questao5/$', views.questao_cinco, name = 'questao5'),
    url(r'^questao6/$', views.questao_seis, name = 'questao6'),

]
