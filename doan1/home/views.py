from django.shortcuts import render, redirect, get_object_or_404
from .models import Calam, Nghiphep, Bangluong, Nhanvien, Thietbi, Baotri, Dungcu, Thongtinnguyenlieu
from .forms import nhap_nguyenlieu, nhap_khonguyenlieu, nhap_calam, nhap_baotri, nhap_dungcu, nhap_luongnhanvien, nhap_nghiphep, nhap_thietbi, nhap_nhanvien, nhap_thongtinnguyenlieu
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import pandas as pd
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import F
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import CustomUser
from .decorators import admin_required
from django.utils import timezone
from datetime import timedelta
# Create your views here.

#thongke
def thong_ke_nhan_vien(request):
    # Thông tin nhân viên
    tong_so_nhan_vien = Nhanvien.objects.count()
    so_nhan_vien_phuc_vu = Nhanvien.objects.filter(vitricongviec="Nhân viên phục vụ").count()
    so_nhan_vien_pha_che = Nhanvien.objects.filter(vitricongviec="Nhân viên pha chế").count()
    so_nhan_vien_kho = Nhanvien.objects.filter(vitricongviec="Nhân viên kho").count()
    so_nhan_vien_quan_ly = Nhanvien.objects.filter(vitricongviec="Nhân viên quản lý").count()

    today = timezone.now().date()
    so_nhan_vien_nghi_hom_nay = Nghiphep.objects.filter(ngaybd__lte=today, ngaykt__gte=today).count()
    so_nhan_vien_dang_lam_viec = tong_so_nhan_vien - so_nhan_vien_nghi_hom_nay

    # Nguyên liệu sắp hết hạn trong vòng 7 ngày
    het_han_trong_vong_7_ngay = today + timedelta(days=7)
    nguyen_lieu_sap_het_han = Thongtinnguyenlieu.objects.filter(ngayhethan__lte=het_han_trong_vong_7_ngay, ngayhethan__gte=today)

    # Cảnh báo nguyên liệu dưới mức tồn kho tối thiểu
    MUC_TON_KHO_TOI_THIEU = 10  # Giả sử mức tối thiểu là 10 đơn vị
    nguyen_lieu_duoi_ton_kho = Thongtinnguyenlieu.objects.filter(soluong__lt=MUC_TON_KHO_TOI_THIEU)

    # Truyền dữ liệu cho template
    context = {
        'tong_so_nhan_vien': tong_so_nhan_vien,
        'so_nhan_vien_phuc_vu': so_nhan_vien_phuc_vu,
        'so_nhan_vien_pha_che': so_nhan_vien_pha_che,
        'so_nhan_vien_kho': so_nhan_vien_kho,
        'so_nhan_vien_quan_ly': so_nhan_vien_quan_ly,
        'so_nhan_vien_dang_lam_viec': so_nhan_vien_dang_lam_viec,
        'so_nhan_vien_nghi_hom_nay': so_nhan_vien_nghi_hom_nay,
        'nguyen_lieu_sap_het_han': nguyen_lieu_sap_het_han,
        'nguyen_lieu_duoi_ton_kho': nguyen_lieu_duoi_ton_kho,
    }
    return render(request, 'home/trangchu.html', context)
#dangnhapdangky


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công!')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return render(request, 'home/dangky.html')

from django.contrib.auth import get_user_model
User = get_user_model()


def login_view(request):

    if request.user.is_authenticated:
        return redirect('trangchu')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
     
            if user.is_staff or user.is_superuser:
                messages.error(request, 'Tài khoản quản trị không được phép đăng nhập tại đây!')
                return render(request, 'home/dangnhap.html')
            
  
            login(request, user)
            messages.success(request, 'Đăng nhập thành công!')
            return redirect('trangchu') 
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    
    return render(request, 'home/dangnhap.html')


def login_viewql(request):

    if request.user.is_authenticated:
        return redirect('trangchu')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Login attempt: username={username}") 
        
        user = authenticate(request, username=username, password=password)
        
        print(f"Authentication result: user={user}")  
        
        if user is not None:
          
            if not (user.is_staff or user.is_superuser):
                messages.error(request, 'Bạn không có quyền đăng nhập vào trang quản lý!')
                return render(request, 'home/dangnhapquanly.html')
            
  
            login(request, user)
            messages.success(request, 'Đăng nhập thành công!')
            return redirect('trangchu')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    
    return render(request, 'home/dangnhapquanly.html')
