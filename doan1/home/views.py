from django.shortcuts import render
from .models import Calam
from .models import Nghiphep
from .models import bangluong
# Create your views here.
def get_index(request):
    return render(request, 'home/index.html')
def get_dangnhap(request):
    return render(request, 'home/dangnhap.html')
def get_trangchu(request):
    return render(request, 'home/trangchu.html')
def get_thongtinnhanvien(request):
    return render(request, 'home/thongtinnhanvien.html')
def get_luongnhanvien(request):
    return render (request, 'home/luongnhanvien.html')
def get_socalam(request):
    return render(request, 'home/socalam.html')
def get_dungcu(request):
    return render(request, 'home/dungcu.html')
def get_nghiphep(request):
    return render(request, 'home/nghiphep.html')
def get_thietbi(request):
    return render(request, 'home/thietbi.html')
def get_baotri(request):
    return render(request, 'home/baotri.html')
def get_thongtinnguyenlieu(request):
    return render(request, 'home/thongtinnguyenlieu.html')
def get_khonguyenlieu(request):
    return render(request, 'home/khonguyenlieu.html')

def so_ca_lam(request):
    ca_lam_list = Calam.objects.all()
    print(ca_lam_list) 
    return render(request, 'home/socalam.html', {'ca_lam_list': ca_lam_list})


def nghi_phep(request):
    nghi_phep_list = Nghiphep.objects.all()
    return render(request, 'home/nghiphep.html', {'nghi_phep_list': nghi_phep_list} )

def bang_luong(request):
    bang_luong_list = bangluong.objects.all()
    return render(request, 'home/luongnhanvien.html', {'bang_luong_list': bang_luong_list} )
