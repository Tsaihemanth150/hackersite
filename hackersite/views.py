from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import generate_token
from django.contrib import messages
from . import forms, models, settings
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from polls import models as pmodel
from polls import forms as CFORM



def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

##################################### Authnentaction ##################################################################
def customeroptions_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hackersite/customeroptions.html')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm': userForm, 'customerForm': customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            ###################################################################
            # Welcome Email
            subject = "Welcome to hacker site!!"
            message = "Hello " + user.first_name + "!! \n" + "Welcome to Hacker site!! \nThank you for registering .\n Your Account has been successfully created !!! .\n You can login at http://127.0.0.1:8000/customerlogin. \n\nThanking You. \nTeam Hacker site."
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)


        return HttpResponseRedirect('customerlogin')
    return render(request,'hackersite/customersignup.html',context=mydict)



########################################DashBord#####################################################################
@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    dict={
        'customer':models.Customer.objects.get(user_id=request.user.id),
        'available_course': pmodel.Course.objects.all().count(),
        'applied_course': pmodel.CourseRecord.objects.all().filter(Customer=models.Customer.objects.get(user_id=request.user.id)).count(),
        'total_category': pmodel.Category.objects.all().count(),
        'total_question': pmodel.Question.objects.all().filter(customer=models.Customer.objects.get(user_id=request.user.id)).count(),

    }
    return render(request,'hackersite/customer_dashboard.html',context=dict)

def customer_profile_view(request):
    Customer = models.Customer.objects.get(user_id=request.user.id)
    Profile = pmodel.Profile.objects.all().filter(customer=Customer)
    return render(request,'hackersite/myprofile.html', {'Profile':Profile,' customer': Customer})

def apply_course_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    course = pmodel.Course.objects.all()
    return render(request,'hackersite/apply_course.html',{'course':course,'customer':customer})

def apply_view(request,pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    course = pmodel.Course.objects.get(id=pk)
    courserecord = pmodel.CourseRecord()
    courserecord.course = course
    courserecord.customer = customer
    courserecord.save()
    return redirect('history')

def history_view(request):
    Customer = models.Customer.objects.get(user_id=request.user.id)
    course = pmodel.CourseRecord.objects.all().filter( Customer= Customer)
    return render(request,'hackersite/history.html',{'course':course,' Customer': Customer})


def ask_question_view(request):
    Customer = models.Customer.objects.get(user_id=request.user.id)
    questionForm = CFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.customer = Customer
            question.save()
            return redirect('question-history')
    return render(request, 'hackersite/ask_question.html', {'questionForm': questionForm, 'Customer': Customer})

def question_history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questions = pmodel.Question.objects.all().filter(customer=customer)
    return render(request,'hackersite/question_history.html',{'questions':questions,'customer':customer})

def upade_profile_view(request):
    customer = models.Customer.objects.get(id=request.user.customer.id)
    user = models.User.objects.get(id=customer.user_id)
    userForm = forms.CustomerUserForm(instance=user)
    customerForm = forms.CustomerForm(request.FILES, instance=customer)
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, request.FILES, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('myprofile')
    return render(request,'hackersite/update_profile.html',context=mydict)

def addpofile_view(request):
    Customer = models.Customer.objects.get(user_id=request.user.id)
    ProfileForm = CFORM.ProfileForm()
    if request.method == 'POST':
        ProfileForm = CFORM.ProfileForm(request.POST)
        if ProfileForm.is_valid():

            question = ProfileForm.save(commit=False)
            question.customer = Customer
            question.save()
            return redirect('myprofile')

    return render(request, 'hackersite/add_profile.html', {'ProfileForm': ProfileForm, 'Customer': Customer})

#######################################################################################################################