def logout_view(request):
    logout(request)
    return redirect('index')  

@login_required
def profile(request):
    if request.method == 'POST':

        user = request.user
        user.phone = request.POST.get('phone', '')
        user.address = request.POST.get('address', '')
        user.birth_date = request.POST.get('birth_date', None)
        user.save()
        messages.success(request, 'Cập nhật thông tin thành công!')
        return redirect('profile')
    return render(request, 'home/profile.html')

#nganchan
@login_required
def trangchu(request):
    return render(request, 'home/trangchu.html')
#giaodien
def get_index(request):
    return render(request, 'home/index.html')
def get_dangnhap(request):
    return render(request, 'home/dangnhap.html')
def get_dangky(request):
    return render(request, 'home/dangky.html')
def get_trangchu(request):
    return render(request, 'home/trangchu.html')
def get_trangcanhan(request):
    return render(request, 'home/trangcanhan.html')
#baotri
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
    date = request.GET.get('date')
    search = request.GET.get('search')
    gia = request.GET.get('gia')
    if gia:
        min_gia, max_gia = map(int, gia.split('-'))
        bao_tri_list = bao_tri_list.filter(chiphi__gte=min_gia, chiphi__lte=max_gia)
    if date:
        bao_tri_list = bao_tri_list.filter(ngaybt=date)
    if search:
        bao_tri_list = bao_tri_list.filter(
            Q(mabt__icontains=search) |
            Q(matb__icontains=search) |
            Q(chiphi__icontains=search) |
            Q(nguoithuchien__icontains=search)|
            Q(mota__icontains=search) 
        )
    if request.method == "POST":
        bt = nhap_baotri(request.POST)
        if bt.is_valid():
            bt.save()
            return redirect('baotri.html')
    else:
        bt = nhap_baotri()
    return render(request, 'home/baotri.html',{
        'bao_tri_list': bao_tri_list,
        'bt':bt,
        'baotri': None  
    })

def sua_baotri(request, mabt):
    baotri = get_object_or_404(Baotri, mabt=mabt)
    if request.method == 'POST':
        form = nhap_baotri(request.POST, instance=baotri)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật thành công bảo trì {mabt}')
            return redirect('baotri')
        else:
            messages.error(request, 'Có lỗi xảy ra khi cập nhật. Vui lòng kiểm tra lại thông tin.')
    return redirect('baotri')

def delete_baotri(request, mabt):
    try:
        baotri = get_object_or_404(Baotri, mabt=mabt)
        baotri.delete()
        messages.success(request, 'Xóa bản ghi bảo trì thành công!')
    except Exception as e:
        messages.error(request, f'Xóa không thành công: {str(e)}')
    return redirect('baotri') 
#dungcu

def delete_dungcu(request, madc):
    try:
        dungcu = get_object_or_404(Dungcu, madc=madc)
        dungcu.delete()
        messages.success(request, 'Xóa bản ghi dụng cụ thành công!')
    except Exception as e:
        messages.error(request, f'Xóa không thành công: {str(e)}')
    return redirect('dungcu')
def Dung_cu(request):   
    dung_cu_list = Dungcu.objects.all()
    date = request.GET.get('date')
    search = request.GET.get('search')
    gia = request.GET.get('gia')
    if gia:
        min_gia, max_gia = map(int, gia.split('-'))
        dung_cu_list = dung_cu_list.filter(giamua__gte=min_gia, giamua__lte=max_gia)
    if date:
        dung_cu_list = dung_cu_list.filter(ngaymua=date)
    if search:
        dung_cu_list = dung_cu_list.filter(
            Q(madc__icontains=search) |
            Q(tendc__icontains=search) |
            Q(dvt__icontains=search) |
            Q(soluong__icontains=search)|
            Q(giamua__icontains=search)  
        )
    if request.method == "POST":
        dc = nhap_dungcu(request.POST)
        if dc.is_valid():
            dc.save()
            return redirect('dungcu.html')
    else:
        dc = nhap_dungcu()
    return render(request, 'home/dungcu.html', {'dung_cu_list': dung_cu_list, 'dc':dc, 'dungcu': None})


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

