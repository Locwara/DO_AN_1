from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Danh sách các URL không cần xác thực
        public_urls = [
            reverse('login'),
            reverse('register'),
            # Thêm các URL khác không cần đăng nhập vào đây
        ]

        # Kiểm tra nếu user chưa đăng nhập và không ở trong public_urls
        if not request.user.is_authenticated and request.path not in public_urls:
            return redirect('login')  # Chuyển hướng đến trang đăng nhập

        response = self.get_response(request)
        return response
