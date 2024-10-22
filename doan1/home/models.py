from django.db import models

# Create your models here.,...


class Calam(models.Model):
    macalam = models.CharField(max_length=10, primary_key=True)
    manv = models.CharField(max_length=10)
    ngay = models.DateField()
    giobd = models.TimeField()
    giokt = models.TimeField()
    
    class Meta:  
        db_table = 'calam'
        
        
        
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
     hoten = models.CharField(max_length=10)
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
    loaibt = models.CharField(max_length=20)
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
    gia = models.FloatField()
    dvt = models.CharField(max_length=10)
    soluong = models.FloatField()
    ngayhethan = models.DateField()
    
    class Meta:
        db_table = 'nguyenlieu'
        
