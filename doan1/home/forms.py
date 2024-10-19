from .models import Calam
from django import forms
from .models import Baotri
from .models import Dungcu
class nhap_calam(forms.ModelForm):
    class Meta:
        model = Calam
        fields = ['macalam', 'manv', 'ngay', 'giobd', 'giokt']
        widgets = {
            'macalam': forms.TextInput(attrs={'placeholder': 'Mã ca làm'}),
            'manv': forms.TextInput(attrs={'placeholder': 'Mã nhân viên'}),
            'ngay': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Ngày'}),
            'giobd': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Giờ bắt đầu'}),
            'giokt': forms.TimeInput(attrs={'type': 'time','placeholder': 'Giờ kết thúc'}),
        }
        
        
class nhap_baotri(forms.ModelForm):
    class Meta:
        model = Baotri
        fields = ['mabt', 'matb', 'ngaybt', 'mota', 'chiphi', 'nguoithuchien']
        widgets = {
            'mabt': forms.TextInput(attrs={'placeholder': 'Mã bảo trì'}),
            'matb': forms.TextInput(attrs={'placeholder': 'Mã thiết bị'}),
            'ngaybt': forms.DateInput(attrs={'type' : 'date', 'placeholder': 'Ngày bảo trì'}),
            'mota': forms.DateInput(attrs={'placeholder': 'Mô tả'}),
            'chiphi': forms.DateInput(attrs={'placeholder': 'Chi phí'}),
            'nguoithuchien': forms.DateInput(attrs={'placeholder': 'Người thực hiện'}),
        }
        
