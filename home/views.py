from django.shortcuts import render, redirect, get_object_or_404
from .models import CaptchaForm, Calam, Nghiphep, Bangluong, Nhanvien, Thietbi, Baotri, Dungcu, Thongtinnguyenlieu
from .forms import ChangePasswordForm ,ForgotPasswordForm ,nhap_nguyenlieu, nhap_khonguyenlieu, nhap_calam, nhap_baotri, nhap_dungcu, nhap_luongnhanvien, nhap_nghiphep, nhap_thietbi, nhap_nhanvien, nhap_thongtinnguyenlieu
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import pandas as pd
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import CustomUser
from .decorators import admin_required
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, datetime, date
import random
import string
from django.db.models.functions import TruncDate, TruncMonth, TruncYear, ExtractYear, ExtractMonth
from django.db.models import Count,  F, IntegerField, DurationField, ExpressionWrapper
from django.utils import timezone

from io import BytesIO
# Create your views here.
from django.http import JsonResponse

def thong_ke_view(request):
    # Xử lý dữ liệu và trả về JSON nếu là yêu cầu Ajax
    if request.is_ajax():
        data = {
            'thong_ke_ngay': thong_ke_ngay_data, 
            'thong_ke_thang': thong_ke_thang_data, 
            'thong_ke_quy': thong_ke_quy_data, 
            'thong_ke_nam': thong_ke_nam_data
        }
        return JsonResponse(data)
    # Trả về trang HTML cho yêu cầu thông thường
    return render(request, 'trang_thong_ke.html', data)

#xuat excel trang chu
def format_sheet(writer, sheet_name, df):
    """Helper function để format worksheet với xử lý ngày tháng"""
    worksheet = writer.sheets[sheet_name]
    
    # Format cơ bản
    header_format = writer.book.add_format({
        'bold': True,
        'bg_color': '#4F81BD',
        'font_color': 'white',
        'border': 1,
        'align': 'center'
    })
    
    cell_format = writer.book.add_format({
        'border': 1,
        'align': 'left'
    })
    
    # Format cho ngày tháng
    date_format = writer.book.add_format({
        'border': 1,
        'align': 'left',
        'num_format': 'dd/mm/yyyy'  # Định dạng ngày tháng
    })
    
    # Set column width và format headers
    for idx, col in enumerate(df.columns):
        series = df[col]
        max_len = max(
            series.astype(str).map(len).max(),
            len(str(series.name))
        ) + 2
        worksheet.set_column(idx, idx, max_len)
        worksheet.write(0, idx, col, header_format)

    # Format cells với xử lý đặc biệt cho cột ngày
    for row in range(1, len(df) + 1):
        for col, column_name in enumerate(df.columns):
            value = df.iloc[row-1, col]
            
            # Kiểm tra nếu là cột ngày và chuyển đổi từ số Excel sang datetime
            if column_name in ['Ngày bắt đầu', 'Ngày kết thúc', 'Ngày sinh', 'Ngày vào làm', 'Ngày mua', 'Ngày hết hạn']:
                # Xử lý giá trị số ngày của Excel
                if isinstance(value, (int, float)):
                    # Chuyển đổi số Excel sang datetime
                    from datetime import datetime, timedelta
                    excel_epoch = datetime(1900, 1, 1)
                    try:
                        # Trừ 2 vì Excel tính sai ngày trong khoảng 1900-1904
                        date_value = excel_epoch + timedelta(days=int(value - 2))
                        worksheet.write(row, col, date_value, date_format)
                        continue
                    except:
                        pass
                        
            worksheet.write(row, col, value, cell_format)

