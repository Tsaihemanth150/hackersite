"""hackersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('polls.urls')),
    path('admin/', admin.site.urls),

    ##################### Aunthntications #############################################################################
    path('customeroptions', views.customeroptions_view,name='customeroptions'),
    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customerlogin', LoginView.as_view(template_name='polls/adminlogin.html'),name='customerlogin'),

    path('change_password', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('password_change_done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    ###################################################################################################################

    path('customer-dashboard', views.customer_dashboard_view, name='customer-dashboard'),
    path('myprofile', views.customer_profile_view, name='myprofile'),
    path('addprofile', views.addpofile_view, name='addprofile'),
    path('update-profile', views.upade_profile_view, name='update-profile'),
    path('apply-course', views.apply_course_view,name='apply-course'),
    path('apply/<int:pk>', views.apply_view,name='apply'),
    path('history', views.history_view,name='history'),
    path('ask-question', views.ask_question_view, name='ask-question'),
    path('question-history', views.question_history_view, name='question-history'),




]