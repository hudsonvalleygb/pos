from django import forms

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from pos.models import Event


class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=DateTimePickerInput())
    end_date = forms.DateTimeField(widget=DateTimePickerInput())

    class Meta:
        model = Event
        fields = ['title', 'partner', 'host', 'start_date', 'end_date', 'address', 'city', 'state']

