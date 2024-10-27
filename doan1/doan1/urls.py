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
    path('thongtinnhanvien.html', home.nhan_vien, name='thongtinnhanvien'),
    path('luongnhanvien.html', home.bang_luong, name='bangluong'),
    path('socalam.html', home.so_ca_lam, name='socalam'),
    path('dungcu.html', home.Dung_cu, name='dungcu'), 
    path('nghiphep.html', home.nghi_phep, name='nghiphep'),
    path('thietbi.html', home.thiet_bi, name='thietbi'),
    path('baotri.html', home.Bao_tri, name='baotri'),
    path('thongtinnguyenlieu.html', home.Nguyen_lieu, name='thongtinnguyenlieu'),
    path('khonguyenlieu.html', home.Kho_nguyen_lieu),
    path('nhap_calam/', home.nhap_calam, name='nhap_calam'),
    path('trangcanhan.html', home.get_trangcanhan),
    path('socalam.html/import', home.import_excel_calam, name='socalam.html/import'),
    path('baotri.html/import', home.import_excel_baotri, name='baotri.html/import'),
    path('dungcu.html/import', home.import_excel_dungcu, name='dungcu.html'),
    path('luongnhanvien.html/import', home.import_excel_bangluong, name='bangluong.html/import'),
    path('nghiphep.html/import', home.import_excel_nghiphep, name='nghiphep.html/import'),
    path('thietbi.html/import', home.import_excel_thietbi, name='thietbi.html/import'),
    path('thongtinnguyenlieu.html/import', home.import_excel_thongtinnguyenlieu, name='thongtinnguyenlieu.html/import'),
    path('thongtinnhanvien.html/import', home.import_excel_thongtinnhanvien, name='thongtinnhanvien.html/import'),
    path('delete_baotri/<str:mabt>/', home.delete_baotri, name='delete_baotri'),
]
