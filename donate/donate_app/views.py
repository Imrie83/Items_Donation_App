from django.shortcuts import render
from django.views import View


class LandingPageView(View):
    """
    Class creating landing page view.
    """
    def get(self, request):
        return render(request, 'index.html')


class RegisterView(View):
    """
    Class creating registration page view.
    """
    def get(self, request):
        return render(request, 'register.html')


class LoginView(View):
    """
    Class creating logi in page view.
    """
    def get(self, request):
        return render(request, 'login.html')


class AddDonationView(View):
    """
    Class creating donation page view.
    """
    def get(self, request):
        return render(request, 'form.html')
