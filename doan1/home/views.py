from django.shortcuts import render, redirect, get_object_or_404
from .models import Calam, Nghiphep, Bangluong, Nhanvien, Thietbi, Baotri, Dungcu, Thongtinnguyenlieu
from .forms import nhap_calam, nhap_baotri, nhap_dungcu, nhap_luongnhanvien, nhap_nghiphep, nhap_thietbi, nhap_nhanvien, nhap_thongtinnguyenlieu
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import pandas as pd
from django.contrib import messages
# Create your views here.
def get_trangcanhan(request):
    return render(request, 'home/trangcanhan.html')
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


def import_excel_calam(request):
    if request.method == "POST" and request.FILES['file']:
        try: 
            excel_f = request.FILES['file']
            df = pd.read_excel(excel_f)
            success_count = 0
        
            for index, row in df.iterrows():
                try:
                    Calam.objects.create(
                        macalam = row['Mã ca làm'],
                        manv = row['Mã nhân viên'],
                        ngay = row['Ngày'],
                        giobd = row['Giờ bắt đầu'],
                        giokt = row['Giờ kết thúc']
                    )
                    success_count += 1
                except Exception as e:
                    messages.error(request, f'Lỗi ở dòng {index + 2}: {str(e)}')
            if success_count > 0:
                messages.success(request, f'Import thành công {success_count} bản ghi')
        except Exception as e:
            messages.error(request, f'Import thất bại: {str(e)}')
    
        return redirect('socalam')
    return render(request, 'home/socalam.html')

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


def import_excel_nghiphep(request):
    if request.method == "POST" and request.FILES['file']:
        try:
            excel_f = request.FILES['file']
            df = pd.read_excel(excel_f)
            success_ip = 0
            for index, row in df.iterrows():
                try:
                    Nghiphep.objects.create(
                        manp = row['Mã nghỉ phép'],
                        manv = row['Mã nhân viên'],
                
                        ngaybd = row['Ngày bắt đầu'],
                        ngaykt = row['Ngày kết thúc'],
                        lydonghi = row['Lý do nghỉ'],
                        trangthai = row['Trạng thái']
                       
                    )
                    success_ip += 1
                except Exception as e:
                    messages.error(request, f'Lỗi ở dòng {index + 2}: {str(e)}')
            if success_ip > 0:
                messages.success(request, f'Import Thành công {success_ip} bản ghi')
        except Exception as e:
            messages.error(request, f'Import thất bại: {str(e)}')
        return redirect('nghiphep')
    return render(request, 'home/nghiphep.html')

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
def delete_bangluong(request, maluong):
    
        bangluong = get_object_or_404(Bangluong, maluong=maluong)
        bangluong.delete()
        messages.success(request, 'Xóa bản ghi bảng lương thành công!')
        return redirect('bangluong') 


def import_excel_bangluong(request):
    if request.method == "POST" and request.FILES['file']:
        try:
            excel_f = request.FILES['file']
            df = pd.read_excel(excel_f)
            success_ip = 0
            for index, row in df.iterrows():
                try:
                    Bangluong.objects.create(
                        maluong = row['Mã lương'],
                        manv = row['Mã nhân viên'],
                        sogio = row['Số giờ'],
                        luongcoban = row['Lương cơ bản'],
                        tongluong = row['Tổng lương']
                       
                    )
                    success_ip += 1
                except Exception as e:
                    messages.error(request, f'Lỗi ở dòng {index + 2}: {str(e)}')
            if success_ip > 0:
                messages.success(request, f'Import Thành công {success_ip} bản ghi')
        except Exception as e:
            messages.error(request, f'Import thất bại: {str(e)}')
        return redirect('bangluong')
    return render(request, 'home/luongnhanvien.html')

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

def import_excel_thongtinnhanvien(request):
    if request.method == "POST" and request.FILES['file']:
        try:
            excel_f = request.FILES['file']
            df = pd.read_excel(excel_f)
            success_ip = 0
            for index, row in df.iterrows():
                try:
                    Nhanvien.objects.create(
                        manv= row['Mã nhân viên'],
                        hoten = row['Họ tên'],
                
                        ngaysinh = row['Ngày sinh'],
                        sdt = row['Số điện thoại'],
                        diachi = row['Địa chỉ'],
                        ngayvaolam = row['Ngày vào làm'],
                        vitricongviec = row['Vị trí công việc'],
                        trangthai = row['Trạng thái']

                       
                    )
                    success_ip += 1
                except Exception as e:
                    messages.error(request, f'Lỗi ở dòng {index + 2}: {str(e)}')
            if success_ip > 0:
                messages.success(request, f'Import Thành công {success_ip} bản ghi')
        except Exception as e:
            messages.error(request, f'Import thất bại: {str(e)}')
        return redirect('thongtinnhanvien')
    return render(request, 'home/thongtinnhanvien.html')

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

def import_excel_thietbi(request):
    if request.method == "POST" and request.FILES['file']:
        try:
            excel_f = request.FILES['file']
            df = pd.read_excel(excel_f)
            success_ip = 0
            for index, row in df.iterrows():
                try:
                    Thietbi.objects.create(
                        matb = row['Mã thiết bị'],
                        tentb = row['Tên thiết bị'],
                
                        loaitb = row['Loại thiết bị'],
                        soluong = row['Số lượng'],
                        tinhtrang = row['Tình trạng'],
                        ngaymua = row['Ngày mua'],
                        giamua = row['Giá mua']

                       
                    )
                    success_ip += 1
                except Exception as e:
                    messages.error(request, f'Lỗi ở dòng {index + 2}: {str(e)}')
            if success_ip > 0:
                messages.success(request, f'Import Thành công {success_ip} bản ghi')
        except Exception as e:
            messages.error(request, f'Import thất bại: {str(e)}')
        return redirect('thietbi')
    return render(request, 'home/thietbi.html')

