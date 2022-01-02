from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from CRM.models import ClassList, Member, Student_list


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")

class NoviceForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ("name","email")