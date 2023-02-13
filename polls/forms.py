
from django import forms
from captcha.fields import ReCaptchaField

from . import models


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
    captcha = ReCaptchaField()


class CourseForm(forms.ModelForm):
    category=forms.ModelChoiceField(queryset=models.Category.objects.all(),empty_label="Category Name", to_field_name="id")
    class Meta:
        model=models.Course
        fields=['course_name','amount','validity']

class InstructorForm(forms.ModelForm):
    class Meta:
        model=models.Instructor
        fields=['instructor_name','instructor_id','mobile','emailid']

class CategoryForm(forms.ModelForm):
    class Meta:
        model=models.Category
        fields=['category_name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model=models.Question
        fields=['description']
        widgets = {
        'description': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=models.Profile
        fields=[ 'pincode', 'gender', 'aboutme', 'website','github','twitter', 'instagram', 'facebook']


