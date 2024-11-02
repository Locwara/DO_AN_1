from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
# Create your models here.,...


class Calam(models.Model):
    macalam = models.CharField(max_length=10, primary_key=True)
    manv = models.ForeignKey('Nhanvien', on_delete=models.CASCADE, db_column='manv')
    ngay = models.DateField()
    giobd = models.TimeField()
    giokt = models.TimeField()
    
    class Meta:  
        db_table = 'calam'
        

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username là bắt buộc')
        if not email:
            raise ValueError('Email là bắt buộc')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)

    # Thêm manager vào đây
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
        
class Nghiphep(models.Model):
    manp = models.CharField(max_length=10, primary_key=True)
    manv = models.CharField(max_length=10)
    ngaybd = models.DateField()
    ngaykt = models.DateField()
    lydonghi = models.CharField(max_length=50)
    trangthai = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'nghiphep'
        
        
class Bangluong(models.Model):
    maluong = models.CharField(max_length=10, primary_key=True)
    manv = models.CharField(max_length=10)
    sogio = models.FloatField()
    luongcoban = models.FloatField()
    tongluong = models.FloatField()

    class Meta:
        db_table = 'bangluong'
        
class Nhanvien(models.Model):
     manv = models.CharField(max_length=10, primary_key=True)
     hoten = models.CharField(max_length=30)
     ngaysinh = models.DateField()
     sdt = models.IntegerField()
     diachi = models.CharField(max_length=70)
     ngayvaolam = models.DateField()
     vitricongviec = models.CharField(max_length=20)
     trangthai = models.CharField(max_length=20)
     class Meta:
         db_table = 'nhanvien'


class Thietbi(models.Model):
    matb = models.CharField(max_length=10, primary_key=True)
    tentb = models.CharField(max_length=50)
    loaitb = models.CharField(max_length=20)
    soluong =models.FloatField()
    tinhtrang =models.CharField(max_length=20)
    ngaymua =models.DateField()
    giamua=models.FloatField()
    class Meta:
        db_table = 'thietbi'

class Baotri(models.Model):
    mabt = models.CharField(max_length=10, primary_key=True)
    matb = models.CharField(max_length=10)
    ngaybt=models.DateField()
    mota =models.CharField(max_length=100)
    chiphi=models.FloatField()
    nguoithuchien=models.CharField(max_length=50)
    class Meta:
        db_table = 'baotri'

class Dungcu(models.Model):
    madc = models.CharField(max_length=10, primary_key=True)
    tendc = models.CharField(max_length=50)
    soluong =models.IntegerField()
    dvt = models.CharField(max_length=20)
    ngaymua=models.DateField()
    giamua=models.FloatField()
    class Meta:
        db_table = 'dungcu'

class Thongtinnguyenlieu(models.Model):
    manl = models.CharField(max_length=10, primary_key=True)
    tennl = models.CharField(max_length=30)
    dvt = models.CharField(max_length=10)
    soluong = models.FloatField()
    gia = models.FloatField()
    ngayhethan = models.DateField()
    
    class Meta:
        db_table = 'nguyenlieu'
        
