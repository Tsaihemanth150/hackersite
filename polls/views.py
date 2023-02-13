import phonenumbers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from . import forms, models
from django.contrib import messages
import functools
import operator
from .models import models as CMODEL
from phonenumbers import geocoder, carrier, timezone
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,reverse
from hackersite import models as CMODEL
from hackersite import forms as CFORM



def index(request):
    if request.user.is_authenticated:
     return HttpResponseRedirect('afterlogin')
    return render(request, 'polls/index.html')

def aboutus_view(request):
    return render(request,'polls/aboutus.html')
def tools_view(request):
    return render(request,'polls/tools.html')
def nmap_view(request):
    return render(request,'polls/nmap.html')
def certification_view(request):
    return render(request, 'polls/certification.html')
def pentesting_view(request):
    return render(request, 'polls/pentesting.html')

def topics_view(request):
    return  render(request,'polls/topics.html')
def digitalforensic_view(request):
    return  render(request,'polls/digitalforensics.html')
def cryptography_view(request):
    return  render(request,'polls/cryptography.html')
def cloudsecurity_view(request):
    return  render(request,'polls/cloudsecurity.html')


@login_required(login_url='customerlogin')
def phone_view(request):
    if request.method == "POST":
        num1 = request.POST['num']
        num2 = phonenumbers.parse(num1,"CH")
        num3 = geocoder.description_for_number(num2, "en")
        num4 = carrier.name_for_number(num2,"en")
        timeZone = timezone.time_zones_for_number(num2)  # for the TimeZone
        valid = phonenumbers.is_valid_number(num2)  ## for Validating a phone number
        possible = phonenumbers.is_possible_number(num2)
        data={
            'num1':num3,
            'num2':num4,
            'num3':timeZone,
            'num4':valid,
            'num5':possible
        }
        return render(request,'polls/phone.html',data)
    else:
        return render(request,'polls/phone.html')

def tandc_view(request):
    return render(request,'polls/t&c.html')

def contactus_view(request):
    context = {
        "captcha": forms,
    }

    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'polls/contactussuccess.html')
    return render(request, 'polls/contactus.html', {'form':sub})

@login_required(login_url='customerlogin')
def price_view(request):
    Course = models.Course.objects.all()
    return render(request,'polls/price.html',{'Course':Course})

################# Authtication_View ###########################

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

def afterlogin_view(request):
    if is_customer(request.user):
        messages.success(request, 'Hello welcome to hackersite')
        return redirect('customer-dashboard')
    else:
        messages.success(request, 'Hello welcome ADMIN !!!')
        return redirect('admin-dashboard')

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')






####### Admin Dadhbord ################################

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
        'total_user': CMODEL.Customer.objects.all().count(),
        'total_course': models.Course.objects.all().count(),
        'total_category': models.Category.objects.all().count(),
        'total_course_holder': models.CourseRecord.objects.all().count(),
        'approved_course_holder': models.CourseRecord.objects.all().filter(status='Approved').count(),
        'disapproved_course_holder': models.CourseRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_course_holder': models.CourseRecord.objects.all().filter(status='Pending').count(),
        'total_question': models.Question.objects.all().count(),
        'total_instructor':models.Instructor.objects.all().count(),
    }
    return render(request,'polls/admin_dashboard.html',context=dict)

################################### Customer ##########################################################################
def admin_view_customer_view(request):
    customers= CMODEL.Customer.objects.all()
    return render(request,'polls/admin_view_customer.html',{'customers':customers})

def update_customer_view(request,pk):
    customer = CMODEL.Customer.objects.get(id=pk)
    user = CMODEL.User.objects.get(id=customer.user_id)
    userForm = CFORM.CustomerUserForm(instance=user)
    customerForm = CFORM.CustomerForm(request.FILES, instance=customer)
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = CFORM.CustomerUserForm(request.POST, instance=user)
        customerForm = CFORM.CustomerForm(request.POST, request.FILES, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request, 'polls/update_customer.html', context=mydict)


def delete_customer_view(request, pk):
    customer = CMODEL.Customer.objects.get(id=pk)
    user = User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')



########################################## Category ###################################################################
def admin_category_view(request):
    return render(request,'polls/admin_category.html')

def admin_category_view(request):
    return render(request,'polls/admin_category.html')

def admin_view_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'polls/admin_view_category.html',{'categories':categories})

def admin_add_category_view(request):
    categoryForm=forms.CategoryForm()
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-view-category')
    return render(request,'polls/admin_add_category.html',{'categoryForm':categoryForm})

@login_required(login_url='adminlogin')
def admin_update_category_view(request):
    categories = models.Category.objects.all()
    return render(request, 'polls/admin_update_category.html', {'categories': categories})



def update_category_view(request, pk):
    category = models.Category.objects.get(id=pk)
    categoryForm = forms.CategoryForm(instance=category)

    if request.method == 'POST':
        categoryForm = forms.CategoryForm(request.POST, instance=category)

        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-update-category')
    return render(request, 'polls/update_category.html', {'categoryForm': categoryForm})


def admin_delete_category_view(request):
    categories = models.Category.objects.all()
    return render(request, 'polls/admin_delete_category.html', {'categories': categories})


