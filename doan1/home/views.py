from django.shortcuts import render, redirect
from .models import Calam
from .models import Nghiphep
from .models import Bangluong
from .models import Nhanvien
from.models  import Thietbi
from.models  import Baotri
from.models  import Dungcu
from.models import Thongtinnguyenlieu
from .forms import nhap_calam
from .forms import nhap_baotri
from .forms import nhap_dungcu
from django.http import HttpResponse
from .forms import nhap_luongnhanvien
from .forms import nhap_nghiphep
from .forms import nhap_thietbi
from .forms import nhap_nhanvien
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
    if request.method == 'POST':
        form = nhap_calam(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home/socalam.html')
    else:
        form = nhap_calam()
    return render(request, 'home/socalam.html', {'ca_lam_list': ca_lam_list, 'form': form})

  
   
def nghi_phep(request):
    nghi_phep_list = Nghiphep.objects.all()
    if request.method == "POST":
        np = nhap_nghiphep(request.POST)
        if np.is_valid():
            np.save()
            return redirect('nghiphep.html')
    else:
        np = nhap_nghiphep()
    return render(request, 'home/nghiphep.html', {'nghi_phep_list': nghi_phep_list,'np':np})

def bang_luong(request):
    bang_luong_list = Bangluong.objects.all()
    if request.method == "POST":
        bl = nhap_luongnhanvien(request.POST)
        if bl.is_valid():
            bl.save()
            return redirect('luongnhanvien.html')
    else:
        bl = nhap_luongnhanvien()
    return render(request, 'home/luongnhanvien.html',{'bang_luong_list':bang_luong_list,'bl': bl})


def nhan_vien(request):
    nhan_vien_list = Nhanvien.objects.all()
    if request.method == "POST":
        nv = nhap_nhanvien(request.POST)
        if nv.is_valid():
            nv.save()
            return redirect('thongtinnhanvien.html')
    else:
        nv = nhap_nhanvien()    
    return render(request, 'home/thongtinnhanvien.html', {'nhan_vien_list': nhan_vien_list, 'nv':nv})


def thiet_bi(request):
    thiet_bi_list = Thietbi.objects.all()
    if request.method == "POST":
        tb = nhap_thietbi(request.POST)
        if tb.is_valid():
            tb.save()
            return redirect('thietbi.html')
    else:
        tb = nhap_thietbi()    
    return render(request, 'home/thietbi.html',{'thiet_bi_list':thiet_bi_list, 'tb':tb})

def Bao_tri(request):
    bao_tri_list = Baotri.objects.all()
    if request.method == "POST":
        bt = nhap_baotri(request.POST)
        if bt.is_valid():
            bt.save()
            return redirect('baotri.html')
    else:
        bt = nhap_baotri()
    return render(request, 'home/baotri.html', {'bao_tri_list': bao_tri_list, 'bt':bt})

def Dung_cu(request):   
    dung_cu_list = Dungcu.objects.all()
    if request.method == "POST":
        dc = nhap_dungcu(request.POST)
        if dc.is_valid():
            dc.save()
            return redirect('dungcu.html')
    else:
        dc = nhap_dungcu()
    return render(request, 'home/dungcu.html', {'dung_cu_list': dung_cu_list, 'dc':dc})

def Nguyen_lieu(request):
    nguyen_lieu_list = Thongtinnguyenlieu.objects.all()
    return render(request, 'home/thongtinnguyenlieu.html', {'nguyen_lieu_list': nguyen_lieu_list})


def Kho_nguyen_lieu(request):
    kho_nguyen_lieu_list = Thongtinnguyenlieu.objects.all()
    return render(request, 'home/khonguyenlieu.html', {'kho_nguyen_lieu_list': kho_nguyen_lieu_list})