def xuat_baocao_nhanvien(request):
    hom_nay = date.today()
    
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # 1. Sheet nhân viên đi làm
    nhanviens_dilam = Nhanvien.objects.filter(
        ngayvaolam__lte=hom_nay, 
        trangthai="đi làm"
    ).values(
        'manv', 'hoten', 'ngaysinh', 'sdt', 'diachi', 
        'ngayvaolam', 'vitricongviec'
    )
    
    df_dilam = pd.DataFrame(list(nhanviens_dilam))
    if not df_dilam.empty:
        df_dilam.columns = ['Mã NV', 'Họ tên', 'Ngày sinh', 'Số ĐT', 
                           'Địa chỉ', 'Ngày vào làm', 'Vị trí công việc']
        df_dilam['Trạng thái'] = 'Đi làm'
        df_dilam.to_excel(writer, sheet_name='Nhân viên đi làm', index=False)
        format_sheet(writer, 'Nhân viên đi làm', df_dilam)
    
    # 2. Sheet nhân viên nghỉ phép
    nhanviens_nghiphep = Nghiphep.objects.filter(
        ngaybd__lte=hom_nay, 
        ngaykt__gte=hom_nay
    ).select_related('manv').values(
        'manv__manv', 'manv__hoten', 'ngaybd', 'ngaykt', 
        'lydonghi', 'trangthai'
    )
    
    df_nghiphep = pd.DataFrame(list(nhanviens_nghiphep))
    if not df_nghiphep.empty:
        df_nghiphep.columns = ['Mã NV', 'Họ tên', 'Ngày bắt đầu', 
                              'Ngày kết thúc', 'Lý do nghỉ', 'Trạng thái']
        df_nghiphep.to_excel(writer, sheet_name='Nhân viên nghỉ phép', index=False)
        format_sheet(writer, 'Nhân viên nghỉ phép', df_nghiphep)
    
    writer.close()
    output.seek(0)
    
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Baocao_nhanvien.xlsx'
    return response

def xuat_baocao_thietbi_nguyenlieu(request):
    hom_nay = date.today()
    
    # Tạo buffer để lưu file Excel
    output = BytesIO()
    
    # Tạo ExcelWriter object với xlsxwriter engine
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # 1. Sheet thiết bị cần bảo trì
    thietbis = Thietbi.objects.exclude(tinhtrang="tốt").values(
        'matb', 'tentb', 'loaitb', 'soluong', 'tinhtrang', 
        'ngaymua', 'giamua'
    )
    
    df_thietbi = pd.DataFrame(list(thietbis))
    if not df_thietbi.empty:
        df_thietbi.columns = ['Mã TB', 'Tên TB', 'Loại TB', 'Số lượng', 
                             'Tình trạng', 'Ngày mua', 'Giá mua']
        df_thietbi.to_excel(writer, sheet_name='Thiết bị cần bảo trì', index=False)
        format_sheet(writer, 'Thiết bị cần bảo trì', df_thietbi)
    
    # 2. Sheet nguyên liệu sắp hết
    nguyenlieus_saphet = Thongtinnguyenlieu.objects.filter(
        soluong__lt=10
    ).values(
        'manl', 'tennl', 'dvt', 'soluong', 'gia', 'ngayhethan'
    )
    
    df_nlsaphet = pd.DataFrame(list(nguyenlieus_saphet))
    if not df_nlsaphet.empty:
        df_nlsaphet.columns = ['Mã NL', 'Tên NL', 'Đơn vị tính', 
                              'Số lượng', 'Giá', 'Ngày hết hạn']
        df_nlsaphet['Ghi chú'] = 'Sắp hết hàng'
        df_nlsaphet.to_excel(writer, sheet_name='Nguyên liệu sắp hết', index=False)
        format_sheet(writer, 'Nguyên liệu sắp hết', df_nlsaphet)
    
    # 3. Sheet nguyên liệu sắp hết hạn
    nguyenlieus_hethan = Thongtinnguyenlieu.objects.filter(
        ngayhethan__lte=hom_nay + pd.Timedelta(days=7)
    ).values(
        'manl', 'tennl', 'dvt', 'soluong', 'gia', 'ngayhethan'
    )
    
    df_nlhethan = pd.DataFrame(list(nguyenlieus_hethan))
    if not df_nlhethan.empty:
        df_nlhethan.columns = ['Mã NL', 'Tên NL', 'Đơn vị tính', 
                              'Số lượng', 'Giá', 'Ngày hết hạn']
        df_nlhethan['Ghi chú'] = 'Sắp hết hạn'
        df_nlhethan.to_excel(writer, sheet_name='Nguyên liệu sắp hết hạn', index=False)
        format_sheet(writer, 'Nguyên liệu sắp hết hạn', df_nlhethan)
    
    # Lưu file và trả về response
    writer.close()
    output.seek(0)
    
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Baocao_thietbi_nguyenlieu.xlsx'
    return response
