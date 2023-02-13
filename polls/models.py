from django.db import models
from django.contrib.auth.models import User
from hackersite.models import Customer



class Question(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    description =models.CharField(max_length=500)
    admin_comment=models.CharField(max_length=200,default='Nothing')
    asked_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.description

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)



class Category(models.Model):
    category_name =models.CharField(max_length=20)
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.category_name


class Course(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    course_name=models.CharField(max_length=200)
    amount=models.PositiveIntegerField()
    validity=models.PositiveIntegerField()
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.course_name

class CourseRecord(models.Model):
    Customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    Course= models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,default='Pending')
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return str(self.course)

class Instructor(models.Model):
    instructor_name = models.CharField(max_length=200,null=False)
    instructor_id = models.CharField(max_length=250,null=False)
    mobile = models.IntegerField(null=True)
    emailid = models.EmailField(null=True)
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.instructor_name


class InstructorRecord(models.Model):
    Customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    instructor_name= models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,default='Pending')
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.Instructor

class Profile(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pincode = models.IntegerField(null=True)
    gender = models.CharField(max_length=500,null=True)
    aboutme = models.CharField(max_length=500,null=True)
    website = models.CharField(max_length=500,null=True)
    github = models.CharField(max_length=500,null=True)
    twitter = models.CharField(max_length=500,null=True)
    instagram = models.CharField(max_length=500,null=True)
    facebook = models.CharField(max_length=500,null=True)
    def __str__(self):
        return self.gender