def sua_dungcu(request, madc):
    dungcu = get_object_or_404(Dungcu, madc=madc)
    if request.method == 'POST':
        form = nhap_dungcu(request.POST, instance=dungcu)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật thành công dụng cụ {madc}')
            return redirect('dungcu')
        else:
            messages.error(request, 'Có lỗi xảy ra khi cập nhật. Vui lòng kiểm tra lại thông tin.')
    return redirect('dungcu')

#khonguyenlieu
def Kho_nguyen_lieu(request):
    kho_nguyen_lieu_list = Thongtinnguyenlieu.objects.all()
    search = request.GET.get('search')
    soluong = request.GET.get('soluong')
    if soluong:
        min_gia, max_gia = map(int, soluong.split('-'))
        kho_nguyen_lieu_list = kho_nguyen_lieu_list.filter(gia__gte=min_gia, gia__lte=max_gia)
    if search:
        kho_nguyen_lieu_list = kho_nguyen_lieu_list.filter(
            Q(manl__icontains=search) |
            Q(manl__icontains=search) |
            Q(dvt__icontains=search) |
            Q(soluong__icontains=search)
        )
    return render(request, 'home/khonguyenlieu.html', {'kho_nguyen_lieu_list': kho_nguyen_lieu_list})


def delete_khonguyenlieu(request, manl):
    try:
        khonguyenlieu = get_object_or_404(Thongtinnguyenlieu, manl=manl)
        khonguyenlieu.delete()
        messages.success(request, 'Xóa bản ghi kho nguyên liệu thành công!')
    except Exception as e:
        messages.error(request, f'Xóa không thành công: {str(e)}')
    return redirect('khonguyenlieu')
def sua_khonguyenlieu(request, manl):
    khonguyenlieu = get_object_or_404(Thongtinnguyenlieu, manl=manl)
    if request.method == 'POST':
        form = nhap_khonguyenlieu(request.POST, instance=khonguyenlieu)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật thành công kho nguyen lieu {manl}')
            return redirect('khonguyenlieu')
        else:
            print(form.errors)
            messages.error(request, f'Có lỗi xảy ra khi cập nhật: {form.errors}')
    return redirect('khonguyenlieu')
  

#luongnhanvien
@admin_required
def bang_luong(request):
    bang_luong_list = Bangluong.objects.all()
    search = request.GET.get('search')
    gia = request.GET.get('gia')
    if gia:
        min_gia, max_gia = map(int, gia.split('-'))
        bang_luong_list = bang_luong_list.filter(tongluong__gte=min_gia, tongluong__lte=max_gia)
    if search:
        bang_luong_list = bang_luong_list.filter(
            Q(maluong__icontains=search) |
            Q(manv__icontains=search) |
            Q(sogio__icontains=search) |
            Q(luongcoban__icontains=search)
        )
    if request.method == "POST":
        bl = nhap_luongnhanvien(request.POST)
        if bl.is_valid():
            bl.save()
            return redirect('bangluong')  
    else:
        bl = nhap_luongnhanvien()
    return render(request, 'home/luongnhanvien.html',{
        'bang_luong_list': bang_luong_list,
        'bl': bl,
        'bangluong': None  
    })

def delete_bangluong(request, maluong):
    
        bangluong = get_object_or_404(Bangluong, maluong=maluong)
        bangluong.delete()
        messages.success(request, 'Xóa bản ghi bảng lương thành công!')
        return redirect('bangluong') 

def sua_bangluong(request, maluong):
    bangluong = get_object_or_404(Bangluong, maluong=maluong)
    if request.method == 'POST':
        form = nhap_luongnhanvien(request.POST, instance=bangluong)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật thành công lương {maluong}')
            return redirect('bangluong')
        else:
            messages.error(request, 'Có lỗi xảy ra khi cập nhật. Vui lòng kiểm tra lại thông tin.')
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
#nghiphep
@admin_required
def nghi_phep(request):
    nghi_phep_list = Nghiphep.objects.all()
    status = request.GET.get('status')
    nbd = request.GET.get('date1')
    nkt = request.GET.get('date2')
    search = request.GET.get('search')
    if nbd:
        nghi_phep_list = nghi_phep_list.filter(ngaybd=nbd)
    if nkt:
        nghi_phep_list = nghi_phep_list.filter(ngaykt=nkt)
    if status:
        nghi_phep_list = nghi_phep_list.filter(trangthai=status)
    if search:
        nghi_phep_list = nghi_phep_list.filter(
            Q(manp__icontains=search) |
            Q(manv__icontains=search) |
            Q(lydonghi__icontains=search) 
        )
    if request.method == "POST":
        np = nhap_nghiphep(request.POST)
        if np.is_valid():
            np.save()
            return redirect('nghiphep.html')
    else:
        np = nhap_nghiphep()
    return render(request, 'home/nghiphep.html', {'nghi_phep_list': nghi_phep_list,'np':np})

