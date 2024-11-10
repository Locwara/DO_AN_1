# home/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # URLs công khai - không cần đăng nhập
        public_urls = [
            reverse('login'),
            reverse('loginql'),
            reverse('register'),
            reverse('index'),
            reverse('forgot_password'),
            '/admin/',
            '/static/',
            '/media/',
            '/captcha/',
        ]
        
        # URLs chỉ dành cho admin/superuser
        admin_only_urls = [
            reverse('thongtinnhanvien'),
            reverse('bangluong'),
            reverse('socalam'),
            reverse('nghiphep'),
            
        ]

        print(f"Request Path: {request.path}")
        print(f"Public URLs: {public_urls}")
        
        # Kiểm tra URL công khai    
        is_public = any(request.path == url for url in public_urls)
        
        # Nếu URL không công khai và người dùng chưa đăng nhập
        if not is_public and not request.user.is_authenticated:
            print("Redirecting to index because URL is not public and user is not authenticated.")
            return redirect('index')
        
        # Kiểm tra quyền truy cập cho URLs chỉ dành cho admin
        is_admin_url = any(request.path == url for url in admin_only_urls)
        if is_admin_url and not request.user.is_superuser:
            print("Redirecting to trangchu because URL is admin-only and user is not superuser.")
            return redirect('trangchu')

        return self.get_response(request)