def delete_category_view(request, pk):
    category = models.Category.objects.get(id=pk)
    category.delete()
    return redirect('admin-delete-category')

#### Course ####
def admin_course_view(request):
    return render(request,'polls/admin_course..html')

def admin_view_course_view(request):
    Course = models.Course.objects.all()
    return render(request,'polls/admin_view_course.html',{'Course':Course})

def admin_view_course_holder_view(request):
    CourseRecord = models.CourseRecord.objects.all()
    return render(request,'polls/admin_view_course_holder.html',{'CourseRecord':CourseRecord})

def admin_view_approved_course_holder_view(request):
    CourseRecord = models.CourseRecord.objects.all().filter(status='Approved')
    return render(request,'polls/admin_view_approved_course_holder.html',{'CourseRecord':CourseRecord})




def admin_add_course_view(request):
    CourseForm = forms.CourseForm()

    if request.method == 'POST':
        CourseForm = forms.CourseForm(request.POST)
        if CourseForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)

            course = CourseForm.save(commit=False)
            course.category = category
            course.save()
            return redirect('admin-view-course')
    return render(request, 'polls/admin_add_course.html', {'CourseForm': CourseForm})


def admin_delete_course_view(request):
    Course = models.Course.objects.all()
    return render(request, 'polls/admin_delete_course.html', {'Course': Course})


@login_required(login_url='adminlogin')
def delete_course_view(request, pk):
    Course = models.Course.objects.get(id=pk)
    Course.delete()
    return redirect('admin-delete-course')

def admin_update_course_view(request):
    Course = models.Course.objects.all()
    return render(request, 'polls/admin_update_course.html', {'Course': Course})


def update_course_view(request, pk):
    Course = models.Course.objects.get(id=pk)
    CourseForm = forms.CourseForm(instance=Course)
    if request.method == 'POST':
        CourseForm = forms.CourseForm(request.POST, instance=Course)
        if CourseForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)

            course = CourseForm.save(commit=False)
            course.category = category
            course.save()

            return redirect('admin-update-course')
    return render(request, 'polls/update_course.html', {'CourseForm': CourseForm})


##### QUESTIONS ########################################################################################################
def admin_question_view(request):
    questions = models.Question.objects.all()
    return render(request,'polls/admin_question.html',{'questions':questions})


def update_question_view(request, pk):
    question = models.Question.objects.get(id=pk)
    questionForm = forms.QuestionForm(instance=question)

    if request.method == 'POST':
        questionForm = forms.QuestionForm(request.POST, instance=question)

        if questionForm.is_valid():
            admin_comment = request.POST.get('admin_comment')

            question = questionForm.save(commit=False)
            question.admin_comment = admin_comment
            question.save()

            return redirect('admin-question')
    return render(request, 'polls/update_question.html', {'questionForm': questionForm})



##### Instructor ######################################################################################################s
def instructor_dashboard_view(request):
    dict={


    }
    return render(request,'polls/instructor/instructor_dashboard.html',context=dict)



### ADMIN _ INSTRUCTOR #############################################################################################
def admin_instructor_view(request):
    return render(request,'polls/admin_instructor.html')


def admin_add_instructor_view(request):
    InstructorForm = forms.InstructorForm()
    if request.method == 'POST':
        InstructorForm = forms.InstructorForm(request.POST)
        if InstructorForm.is_valid():
            name = request.POST['instructor_name']
            mail123= request.POST['emailid']
            id=request.POST['instructor_id']
           ########### Email #####################
            subject = "Welcome to hacker site!!"
            message = "Hello " + name + "!! \n" + "Welcome to Hacker site!! \nThank you for being part of our newtwork .\n Your Account has been successfully created !!! \n" + "Your Instrcutor id is :" +id+"\n You can login at http://127.0.0.1:8000/customerlogin. \n\nThanking You. \nTeam Hacker site."
            from_email = settings.EMAIL_HOST_USER
            to_list = [mail123]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            InstructorForm.save()
            return redirect('admin-view-instructor')
    return render(request, 'polls/admin_add_instructor.html', {'InstructorForm': InstructorForm})



def admin_view_instructor_view(request):
    Instructor = models.Instructor.objects.all()
    return render(request,'polls/admin_view_instructor.html',{'Instructor':Instructor})

def admin_update_instructor_view(request):
    instructor = models.Instructor.objects.all()
    return render(request, 'polls/admin_update_instructor.html', {'instructor': instructor})

def update_instructor_view(request,pk):
    instructor = models.Instructor.objects.get(id=pk)
    instructorForm = forms.InstructorForm(instance=instructor)
    if request.method == 'POST':
        instructorForm = forms.InstructorForm(request.POST, instance=instructor)
        if instructorForm.is_valid():
            instructorForm.save()
            return redirect('admin-instructor')
    return render(request, 'polls/update_instructor.html', {'instructorForm': instructorForm})

def admin_delete_instructor_view(request):
    instructor = models.Instructor.objects.all()
    return render(request, 'polls/admin_delete_instructor.html', {'instructor': instructor})


def delete_instructor_view(request, pk):
    Instructor = models.Instructor.objects.get(id=pk)
    Instructor.delete()
    return redirect('admin-instructor')

####################################################################################################
