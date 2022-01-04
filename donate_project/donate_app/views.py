from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator

from donate_app.forms import RegisterForm
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
        # count all organisations
        supported_org = Institution.objects.all().count()

        # count all bags donated
        donations = Donation.objects.all()
        for donation in donations:
            bag_count += donation.quantity

        foundation = Institution.objects.filter(type=1)
        # fun_paginator = Paginator(foundation_list, 1)

        organization = Institution.objects.filter(type=2)
        # org_paginator = Paginator(organization_list, 1)

        local_collection = Institution.objects.filter(type=3)
        # loc_paginator = Paginator(local_collection_list, 1)

        # TODO: Pagination
        # fun_page = request.GET.get('page')
        # org_page = request.GET.get('page2')
        # loc_page = request.GET.get('page3')
        #
        # foundations = fun_paginator.get_page(fun_page)
        # organization = org_paginator.get_page(org_page)
        # local_collection = loc_paginator.get_page(loc_page)


        return render(
            request,
            'index.html',
            context={
                'supported': supported_org,
                'bag_count': bag_count,
                'foundation': foundation,
                'organization': organization,
                'local_collection': local_collection,
            },
        )


class RegisterView(View):
    """
    Class creating registration page view.
    """
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['email'],
                first_name=form.cleaned_data['name'],
                last_name=form.cleaned_data['surname'],
                email=form.cleaned_data['email'],
            )
            user.password = make_password(form.cleaned_data['password'])
            user.save()

            return redirect('/login/')
        return render(request, 'register.html', {'form': form})


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
