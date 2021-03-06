"""donate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from donate_app.views import (
    LandingPageView,
    RegisterView,
    LoginView,
    AddDonationView,
    LogoutView,
    ConfirmationView,
    UserPageView,
    EditUserView,
    ActivationView,
    ActivationCompleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('donate/', AddDonationView.as_view(), name='donation'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('user_page/', UserPageView.as_view(), name='user_page'),
    path('edit-user/', EditUserView.as_view(), name='edit-user'),
    path('activate/<str:code>/', ActivationView.as_view(), name='activate'),
    path('activation_complete/', ActivationCompleteView.as_view(),
         name='activation_complete'),

]
