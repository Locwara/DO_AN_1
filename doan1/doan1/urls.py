"""doan1 URL Configuration

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
from home import views as home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.get_index),
    path('dangnhap.html', home.get_dangnhap),
    path('trangchu.html', home.get_trangchu),
    path('thongtinnhanvien.html', home.get_thongtinnhanvien),
    path('luongnhanvien.html', home.get_luongnhanvien),
    path('socalam.html', home.get_socalam),
    path('dungcu.html', home.get_dungcu)
]
