"""QualityAssurance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path,include
from common import views
from application import views as application_views
urlpatterns = [
    path('eaa/login', views.Login.as_view()),
    re_path(r'^eaa/application/pending/(?P<applicant_id>\w{1,8})$',application_views.PendingList.as_view()),
    re_path(r'^eaa/application/myapply/(?P<applicant_id>\w{1,8})$',application_views.MyApply.as_view()),
    re_path(r'^eaa/application/all/(?P<applicant_id>\w{1,8})$',application_views.AllApply.as_view()),
    re_path(r'^eaa/application/add_apply$', application_views.Apply.as_view()),
    path('eaa/application/resource',application_views.ResourceList.as_view())
]
