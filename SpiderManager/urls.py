#! /usr/bin/python
# -*- coding:utf-8 -*-
"""SpiderManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.conf.urls import handler404, handler500
from django.contrib import admin

from django.views.generic import RedirectView
import route.mainroute as route
handler404 = "nmaptoolbackground.nmaproute.page_not_found"
handler500 = "nmaptoolbackground.nmaproute.page_error"

urlpatterns = [
    url(r'^', include('nmaptoolbackground.urls', namespace='nmaptool')),
    url(r'^admin/', admin.site.urls),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^status/$', route.indexpage, name='status'),
    url(r'^testdata/$', route.testdata, name='testdata'),
    # 注意include前没有$符号，而是以/结尾
    url(r'^nmaptool/', include('nmaptoolbackground.urls', namespace='nmaptool')),
    url(r'^fontsearch/', include('fontsearch.urls', namespace='fontsearch')),
]
