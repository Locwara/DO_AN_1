# Generated by Django 4.2 on 2024-11-06 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bangluong',
            fields=[
                ('maluong', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('manv', models.CharField(max_length=10)),
                ('sogio', models.FloatField()),
                ('luongcoban', models.FloatField()),
                ('tongluong', models.FloatField()),
            ],
            options={
                'db_table': 'bangluong',
            },
        ),
        migrations.CreateModel(
            name='Baotri',
            fields=[
                ('mabt', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('matb', models.CharField(max_length=10)),
                ('ngaybt', models.DateField()),
                ('mota', models.CharField(max_length=100)),
                ('chiphi', models.FloatField()),
                ('nguoithuchien', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'baotri',
            },
        ),
        migrations.CreateModel(
            name='Dungcu',
            fields=[
                ('madc', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('tendc', models.CharField(max_length=50)),
                ('soluong', models.IntegerField()),
                ('dvt', models.CharField(max_length=20)),
                ('ngaymua', models.DateField()),
                ('giamua', models.FloatField()),
            ],
            options={
                'db_table': 'dungcu',
            },
        ),
        migrations.CreateModel(
            name='Nghiphep',
            fields=[
                ('manp', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('manv', models.CharField(max_length=10)),
                ('ngaybd', models.DateField()),
                ('ngaykt', models.DateField()),
                ('lydonghi', models.CharField(max_length=50)),
                ('trangthai', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'nghiphep',
            },
        ),
        migrations.CreateModel(
            name='Nhanvien',
            fields=[
                ('manv', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('hoten', models.CharField(max_length=30)),
                ('ngaysinh', models.DateField()),
                ('sdt', models.IntegerField()),
                ('diachi', models.CharField(max_length=70)),
                ('ngayvaolam', models.DateField()),
                ('vitricongviec', models.CharField(max_length=20)),
                ('trangthai', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'nhanvien',
            },
        ),
        migrations.CreateModel(
            name='Thietbi',
            fields=[
                ('matb', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('tentb', models.CharField(max_length=50)),
                ('loaitb', models.CharField(max_length=20)),
                ('soluong', models.FloatField()),
                ('tinhtrang', models.CharField(max_length=20)),
                ('ngaymua', models.DateField()),
                ('giamua', models.FloatField()),
            ],
            options={
                'db_table': 'thietbi',
            },
        ),
        migrations.CreateModel(
            name='Thongtinnguyenlieu',
            fields=[
                ('manl', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('tennl', models.CharField(max_length=30)),
                ('dvt', models.CharField(max_length=10)),
                ('soluong', models.FloatField()),
                ('gia', models.FloatField()),
                ('ngayhethan', models.DateField()),
            ],
            options={
                'db_table': 'nguyenlieu',
            },
        ),
        migrations.CreateModel(
            name='Calam',
            fields=[
                ('macalam', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('ngay', models.DateField()),
                ('giobd', models.TimeField()),
                ('giokt', models.TimeField()),
                ('manv', models.ForeignKey(db_column='manv', on_delete=django.db.models.deletion.CASCADE, to='home.nhanvien')),
            ],
            options={
                'db_table': 'calam',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=40, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