def sua_nghiphep(request, manp):
    nghiphep = get_object_or_404(Nghiphep, manp=manp)
    if request.method == 'POST':
        form = nhap_nghiphep(request.POST, instance=nghiphep)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật thành công nghỉ phép {manp}')
            return redirect('nghiphep')
        else:
            messages.error(request, f'Có lỗi xảy ra: {form.errors.as_json()}')  
    return redirect('nghiphep')
def delete_nghiphep(request, manp):
    try:
        manghiphep = get_object_or_404(Nghiphep, manp=manp)
        manghiphep.delete()
        messages.success(request, 'Xóa bản ghi nghỉ phép thành công!')
    except Exception as e:
        messages.error(request, f'Xóa không thành công: {str(e)}')
        return redirect('nghiphep')

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
#socalam

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
def sua_calam(request, macalam):
    calam = get_object_or_404(Calam, macalam=macalam)
    if request.method == 'POST':
        form = nhap_calam(request.POST, instance=calam)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật thành công ca làm {macalam}')
            return redirect('socalam')
        else:
            messages.error(request, f'Có lỗi xảy ra: {form.errors.as_json()}')  
    return redirect('socalam')
@admin_required
def so_ca_lam(request):
    ca_lam_list = Calam.objects.select_related('manv').annotate(
        tennv=F('manv__hoten')
    ).all()
    date = request.GET.get('date')
    search = request.GET.get('search')
    if date:
        ca_lam_list = ca_lam_list.filter(ngay=date)
    if search:
        ca_lam_list = ca_lam_list.filter(
            Q(macalam__icontains=search) |
            Q(manv__icontains=search) 
        )
    print(ca_lam_list) 
    if request.method == 'POST':
        form = nhap_calam(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home/socalam.html')
    else:
        form = nhap_calam()
    return render(request, 'home/socalam.html', {'ca_lam_list': ca_lam_list, 'form': form})


def delete_calam(request, macalam):
    try:
        macalam = get_object_or_404(Calam, macalam=macalam) 
        macalam.delete()
        messages.success(request, 'Xóa bản ghi ca làm thành công!')
    except Exception as e:
        messages.error(request, f'Xóa không thành công: {str(e)}')
    return redirect('socalam')
#thietbi
def thiet_bi(request):
    thiet_bi_list = Thietbi.objects.all()
    status = request.GET.get('status')
    date = request.GET.get('date')
    search = request.GET.get('search')
    gia = request.GET.get('gia')
    if gia:
        min_gia, max_gia = map(int, gia.split('-'))
        thiet_bi_list = thiet_bi_list.filter(giamua__gte=min_gia, giamua__lte=max_gia)
    if status:
        thiet_bi_list = thiet_bi_list.filter(tinhtrang=status)
    if date:
        thiet_bi_list = thiet_bi_list.filter(ngaymua=date)
    if search:
        thiet_bi_list = thiet_bi_list.filter(
            Q(matb__icontains=search) |
            Q(tentb__icontains=search) |
            Q(loaitb__icontains=search) |
            Q(soluong__icontains=search)
        )
    if request.method == "POST":
        tb = nhap_thietbi(request.POST)
        if tb.is_valid():
            tb.save()
            return redirect('thietbi.html')
    else:
        tb = nhap_thietbi()    
    return render(request, 'home/thietbi.html',{'thiet_bi_list':thiet_bi_list, 'tb':tb})
def sua_thietbi(request, matb):
    thietbi = get_object_or_404(Thietbi, matb=matb)
    if request.method == 'POST':
        form = nhap_thietbi(request.POST, instance=thietbi)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật thành công thiết bị {matb}')
            return redirect('thietbi')
        else:
            messages.error(request, f'Có lỗi xảy ra: {form.errors.as_json()}')  
    return redirect('thietbi')
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
def delete_thietbi(request, matb):
    try:
        mathietbi = get_object_or_404(Thietbi, matb=matb)
        mathietbi.delete()
        messages.success(request, 'Xóa bản ghi thiết bị thành công!')
    except Exception as e:
        messages.error(request, f'Xóa không thành công: {str(e)}')
    return redirect('thietbi')

#thongtinnguyenlieu
def Nguyen_lieu(request):
    nguyen_lieu_list = Thongtinnguyenlieu.objects.all()
    date = request.GET.get('date')
    search = request.GET.get('search')
    gia = request.GET.get('gia')
    if gia:
        min_gia, max_gia = map(int, gia.split('-'))
        nguyen_lieu_list = nguyen_lieu_list.filter(gia__gte=min_gia, gia__lte=max_gia)
    if date:
        nguyen_lieu_list = nguyen_lieu_list.filter(ngayhethan=date)
    if search:
        nguyen_lieu_list = nguyen_lieu_list.filter(
            Q(manl__icontains=search) |
            Q(manl__icontains=search) |
            Q(dvt__icontains=search) |
            Q(soluong__icontains=search)
        )
    return render(request, 'home/thongtinnguyenlieu.html', {'nguyen_lieu_list': nguyen_lieu_list})

def sua_thongtinnguyenlieu(request, manl):
    nguyenlieu = get_object_or_404(Thongtinnguyenlieu, manl=manl)
    if request.method == 'POST':
        form = nhap_nguyenlieu(request.POST, instance=nguyenlieu)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật thành công nguyên liệu {manl}')
            return redirect('thongtinnguyenlieu')
        else:
            messages.error(request, f'Có lỗi xảy ra: {form.errors.as_json()}')  
    return redirect('thongtinnguyenlieu')
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
def delete_thongtinnguyenlieu(request, manl):
    try:
        ttnguyenlieu = get_object_or_404(Thongtinnguyenlieu, manl=manl)
        ttnguyenlieu.delete()
        messages.success(request, 'Xóa bản ghi thông tin nguyên liệu thành công!')
    except Exception as e:
        messages.error(request, f'Xóa không thành công: {str(e)}')
        return redirect('thongtinnguyenlieu')
#thongtinnhanvien
def delete_thongtinnhanvien(request, manv):
    try:
        ttnhanvien = get_object_or_404(Nhanvien, manv=manv)
        ttnhanvien.delete()
        messages.success(request, 'Xóa bản ghi thông tin nhân viên thành công!')
    except Exception as e:
        messages.error(request, f'Xóa không thành công: {str(e)}')
    return redirect('thongtinnhanvien')




def nhan_vien(request):
    
    nhan_vien_list = Nhanvien.objects.all()
    status = request.GET.get('status')
    date = request.GET.get('date')
    search = request.GET.get('search')
    vtcv = request.GET.get('vtcv')
    if vtcv:
        nhan_vien_list = nhan_vien_list.filter(vitricongviec=vtcv)
    if status:
        nhan_vien_list = nhan_vien_list.filter(trangthai=status)
    if date:
        nhan_vien_list = nhan_vien_list.filter(ngayvaolam=date)
    if search:
        nhan_vien_list = nhan_vien_list.filter(
            Q(hoten__icontains=search) |
            Q(manv__icontains=search) |
            Q(sdt__icontains=search) |
            Q(diachi__icontains=search)
        )
    if request.method == "POST":
        nv = nhap_nhanvien(request.POST)
        if nv.is_valid():
            nv.save()
            return redirect('thongtinnhanvien.html')
    else:
        nv = nhap_nhanvien()    
    return render(request, 'home/thongtinnhanvien.html', {'nhan_vien_list': nhan_vien_list, 'nv':nv })


def sua_thongtinnhanvien(request, manv):
    nhanvien = get_object_or_404(Nhanvien, manv=manv)
    if request.method == 'POST':
        form = nhap_nhanvien(request.POST, instance=nhanvien)
        if form.is_valid():
            form.save()
            messages.success(request, f'Đã cập nhật thành công nhân viên {manv}')
            return redirect('thongtinnhanvien')
        else:
            messages.error(request, f'Có lỗi xảy ra: {form.errors.as_json()}')  
    return redirect('thongtinnhanvien')
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