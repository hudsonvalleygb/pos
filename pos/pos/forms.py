from django import forms
from django.contrib.auth.models import User

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from pos.models import Event, UserInfo


class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=DateTimePickerInput())
    end_date = forms.DateTimeField(widget=DateTimePickerInput())

    class Meta:
        model = Event
        fields = ['title', 'partner', 'host', 'start_date', 'end_date', 'address', 'city', 'state']


class NewUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'max_length': '50'}), required=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
