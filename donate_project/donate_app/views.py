import os
import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, mail_admins
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator

from donate_app.forms import RegisterForm, EditUserForm
from donate_app.models import (
    Institution,
    Donation,
    Category, ActivationTokenModel,
)


def send_email(request):
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    msg = request.POST.get('message')

    mail_admins(
        subject='Visitor Message',
        message=f'From: {name} {surname}\n'
                f'{msg}'
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

    def post(self, request):
        send_email(request)

        return redirect('/')


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
                is_active=False,
            )
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            activation_token = uuid.uuid4()
            user_activation = ActivationTokenModel.objects.create(
                user=user,
                active_token=activation_token,
            )
            emai_body = (f'Click on this link to activate your account '
                         f'{request.get_host()}/activate/{activation_token}/')
            send_mail(
                'Account activation',
                emai_body,
                'site_admin@donations.com',
                [user.email],
            )

            return redirect('/login/')
        return render(request, 'register.html', {'form': form})


class ActivationView(View):
    def get(self, request, code):
        activate_user = ActivationTokenModel.objects.filter(
            active_token__exact=code,
        )
        if activate_user.exists():
            try:
                edit_user = User.objects.get(id=activate_user[0].user.pk)
            except ObjectDoesNotExist:
                msg = 'U??ytkownik nie zosta?? znaleziony w bazie danych!'
                return render(request, 'activation_complete.html', context={
                    'msg': msg,
                })
            edit_user.is_active = True
            edit_user.save()
            activate_user.delete()

            msg = 'Konto aktywowane pomy??lnie.'
            return render(request, 'activation_complete.html', context={
                'msg': msg,
            })
        else:
            msg = '''Konto zosta??o aktywowane u??ywaj??c tego linka. 
                  Je??li twoje konto nie jest aktywne skontaktuj si??
                  z administratorem strony'''
            return render(request, 'activation_complete.html', context={
                'msg': msg,
            })



class ActivationCompleteView(View):
    def get(self, request):
        return render(request, 'activation_complete.html')


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
            user_check = authenticate(
                username=user,
                password=form.cleaned_data['old_password'],
            )

            if user_check:
                user.email = form.cleaned_data['email']
                user.last_name = form.cleaned_data['surname']
                user.first_name = form.cleaned_data['name']
                if form.cleaned_data['new_password']:
                    user.password = make_password(
                        form.cleaned_data['new_password']
                    )
                user.save()
            return redirect('/')

        return render(
            request,
            'edit-user.html',
            context={'form': form},
        )
