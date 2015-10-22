"""quizext URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from .views import TestList, TestDetail, startquiz, question, results


urlpatterns = [
    url(r'^tests/$', TestList.as_view(), name='tests'),
    url(r'^tests/(?P<pk>[0-9]+)/$', TestDetail.as_view(), name='test_confirm'),
    url(r'^tests/(?P<pk>[0-9]+)/start/$', startquiz, name='startquiz'),
    url(r'^tests/(?P<pk>[0-9]+)/question/(?P<q_set>[0-9]+)/$', question, kwargs=attempt_count, name='question'),
    url(r'^tests/(?P<pk>[0-9]+)/results/$', results, name='results')
]