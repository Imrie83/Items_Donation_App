from django.shortcuts import render
from django.views import View

from donate_app.models import (
    Institution,
    Donation,
)


class LandingPageView(View):
    """
    Class creating landing page view.
    """
    def get(self, request):

        bag_count = 0
        supported_org = Institution.objects.all().count()

        donations = Donation.objects.all()
        for donation in donations:
            bag_count += donation.quantity

        foundations = Institution.objects.filter(type=1)
        organization = Institution.objects.filter(type=2)
        local_collection = Institution.objects.filter(type=3)

        return render(
            request,
            'index.html',
            context={
                'supported': supported_org,
                'bag_count': bag_count,
                'foundation': foundations,
                'organization': organization,
                'local_collection': local_collection,
            },
        )


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