def import_excel_baotri(request):
    if request.method == "POST" and request.FILES['file']:
        try:
            excel_f = request.FILES['file']
            df = pd.read_excel(excel_f)
            success_ip = 0
            for index, row in df.iterrows():
                try:
                    Baotri.objects.create(
                        mabt = row['Mã bảo trì'],
                        matb = row['Mã thiết bị'],
                        ngaybt = row['Ngày bảo trì'],
                        mota = row['Mô tả'],
                        chiphi = row['Chi phí'],
                        nguoithuchien = row['Người thực hiện']
                    )
                    success_ip += 1
                except Exception as e:
                    messages.error(request, f'Lỗi ở dòng {index + 2}: {str(e)}')
            if success_ip > 0:
                messages.success(request, f'Import Thành công {success_ip} bản ghi')
        except Exception as e:
            messages.error(request, f'Import thất bại: {str(e)}')
        return redirect('baotri')
    return render(request, 'home/baotri.html')
                
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

def delete_baotri(request, mabt):
    
        baotri = get_object_or_404(Baotri, mabt=mabt)
        baotri.delete()
        messages.success(request, 'Xóa bản ghi bảo trì thành công!')
        return redirect('baotri') 
    
def delete_dungcu(request, madc):
        dungcu = get_object_or_404(Dungcu, madc=madc)
        dungcu.delete()
        messages.success(request, 'Xóa bản ghi dụng cụ thành công!')
        return redirect('dungcu')

def delete_nghiphep(request, manp):
        manghiphep = get_object_or_404(Nghiphep, manp=manp)
        manghiphep.delete()
        messages.success(request, 'Xóa bản ghi nghỉ phép thành công!')
        return redirect('nghiphep')
def delete_calam(request, macl):
        macalam = get_object_or_404(Nghiphep, macl=macl)
        macalam.delete()
        messages.success(request, 'Xóa bản ghi ca làm thành công!')
        return redirect('calam')
    

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

def import_excel_dungcu(request):
    if request.method == "POST" and request.FILES['file']:
        try:
            excel_f = request.FILES['file']
            df = pd.read_excel(excel_f)
            success_ip = 0
            for index, row in df.iterrows():
                try:
                    Dungcu.objects.create(
                        madc = row['Mã dụng cụ'],
                        tendc = row['Tên dụng cụ'],
                        soluong = row['Số lượng'],
                        dvt = row['Đơn vị tính'],
                        ngaymua = row['Ngày mua'],
                        giamua = row['Giá mua']
                    )
                    success_ip += 1
                except Exception as e:
                    messages.error(request, f'Lỗi ở dòng {index + 2}: {str(e)}')
            if success_ip > 0:
                messages.success(request, f'Import Thành công {success_ip} bản ghi')
        except Exception as e:
            messages.error(request, f'Import thất bại: {str(e)}')
        return redirect('dungcu')
    return render(request, 'home/dungcu.html')

def Nguyen_lieu(request):
    nguyen_lieu_list = Thongtinnguyenlieu.objects.all()
    if request.method =="POST":
        nl = nhap_thongtinnguyenlieu(request.POST)
        if nl.is_valid():
            nl.save()
            return redirect('thongtinnguyenlieu.html')
    else:
        nl = nhap_thongtinnguyenlieu()
    
    return render(request, 'home/thongtinnguyenlieu.html', {'nguyen_lieu_list': nguyen_lieu_list, 'nl': nl})

def import_excel_thongtinnguyenlieu(request):
    if request.method == "POST" and request.FILES['file']:
        try:
            excel_f = request.FILES['file']
            df = pd.read_excel(excel_f)
            success_ip = 0
            for index, row in df.iterrows():
                try:
                    Thongtinnguyenlieu.objects.create(
                        manl = row['Mã nguyên liệu'],
                        tennl = row['Tên nguyên liệu'],
                        gia = row['Giá'],
                        dvt = row['Đơn vị tính'],
                        soluong = row['Số lượng'],
                        ngayhethan = row['Ngày hết hạn']
                    )
                    success_ip += 1
                except Exception as e:
                    messages.error(request, f'Lỗi ở dòng {index + 2}: {str(e)}')
            if success_ip > 0:
                messages.success(request, f'Import Thành công {success_ip} bản ghi')
        except Exception as e:
            messages.error(request, f'Import thất bại: {str(e)}')
        return redirect('thongtinnguyenlieu')
    return render(request, 'home/thongtinnguyenlieu.html')

def Kho_nguyen_lieu(request):
    kho_nguyen_lieu_list = Thongtinnguyenlieu.objects.all()
    return render(request, 'home/khonguyenlieu.html', {'kho_nguyen_lieu_list': kho_nguyen_lieu_list})

def delete_khonguyenlieu(request, manl):
        khonguyenlieu = get_object_or_404(Thongtinnguyenlieu, manl=manl)
        khonguyenlieu.delete()
        messages.success(request, 'Xóa bản ghi kho nguyên liệu thành công!')
        return redirect('khonguyenlieu')
