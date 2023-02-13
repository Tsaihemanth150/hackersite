from django.urls import path

from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('tools', views.tools_view),
    path('nmap',views.nmap_view),
    path('phone',views.phone_view),
    path('certification',views.certification_view),
    path('pentesting', views.pentesting_view),
    #path('adminlogin', views.adminlogin_view),
    path('topics', views.topics_view),
    path('digitalforensic', views.digitalforensic_view),
    path('cryptography', views.cryptography_view),
    path('cloudsecurity', views.cloudsecurity_view),
    path('price', views.price_view),
    path('t&c',views.tandc_view,name='t&c'),

    ### Controlers
    path('logout', LogoutView.as_view(template_name='polls/logout.html'),name='logout'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('adminlogin', LoginView.as_view(template_name='polls/adminlogin.html'),name='adminlogin'),


    #AdminPaths
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-category', views.admin_category_view, name='admin-category'),

    ###Customer
    path('admin-view-customer', views.admin_view_customer_view,name='admin-view-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view, name='delete-customer'),


    #Category
    path('admin-category', views.admin_category_view,name='admin-category'),
    path('admin-view-category', views.admin_view_category_view, name='admin-view-category'),
    path('admin-add-category', views.admin_add_category_view,name='admin-add-category'),
    path('admin-update-category', views.admin_update_category_view,name='admin-update-category'),
    path('update-category/<int:pk>', views.update_category_view,name='update-category'),
    path('admin-delete-category', views.admin_delete_category_view, name='admin-delete-category'),
    path('delete-category/<int:pk>', views.delete_category_view, name='delete-category'),
    path('admin-view-approved-course-holder', views.admin_view_approved_course_holder_view,name='admin-view-approved-course-holder'),

    ###Course
    path('admin-course', views.admin_course_view,name='admin-course'),
    path('admin-view-course', views.admin_view_course_view, name='admin-view-course'),
    path('admin-view-course-holder', views.admin_view_course_holder_view, name='admin-view-course-holder'),
    path('admin-add-course', views.admin_add_course_view, name='admin-add-course'),
    path('update-course/<int:pk>', views.update_course_view, name='update-course'),
    path('admin-update-course', views.admin_update_course_view,name='admin-update-course'),
    path('admin-delete-course', views.admin_delete_course_view, name='admin-delete-course'),
    path('delete-course/<int:pk>', views.delete_course_view, name='delete-course'),

    ## ADMIN Instructor
    path('admin-instructor', views.admin_instructor_view,name='admin-instructor'),
    path('admin-add-instructor', views.admin_add_instructor_view, name='admin-add-instructor'),
    path('admin-view-instructor', views.admin_view_instructor_view, name='admin-view-instructor'),
    path('admin-update-instructor', views.admin_update_instructor_view, name='admin-update-instructor'),
    path('update-instructor/<int:pk>', views.update_instructor_view,name='update-instructor'),
    path('admin-delete-instructor', views.admin_delete_instructor_view, name='admin-delete-instructor'),
    path('delete-instructor/<int:pk>', views.delete_instructor_view, name='delete-instructor'),


    ##Questions
    path('admin-question', views.admin_question_view, name='admin-question'),
    path('update-question/<int:pk>', views.update_question_view,name='update-question'),

    ##instructor
    path('instructor-dashboard', views.instructor_dashboard_view, name='instructor-dashboard'),





]