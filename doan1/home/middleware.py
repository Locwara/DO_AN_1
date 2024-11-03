# home/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Debug prints
        print(f"Current path: {request.path}")
        print(f"Is authenticated: {request.user.is_authenticated}")
        
        public_urls = [
            reverse('login'),
            reverse('loginql'),
            reverse('register'),
            reverse('index'),
            '/admin/',
            '/static/',
            '/media/',
        ]

        is_public = any(request.path.startswith(url) for url in public_urls)

        if not is_public and not request.user.is_authenticated:
            print("Redirecting to index because not authenticated and not public URL")
            return redirect('index') 
        
        response = self.get_response(request)
        return response