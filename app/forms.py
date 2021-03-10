from django import forms

from .models import *


class EmployeeCreate(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['fio', 'position',]