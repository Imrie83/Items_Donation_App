from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator

from donate_app.forms import RegisterForm, EditUserForm
from donate_app.models import (
    Institution,
    Donation, Category,
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

    def post(self, request):

        if not User.objects.filter(username=request.POST.get('email')).exists():
            return redirect('/register/')

        user = authenticate(
            username=request.POST.get('email'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login/')


class LogoutView(View):
    """
    Class creating a view allowing for user to logout
    """
    def get(self, request):
        logout(request)
        return redirect('/')


class AddDonationView(LoginRequiredMixin, View):
    """
    Class creating donation page view.
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(
            request,
            'form.html',
            context={
                'categories': categories,
                'institutions': institutions,
            })

    def post(self, request):
        current_user = request.user
        categories = request.POST.getlist('categories')
        quantity = request.POST.get('bags')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        date = request.POST.get('date')
        time = request.POST.get('time')
        comment = request.POST.get('more_info')
        institution = request.POST.get('organization')

        donation = Donation.objects.create(
            quantity=quantity,
            address=address,
            phone_number=phone,
            city=city,
            zip_code=postcode,
            pick_up_date=date,
            pick_up_time=time,
            pick_up_comment=comment,
            institution_id=institution,
            user=current_user,
        )
        donation.category.set(categories)

        return redirect('confirmation')


class ConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


class UserPageView(View):
    def get(self, request):
        donations = Donation.objects.filter(user=request.user).order_by(
            'is_taken',
            'pick_up_date',
            'pick_up_time',
        )

        return render(
            request,
            'user-page.html',
            context={'donations': donations}
        )

    def post(self, request):

        if request.POST['taken'][-1] == 'y':
            donation = Donation.objects.get(id=request.POST['taken'][:-1])
            donation.is_taken = True
            donation.save()

        elif request.POST['taken'][-1] == 'n':
            donation = Donation.objects.get(id=request.POST['taken'][:-1])
            donation.is_taken = False
            donation.save()

        donations = Donation.objects.filter(user=request.user).order_by(
            'is_taken',
            'pick_up_date',
            'pick_up_time',
        )

        return render(
            request,
            'user-page.html',
            context={'donations': donations}
        )

class EditUserView(View):
    def get(self, request):
        user = request.user
        form = EditUserForm(initial={
            'name': user.first_name,
            'surname': user.last_name,
            'email': user.email,
        })
        return render(
            request,
            'edit-user.html',
            context={'form': form},
        )

    def post(self, request):
        user = request.user
        form = EditUserForm(request.POST)

        if form.is_valid():
            return redirect('/')

        return render(
            request,
            'edit-user.html',
            context={'form': form},
        )
