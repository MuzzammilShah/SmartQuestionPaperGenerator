from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, HiddenInput
from django.contrib.auth.models import User, Group
from django import forms
from .models import *

class UserProfileForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label='Select Department', required=True)
    email = forms.EmailField(required=True)
    otp = forms.CharField(required=True)
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2', 'group', 'otp']

class UpdateUserForm(UserChangeForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label='Select Department', required=True)
    email = forms.EmailField(required=True)
    email_disabled = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = HiddenInput()
        self.fields['email_disabled'].disabled = True

    class Meta:
        model=User
        fields=['username', 'email', 'group']

class CreateGroupForm(ModelForm):
    class Meta:
        model=Group
        fields=['name']

class CreateCourseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dept'].empty_label = 'Select Department'

    class Meta:
        model=Course
        fields='__all__'

class CreateModuleForm(ModelForm):
    course_disabled = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label='Select Course', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].empty_label = 'Select Course'
        self.fields['course'].widget = HiddenInput()
        self.fields['course_disabled'].disabled = True

    class Meta:
        model=Module
        fields='__all__'

class CreateQuestionForm(ModelForm):
    module_disabled = forms.ModelChoiceField(queryset=Module.objects.all(), empty_label='Select Module', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['module'].empty_label = 'Select Module'
        self.fields['module'].widget = HiddenInput()
        self.fields['module_disabled'].disabled = True

    class Meta:
        model=Question
        # fields=['question', 'marks', 'difficulty', 'rbt_level', 'module', 'module_disabled']
        fields = '__all__'

class CreateMcqForm(ModelForm):
    module_disabled = forms.ModelChoiceField(queryset=Module.objects.all(), empty_label='Select Module', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['module'].empty_label = 'Select Module'
        self.fields['module'].widget = HiddenInput()
        self.fields['module_disabled'].disabled = True

    class Meta:
        model=Mcq
        fields='__all__'

class GeneratePaperForm(ModelForm):
    
    group = forms.ModelChoiceField(queryset=Group.objects.exclude(name="Admin"), empty_label='Select Department', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].empty_label = 'Select Course'

    class Meta:
        model=Paper
        fields=['group', 'sem', 'course', 'difficulty', 'term', 'exam_date']