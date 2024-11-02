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
    path('khonguyenlieu.html', home.Kho_nguyen_lieu, name='khonguyenlieu'),
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
    path('delete_dungcu/<str:madc>/', home.delete_dungcu, name='delete_dungcu'),
    path('delete_khonguyenlieu/<str:manl>/', home.delete_khonguyenlieu, name='delete_khonguyenlieu'),
    path('delete_bangluong/<str:maluong>/', home.delete_bangluong, name='delete_bangluong'),
    path('delete_nghiphep/<str:manp>/', home.delete_nghiphep, name='delete_nghiphep'),
    path('delete_calam/<str:macalam>/', home.delete_calam, name='delete_calam'),
    path('delete_thietbi/<str:matb>/', home.delete_thietbi, name='delete_thietbi'),
    path('delete_thongtinnguyenlieu/<str:manl>/', home.delete_thongtinnguyenlieu, name='delete_thongtinnguyenlieu'),
    path('delete_thongtinnhanvien/<str:manv>/', home.delete_thongtinnhanvien, name='delete_thongtinnhanvien'),
    path('sua_bangluong/<str:maluong>/', home.sua_bangluong, name='sua_bangluong'),
    path('sua_baotri/<str:mabt>/', home.sua_baotri, name='sua_baotri'),
    path('sua_dungcu/<str:madc>/', home.sua_dungcu, name='sua_dungcu'),
    path('sua_khonguyenlieu/<str:manl>/', home.sua_khonguyenlieu, name='sua_khonguyenlieu'),
    path('sua_nghiphep/<str:manp>/', home.sua_nghiphep, name='sua_nghiphep'),
    path('sua_calam/<str:macalam>/', home.sua_calam, name='sua_calam'),
    path('sua_thietbi/<str:matb>/', home.sua_thietbi, name='sua_thietbi'),
    path('sua_thongtinnguyenlieu/<str:manl>/', home.sua_thongtinnguyenlieu, name='sua_thongtinnguyenlieu'),
    path('sua_thongtinnhanvien/<str:manv>/', home.sua_thongtinnhanvien, name='sua_thongtinnhanvien'),
    path('search_thongtinnhanvin/', home.search_thongtinnhanvien, name='search_thongtinnhanvien'),

]
