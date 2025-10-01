"""
URL configuration for studentresultmanagementsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from resultapp.views import *
from resultapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='home'),
    path('admin_login/',admin_login, name='admin_login'),
    path('admin_dashboard/',admin_dashboard, name='admin_dashboard'),
    path('create_class/',create_class, name='create_class'),
    path('admin_logout/',admin_logout, name='admin_logout'),
    path('manage_classes/',manage_classes, name='manage_classes'),
    path('edit_class/<int:class_id>/', views.edit_class, name='edit_class'),
    path('create_subject/',create_subject, name='create_subject'),
    path('manage_subject/',manage_subject, name='manage_subject'),
    path('edit_subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('add_subject_combination/',add_subject_combination, name='add_subject_combination'),
]