#xuatexcel
def export_excel_nhansu(request):
    # Tạo writer để ghi nhiều sheet vào một file Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # 1. Sheet Nhân viên
    nhanvien_data = Nhanvien.objects.values(
        'hoten',
        'ngaysinh',
        'sdt',
        'diachi',
        'ngayvaolam',
        'vitricongviec',
        'trangthai'
    )
    df_nhanvien = pd.DataFrame(list(nhanvien_data))
    if not df_nhanvien.empty:
        df_nhanvien.columns = ['Họ tên', 'Ngày sinh', 'Số điện thoại', 'Địa chỉ',
                              'Ngày vào làm', 'Vị trí công việc', 'Trạng thái']
    df_nhanvien.to_excel(writer, sheet_name='Nhân viên', index=False)

   # Sheet Nghỉ phép
    nghiphep_data = Nghiphep.objects.annotate(
        ten_nhanvien=F('manv__hoten')
    ).values(
        'ten_nhanvien',
        'ngaybd',
        'ngaykt', 
        'lydonghi',
        'trangthai'
    ).order_by('ngaybd')  # Sắp xếp theo ngày bắt đầu

    df_nghiphep = pd.DataFrame(list(nghiphep_data))
    if not df_nghiphep.empty:
        # Đổi tên cột trước khi xử lý dữ liệu
        df_nghiphep.rename(columns={
            'ten_nhanvien': 'Họ tên nhân viên',
            'ngaybd': 'Ngày bắt đầu',
            'ngaykt': 'Ngày kết thúc',
            'lydonghi': 'Lý do nghỉ',
            'trangthai': 'Trạng thái'
        }, inplace=True)

        # Chỉ chuyển đổi định dạng cho các cột ngày tháng
        date_columns = ['Ngày bắt đầu', 'Ngày kết thúc']
        for col in date_columns:
            df_nghiphep[col] = pd.to_datetime(df_nghiphep[col]).dt.strftime('%d-%m-%Y')

    df_nghiphep.to_excel(writer, sheet_name='Nghỉ phép', index=False)

    # Định dạng sheet
    worksheet = writer.sheets['Nghỉ phép']
    worksheet.set_column('A:A', 20)  # Họ tên
    worksheet.set_column('B:C', 15)  # Ngày tháng
    worksheet.set_column('D:D', 25)  # Lý do nghỉ
    worksheet.set_column('E:E', 15)  # Trạng thái

    # Thêm định dạng cho header
    header_format = writer.book.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#D7E4BC',
        'border': 1
    })

