from django import forms
from django.utils.timezone import datetime, timedelta
from . models import Order

class DateInput(forms.DateInput):
    input_type = 'date'


class UserOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer', 'reserved_date',)
        widgets = {'reserved_date': DateInput()}


class UserOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer', 'reserved_date',)
        widgets = {'customer': forms.HiddenInput(), 'reserved_date': forms.HiddenInput(), }