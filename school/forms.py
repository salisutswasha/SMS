from django import forms
from django.contrib.auth.models import User
from .models import StudentExtra
from .models import TeacherExtra
from . import models

#for admin
class AdminSigupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['first_name', 'last_name', 'username', 'email', 'password']
        for name in required_fields:
            if name in self.fields:
                self.fields[name].required = True
                self.fields[name].widget.attrs['required'] = 'required'
        # confirm_password is a plain form field
        self.fields['confirm_password'].required = True
        self.fields['confirm_password'].widget.attrs['required'] = 'required'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data


#for student related form
class StudentUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['first_name', 'last_name', 'username', 'email', 'password']
        for name in required_fields:
            if name in self.fields:
                self.fields[name].required = True
                self.fields[name].widget.attrs['required'] = 'required'
        self.fields['confirm_password'].required = True
        self.fields['confirm_password'].widget.attrs['required'] = 'required'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email is required.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = StudentExtra
        fields = ['mobile', 'middle_name', 'date_of_birth', 'state_of_origin','address', 'gender']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'text', 'placeholder': 'Date of Birth', 'onfocus': "this.type='date'", 'onblur': "if(!this.value)this.type='text'"}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile and (len(mobile) < 10 or len(mobile) > 20):
            raise forms.ValidationError('Enter a valid phone number.')
        return mobile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all displayed fields required
        required_fields = ['mobile', 'middle_name', 'date_of_birth', 'state_of_origin', 'address', 'gender']
        for name in required_fields:
            if name in self.fields:
                self.fields[name].required = True
                # address uses Textarea by default, still supports required attr
                self.fields[name].widget.attrs['required'] = 'required'
        # Set Gender empty label
        if 'gender' in self.fields:
            choices = list(self.fields['gender'].choices)
            if choices and choices[0][0] == '':
                choices[0] = ('', 'Gender')
            else:
                choices = [('', 'Gender')] + choices
            self.fields['gender'].choices = choices


#for teacher related form
class TeacherUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Email Address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['first_name', 'last_name', 'username', 'email', 'password']
        for name in required_fields:
            if name in self.fields:
                self.fields[name].required = True
                self.fields[name].widget.attrs['required'] = 'required'
        self.fields['confirm_password'].required = True
        self.fields['confirm_password'].widget.attrs['required'] = 'required'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

class TeacherExtraForm(forms.ModelForm):
    class Meta:
        model = models.TeacherExtra
        fields = ['date_of_birth', 'mobile', 'course_of_study', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'text', 'placeholder': 'Date of Birth', 'onfocus': "this.type='date'", 'onblur': "if(!this.value)this.type='text'"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['date_of_birth', 'mobile', 'course_of_study', 'address']
        for name in required_fields:
            if name in self.fields:
                self.fields[name].required = True
                self.fields[name].widget.attrs['required'] = 'required'





#for Attendance related form
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()




#for notice related form
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'



#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
