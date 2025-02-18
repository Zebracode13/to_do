
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms

from django.forms.widgets import TextInput, Textarea, DateTimeInput
from .models import Task

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = (
            'username', 'email', 'password1', 'password1'
        )
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "deadline"]
        widgets = {
            "title": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Task Title",
            }),
            "description": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter Task Description",
                "rows": 2,
            }),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})

        }
