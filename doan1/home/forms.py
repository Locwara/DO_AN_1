from .models import CustomUser ,Calam, Baotri, Dungcu, Thongtinnguyenlieu, Bangluong, Nghiphep, Thietbi, Nhanvien
from django import forms
from django.contrib.auth.forms import UserCreationForm
class nhap_calam(forms.ModelForm):
    class Meta:
        model = Calam
        fields = ['macalam', 'manv', 'ngay', 'giobd', 'giokt']
        widgets = {
            'macalam': forms.TextInput(attrs={'placeholder': 'Mã ca làm'}),
            'manv': forms.Select(attrs={'placeholder': 'Chọn nhân viên'}),  # Thay đổi thành Select
            'ngay': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày'}),
            'giobd': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Giờ bắt đầu'}),
            'giokt': forms.TimeInput(attrs={'type': 'time','placeholder': 'Giờ kết thúc'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(nhap_calam, self).__init__(*args, **kwargs)
        self.fields['manv'].queryset = Nhanvien.objects.all()
        self.fields['manv'].label_from_instance = lambda obj: f"{obj.manv} - {obj.hoten}"
        

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone', 'address', 'birth_date', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Thêm các trường tùy chỉnh
        self.fields['phone'].widget.attrs.update({'class': 'input', 'placeholder': 'Số điện thoại'})
        self.fields['address'].widget.attrs.update({'class': 'input', 'placeholder': 'Địa chỉ'})
        self.fields['birth_date'].widget.attrs.update({'class': 'input', 'type': 'date'})
        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder': 'Email'})
class nhap_baotri(forms.ModelForm):
    class Meta:
        model = Baotri
        fields = ['mabt', 'matb', 'ngaybt', 'mota', 'chiphi', 'nguoithuchien']
        widgets = {
            'mabt': forms.TextInput(attrs={'placeholder': 'Mã bảo trì'}),
            'matb': forms.TextInput(attrs={'placeholder': 'Mã thiết bị'}),
            'ngaybt': forms.DateInput(attrs={'type' : 'date', 'placeholder': 'Ngày bảo trì'}),
            'mota': forms.TextInput(attrs={'placeholder': 'Mô tả'}),
            'chiphi': forms.TextInput(attrs={'placeholder': 'Chi phí'}),
            'nguoithuchien': forms.TextInput(attrs={'placeholder': 'Người thực hiện'}),
        }
        
class nhap_dungcu(forms.ModelForm):
    class Meta:
        model = Dungcu
        fields = ['madc', 'tendc', 'soluong', 'dvt', 'ngaymua', 'giamua']
        widgets = {
            'madc': forms.TextInput(attrs={'placeholder': 'Mã dụng cụ'}),
            'tendc': forms.TextInput(attrs={'placeholder': 'Tên dụng cụ'}),
            'soluong': forms.TextInput(attrs={'placeholder': 'Số lượng'}),
            'dvt': forms.TextInput(attrs={'placeholder': 'Đơn vị tính'}),
            'ngaymua': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày mua'}),
            'giamua': forms.TextInput(attrs={'placeholder': 'Giá mua'}),
        }
class nhap_luongnhanvien(forms.ModelForm):
    class Meta:
        model = Bangluong
        fields = ['maluong', 'manv', 'sogio', 'luongcoban', 'tongluong']
        widgets = {
            'maluong': forms.TextInput(attrs={'placeholder': 'Mã lương'}),
            'manv': forms.TextInput(attrs={'placeholder': 'Mã nhân viên'}),
            'sogio': forms.TextInput(attrs={'placeholder': 'Số giờ'}),
            'luongcoban': forms.TextInput(attrs={'placeholder': 'Lương cơ bản'}),
            'tongluong': forms.TextInput(attrs={'placeholder': 'Tổng lương'}),
        }

class nhap_nghiphep(forms.ModelForm):
    class Meta:
        model = Nghiphep
        fields = ['manp', 'manv', 'ngaybd', 'ngaykt', 'lydonghi', 'trangthai']
        widgets = {
            'manp': forms.TextInput(attrs={'placeholder': 'Mã nghỉ phép'}),
            'manv': forms.TextInput(attrs={'placeholder': 'Mã nhân viên'}),
            'ngaybd': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày bắt đầu'}),
            'ngaykt': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày kết thúc'}),
            'lydonghi': forms.TextInput(attrs={'placeholder': 'Lý do nghỉ'}),
            'trangthai': forms.TextInput(attrs={'placeholder': 'Trạng thái'}),
        }
class nhap_thietbi(forms.ModelForm):
    class Meta:
        model = Thietbi
        fields = ['matb', 'tentb', 'loaitb', 'soluong', 'tinhtrang', 'ngaymua', 'giamua']
        widgets = {
            'matb': forms.TextInput(attrs={'placeholder': 'Mã thiết bị'}),
            'tentb': forms.TextInput(attrs={'placeholder': 'Tên thiết bị'}),
            'loaitb': forms.TextInput(attrs={'placeholder': 'Loại thiết bị'}),
            'soluong': forms.TextInput(attrs={'placeholder': 'Số lượng'}),
            'tinhtrang': forms.TextInput(attrs={'placeholder': 'Tình trạng'}),
            'ngaymua': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày mua'}),
            'giamua': forms.TextInput(attrs={'placeholder': 'Giá mua'}),
        }
class nhap_nhanvien(forms.ModelForm):
    class Meta:
        model = Nhanvien
        fields = ['manv', 'hoten', 'ngaysinh', 'sdt', 'diachi', 'ngayvaolam', 'vitricongviec', 'trangthai']
        widgets = {
            'manv': forms.TextInput(attrs={'placeholder': 'Mã nhân viên'}),
            'hoten': forms.TextInput(attrs={'placeholder': 'Họ tên'}),
            'ngaysinh': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày sinh'}),
            'sdt': forms.TextInput(attrs={'placeholder': 'Số điện thoại'}),
            'diachi': forms.TextInput(attrs={'placeholder': 'Địa chỉ'}),
            'ngayvaolam': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày vào làm'}),
            'vitricongviec': forms.TextInput(attrs={'placeholder': 'Vị trí công việc'}),
            'trangthai': forms.TextInput(attrs={'placeholder': 'Trạng thái'}),
        }
class nhap_thongtinnguyenlieu(forms.ModelForm):
    class Meta:
        model = Thongtinnguyenlieu
        fields = ['manl', 'tennl', 'gia', 'dvt', 'soluong', 'ngayhethan']
        widgets = {
            'manl': forms.TextInput(attrs={'placeholder': 'Mã nguyên liệu'}),
            'tennl': forms.TextInput(attrs={'placeholder': 'Tên nguyên liệu'}),
            'gia': forms.TextInput(attrs={'placeholder': 'Giá'}),
            'dvt': forms.TextInput(attrs={'placeholder': 'Đơn vị tính'}),
            'soluong': forms.TextInput(attrs={'placeholder': 'Số lượng'}),
            'ngayhethan': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày hết hạn'}),
        }
        
class nhap_khonguyenlieu(forms.ModelForm):
    class Meta:
        model = Thongtinnguyenlieu
        fields = ['manl', 'tennl', 'dvt', 'soluong']
        widgets = {
            'manl': forms.TextInput(attrs={'placeholder': 'Mã nguyên liệu'}),
            'tennl': forms.TextInput(attrs={'placeholder': 'Tên nguyên liệu'}),
            'dvt': forms.TextInput(attrs={'placeholder': 'Đơn vị tính'}),
            'soluong': forms.TextInput(attrs={'placeholder': 'Số lượng'}),
        }
        
        
        
class nhap_nguyenlieu(forms.ModelForm):
    class Meta:
        model = Thongtinnguyenlieu
        fields = ['manl', 'tennl', 'gia', 'ngayhethan']
        widgets = {
            'manl': forms.TextInput(attrs={'placeholder': 'Mã nguyên liệu'}),
            'tennl': forms.TextInput(attrs={'placeholder': 'Tên nguyên liệu'}),
            'gia': forms.TextInput(attrs={'placeholder': 'Giá'}),
            'ngayhethan': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày hết hạn'}),
        }
             