# Áp dụng định dạng cho header
    for col_num, value in enumerate(df_nghiphep.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # 3. Sheet Lương
    luong_data = Bangluong.objects.annotate(
        ten_nhanvien=F('manv__hoten')
    ).values(
        'ten_nhanvien',
        'thangluong',
        'sogio',
        'luongcoban',
        'tongluong'
    )
    df_luong = pd.DataFrame(list(luong_data))
    if not df_luong.empty:
        df_luong.columns = ['Tháng lương', 'Số giờ', 
                           'Lương cơ bản','Tổng lương','Họ tên nhân viên']
    df_luong.to_excel(writer, sheet_name='Bảng lương', index=False)

    # Format các sheet
    for sheet_name in writer.sheets:
        worksheet = writer.sheets[sheet_name]
        worksheet.set_column('A:Z', 18)

    # Lưu file
    writer.close()
    
    # Chuẩn bị response
    output.seek(0)
    filename = f'bao_cao_nhan_su_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

def export_excel_thietbi(request):
    # Tạo writer để ghi nhiều sheet vào một file Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # 1. Sheet Thiết bị
    thietbi_data = Thietbi.objects.values(
        'tentb',
        'loaitb',
        'soluong',
        'tinhtrang',
        'ngaymua',
        'giamua'
    )
    df_thietbi = pd.DataFrame(list(thietbi_data))
    if not df_thietbi.empty:
        df_thietbi.columns = ['Tên thiết bị', 'Loại thiết bị', 'Số lượng',
                             'Tình trạng', 'Ngày mua', 'Giá mua']
    df_thietbi.to_excel(writer, sheet_name='Thiết bị', index=False)

    # 2. Sheet Bảo trì
    baotri_data = Baotri.objects.annotate(
        ten_thietbi=F('matb__tentb')
    ).values(
        'ten_thietbi',
        'ngaybt',
        'mota',
        'chiphi',
        'nguoithuchien'
    )
    df_baotri = pd.DataFrame(list(baotri_data))
    if not df_baotri.empty:
        df_baotri.columns = ['Tên thiết bị', 'Ngày bảo trì', 'Mô tả',
                            'Chi phí', 'Người thực hiện']
    df_baotri.to_excel(writer, sheet_name='Bảo trì', index=False)

    # 3. Sheet Dụng cụ
    dungcu_data = Dungcu.objects.values(
        'tendc',
        'soluong',
        'dvt',
        'ngaymua',
        'giamua'
    )
    df_dungcu = pd.DataFrame(list(dungcu_data))
    if not df_dungcu.empty:
        df_dungcu.columns = ['Tên dụng cụ', 'Số lượng', 'Đơn vị tính',
                            'Ngày mua', 'Giá mua']
    df_dungcu.to_excel(writer, sheet_name='Dụng cụ', index=False)

    # 4. Sheet Nguyên liệu
    nguyenlieu_data = Thongtinnguyenlieu.objects.values(
        'tennl',
        'dvt',
        'soluong',
        'gia',
        'ngayhethan'
    )
    df_nguyenlieu = pd.DataFrame(list(nguyenlieu_data))
    if not df_nguyenlieu.empty:
        df_nguyenlieu.columns = ['Tên nguyên liệu', 'Đơn vị tính', 'Số lượng',
                                'Giá', 'Ngày hết hạn']
    df_nguyenlieu.to_excel(writer, sheet_name='Nguyên liệu', index=False)

    # Format các sheet
    for sheet_name in writer.sheets:
        worksheet = writer.sheets[sheet_name]
        worksheet.set_column('A:Z', 18)

    # Lưu file
    writer.close()
    
    # Chuẩn bị response
    output.seek(0)
    filename = f'bao_cao_thiet_bi_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
#doimk
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            
            # Kiểm tra mật khẩu cũ
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Đổi mật khẩu thành công!')
                return redirect('index')  # Chuyển về trang đăng nhập
            else:
                messages.error(request, 'Mật khẩu cũ không đúng')
    else:
        form = ChangePasswordForm()
    
    return render(request, 'home/change_password.html', {'form': form})
#quenmk
def generate_password():
    """Tạo mật khẩu ngẫu nhiên 12 ký tự"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(12))

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Tìm user với email được cung cấp
            user = CustomUser.objects.filter(email=email).first()
            
            if user:
                # Generate mật khẩu mới
                new_password = generate_password()
                
                # Cập nhật mật khẩu mới cho user
                user.set_password(new_password)
                user.save()
                
                # Chuẩn bị nội dung email
                subject = 'Mật khẩu mới cho tài khoản của bạn'
                message = f"""Xin chào {user.username},

Bạn vừa yêu cầu đặt lại mật khẩu cho tài khoản của mình.
Dưới đây là thông tin đăng nhập mới của bạn:

Username: {user.username}
Mật khẩu mới: {new_password}

Vui lòng đăng nhập và đổi mật khẩu ngay sau khi nhận được email này.

Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng liên hệ với chúng tôi ngay.

Trân trọng,
Ban quản trị"""

                try:
                    # Gửi email
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        
                    )

                    messages.success(
                        request, 
                        'Mật khẩu mới đã được gửi đến email của bạn. Vui lòng kiểm tra email và đăng nhập lại.'
                    )
                    return redirect('index')
                
                except Exception as e:
                    # Nếu gửi email thất bại, hoàn tác việc đổi mật khẩu
                    user.set_password(new_password)
                    user.save()
                    messages.error(
                        request,
                        'Có lỗi xảy ra khi gửi email. Vui lòng thử lại sau.'
                    )
            else:
                messages.error(
                    request,
                    'Email này không tồn tại trong hệ thống. Vui lòng kiểm tra lại.'
                )
                
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'home/forgot_password.html', {'form': form})
#thongke


def thong_ke_nhan_vien(request):
    # Thông tin nhân viên
    tong_so_nhan_vien = Nhanvien.objects.count()
    so_nhan_vien_phuc_vu = Nhanvien.objects.filter(vitricongviec="Nhân viên phục vụ").count()
    so_nhan_vien_pha_che = Nhanvien.objects.filter(vitricongviec="Nhân viên pha chế").count()
    so_nhan_vien_kho = Nhanvien.objects.filter(vitricongviec="Nhân viên kho").count()
    so_nhan_vien_quan_ly = Nhanvien.objects.filter(vitricongviec="Quản lý").count()
    data = Nhanvien.objects.values_list('ngayvaolam', flat=True)

    today = timezone.now().date()
    so_nhan_vien_nghi_hom_nay = Nghiphep.objects.filter(ngaybd__lte=today, ngaykt__gte=today).count()
    so_nhan_vien_dang_lam_viec = tong_so_nhan_vien - so_nhan_vien_nghi_hom_nay

    # Nguyên liệu sắp hết hạn trong vòng 7 ngày
    het_han_trong_vong_7_ngay = today + timedelta(days=7)
    nguyen_lieu_sap_het_han = Thongtinnguyenlieu.objects.filter(ngayhethan__lte=het_han_trong_vong_7_ngay, ngayhethan__gte=today)

    # Cảnh báo nguyên liệu dưới mức tồn kho tối thiểu
    MUC_TON_KHO_TOI_THIEU = 10  # Giả sử mức tối thiểu là 10 đơn vị
    nguyen_lieu_duoi_ton_kho = Thongtinnguyenlieu.objects.filter(soluong__lt=MUC_TON_KHO_TOI_THIEU)

    # Dữ liệu để thống kê theo ngày tháng năm
    data = Nghiphep.objects.values_list('ngaybd', flat=True)
    thong_ke_ngay = {}
    thong_ke_thang = {}
    thong_ke_nam = {}
    thong_ke_quy = {}
    if 'ngay' in request.GET.getlist('thong_ke'):
        thong_ke_ngay = thong_ke_theo_ngay(data)
    if 'thang' in request.GET.getlist('thong_ke'):
        thong_ke_thang = thong_ke_theo_thang(data)
    if 'nam' in request.GET.getlist('thong_ke'):
        thong_ke_nam = thong_ke_theo_nam(data)
    if 'quy' in request.GET.getlist('thong_ke'):
        thong_ke_quy = thong_ke_theo_quy(data)

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
        'thong_ke_ngay': thong_ke_ngay if 'ngay' in request.GET.getlist('thong_ke') else None,
        'thong_ke_thang': thong_ke_thang if 'thang' in request.GET.getlist('thong_ke') else None,
        'thong_ke_nam': thong_ke_nam if 'nam' in request.GET.getlist('thong_ke') else None,
        'thong_ke_quy': thong_ke_quy if 'quy' in request.GET.getlist('thong_ke') else None,
    }
    return render(request, 'home/trangchu.html', context)


def thong_ke_theo_ngay(data):
    thong_ke = {}
    for ngay in data:
        ngay_str = ngay.strftime('%Y-%m-%d')  # Chuyển đổi ngày thành chuỗi định dạng năm-tháng-ngày
        if ngay_str not in thong_ke:
            thong_ke[ngay_str] = 0
        thong_ke[ngay_str] += 1
    return thong_ke

def thong_ke_theo_thang(data):
    thong_ke = {}
    for ngay in data:
        thang = ngay.strftime('%Y-%m')  # Định dạng năm-tháng
        if thang not in thong_ke:
            thong_ke[thang] = 0
        thong_ke[thang] += 1
    return thong_ke

def thong_ke_theo_nam(data):
    thong_ke = {}
    for ngay in data:
        nam = ngay.strftime('%Y')
        if nam not in thong_ke:
            thong_ke[nam] = 0
        thong_ke[nam] += 1
    return thong_ke

def thong_ke_theo_quy(data):
    thong_ke = {}
    for ngay in data:
        nam = ngay.strftime('%Y')
        thang = int(ngay.strftime('%m'))
        quy = (thang - 1) // 3 + 1
        quy_nam = f"Q{quy}-{nam}"
        if quy_nam not in thong_ke:
            thong_ke[quy_nam] = 0
        thong_ke[quy_nam] += 1
    return thong_ke

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
    # Kiểm tra nếu user đã đăng nhập
    if request.user.is_authenticated:
        return redirect('trangchu')
    
    # Khởi tạo form captcha

    if request.method == 'POST':
        # Xác thực captcha trước
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if username and password:
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    # Kiểm tra không cho phép admin đăng nhập
                    if user.is_staff or user.is_superuser:
                        messages.error(request, 'Tài khoản quản trị không được phép đăng nhập tại đây!')
                        return render(request, 'home/dangnhap.html')
                    
                    # Đăng nhập thành công
                    login(request, user)
                    messages.success(request, 'Đăng nhập thành công!')
                    return redirect('trangchu')
                else:
                    messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
            else:
                messages.error(request, 'Vui lòng nhập đầy đủ thông tin đăng nhập!')
        

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
    if request.method == 'POST':
    
        user = request.user
        user.phone = request.POST.get('phone', '')
        user.address = request.POST.get('address', '')
        user.birth_date = request.POST.get('birth_date', None)
        user.save()
        messages.success(request, 'Cập nhật thông tin thành công!')
        return redirect('trangchu')
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
    bao_tri_list = Baotri.objects.select_related('matb').annotate(
        tentb = F('matb__tentb')
    ).all()
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
    # Lấy danh sách bảng lương với thông tin nhân viên
    bang_luong_list = (Bangluong.objects
        .select_related('manv')
        .annotate(
            tennv=F('manv__hoten'),
            thang=F('thangluong__month'),
            nam=F('thangluong__year')
        )
        .order_by('-thangluong', 'manv__hoten'))  # Sắp xếp theo tháng mới nhất và tên nhân viên

    # Xử lý tìm kiếm và lọc
    search = request.GET.get('search', '').strip()
    gia = request.GET.get('gia')
    thang = request.GET.get('thang')
    nam = request.GET.get('nam')

    # Lọc theo khoảng lương
    if gia:
        try:
            min_gia, max_gia = map(int, gia.split('-'))
            bang_luong_list = bang_luong_list.filter(
                tongluong__gte=min_gia, 
                tongluong__lte=max_gia
            )
        except ValueError:
            messages.error(request, "Định dạng khoảng lương không hợp lệ")

    # Lọc theo tháng năm nếu có
    if thang and nam:
        try:
            bang_luong_list = bang_luong_list.filter(
                thangluong__month=int(thang),
                thangluong__year=int(nam)
            )
        except ValueError:
            messages.error(request, "Tháng năm không hợp lệ")

    # Tìm kiếm theo nhiều tiêu chí
    if search:
        bang_luong_list = bang_luong_list.filter(
            Q(maluong__icontains=search) |
            Q(manv__hoten__icontains=search) |  # Tìm theo tên nhân viên
            Q(manv__manv__icontains=search) |   # Tìm theo mã nhân viên
            Q(sogio__icontains=search) |
            Q(luongcoban__icontains=search)
        )

    # Xử lý thêm mới bảng lương
    if request.method == "POST":
        bl = nhap_luongnhanvien(request.POST)
        if bl.is_valid():
            try:
                thangluong = bl.cleaned_data['thangluong']
                manv = bl.cleaned_data['manv']
                
                # Kiểm tra bảng lương đã tồn tại
                existing_luong = Bangluong.objects.filter(
                    manv=manv,
                    thangluong__month=thangluong.month,
                    thangluong__year=thangluong.year
                ).first()
                
                if existing_luong:
                    messages.error(
                        request, 
                        f"Đã tồn tại bảng lương của nhân viên {manv.hoten} trong tháng {thangluong.month}/{thangluong.year}"
                    )
                else:
                    # Tính tổng số giờ làm từ bảng ca làm
                    calam_trong_thang = Calam.objects.filter(
                        manv=manv,
                        ngay__month=thangluong.month,
                        ngay__year=thangluong.year
                    )
                    
                    tong_gio = 0
                    for ca in calam_trong_thang:
                        # Chuyển giờ bắt đầu và kết thúc thành datetime để tính toán
                        giobd = datetime.combine(ca.ngay, ca.giobd)
                        giokt = datetime.combine(ca.ngay, ca.giokt)
                        # Tính số giờ làm trong ca (kết quả là số giờ dạng float)
                        so_gio_lam = (giokt - giobd).total_seconds() / 3600
                        tong_gio += so_gio_lam
                    
                    # Tạo instance của Bangluong nhưng chưa lưu
                    bangluong = bl.save(commit=False)
                    # Gán số giờ đã tính được
                    bangluong.sogio = round(tong_gio, 2)  # Làm tròn 2 chữ số thập phân
                    # Lưu vào database
                    bangluong.save()
                    
                    messages.success(
                        request, 
                        f"Đã thêm bảng lương thành công cho nhân viên {manv.hoten}"
                    )
                    return redirect('bangluong')
            except Exception as e:
                messages.error(request, f"Lỗi khi lưu bảng lương: {str(e)}")
    else:
        bl = nhap_luongnhanvien()

    # Chuẩn bị context cho template
    context = {
        'bang_luong_list': bang_luong_list,
        'bl': bl,
        'bangluong': None,
        'search': search,
        'gia': gia,
        'thang': thang,
        'nam': nam,
        # Thêm danh sách tháng và năm cho bộ lọc
        'months': range(1, 13),
        'years': range(datetime.now().year - 2, datetime.now().year + 1),
    }

    return render(request, 'home/luongnhanvien.html', context)

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
    nghi_phep_list = Nghiphep.objects.select_related('manv').annotate(
        tennv = F('manv__hoten')
    ).all()
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
            return redirect('socalam')
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

def nhan_vien_sua(request):
    nhanviens = Nhanvien.objects.all()
    return render(request, 'home/socalam.html', {'nhanviens': nhanviens})   

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
    if request.method != "POST":
        return render(request, 'home/thongtinnhanvien.html')
        
    if 'file' not in request.FILES:
        messages.error(request, 'Vui lòng chọn file Excel để import')
        return redirect('thongtinnhanvien')
        
    try:
        excel_file = request.FILES['file']
        # Kiểm tra file có phải Excel không
        if not excel_file.name.endswith(('.xls', '.xlsx')):
            messages.error(request, 'Vui lòng upload file Excel (.xls, .xlsx)')
            return redirect('thongtinnhanvien')
            
        df = pd.read_excel(excel_file)
        
        # Kiểm tra các cột bắt buộc
        required_columns = ['Họ tên', 'Ngày sinh', 'Số điện thoại', 'Địa chỉ', 'Ngày vào làm', 'Vị trí công việc', 'Trạng thái']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            messages.error(request, f'Thiếu các cột: {", ".join(missing_cols)}')
            return redirect('thongtinnhanvien')

        success_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                Nhanvien.objects.create(
                    hoten = row['Họ tên'].strip(),  # Thêm strip() để xóa khoảng trắng
                    ngaysinh = row['Ngày sinh'],
                    sdt = str(row['Số điện thoại']).strip(),
                    diachi = row['Địa chỉ'],
                    ngayvaolam = row['Ngày vào làm'],
                    vitricongviec = row['Vị trí công việc'],
                    trangthai = row['Trạng thái']
                )
                success_count += 1
            except Exception as e:
                errors.append(f'Lỗi ở dòng {index + 2}: {str(e)}')
                
        if errors:
            for error in errors:
                messages.error(request, error)
                
        if success_count > 0:
            messages.success(request, f'Import thành công {success_count} bản ghi')
        
    except Exception as e:
        messages.error(request, f'Import thất bại: {str(e)}')
        
    return redirect('thongtinnhanvien')