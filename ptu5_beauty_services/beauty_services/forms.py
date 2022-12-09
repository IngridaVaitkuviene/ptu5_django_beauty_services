from django import forms
from django.utils.timezone import datetime, timedelta
from datetime import date
from . models import Order, OrderLine, SalonReview

def tomorrow():
    return date.today() + timedelta(days=1)

class SalonReviewForm(forms.ModelForm):
    class Meta:
        model = SalonReview
        fields = ('content', 'beauty_salon', 'customer',)
        widgets = {
            'beauty_salon': forms.HiddenInput(),
            'customer': forms.HiddenInput(),
        }


class DateInput(forms.DateInput):
    input_type = 'date'


class UserOrderForm(forms.ModelForm):
    reserved_date = forms.DateField(required=True, widget=DateInput())
    class Meta:
        model = Order
        fields = ('customer', 'reserved_date',)
        widgets = {'customer': forms.HiddenInput()}


class UserOrderDetailAddForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ('order', 'salon_service', 'price',)
        widgets = {'order': forms.HiddenInput(), 'price': forms.HiddenInput()}

    def clean(self):
        cleaned_data = super().clean()
        salon_service = cleaned_data['salon_service']
        cleaned_data['price'] = salon_service.service.price
        return cleaned_data


class UserOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer', 'reserved_date',)
        widgets = {'customer': forms.HiddenInput(), 'reserved_date': forms.HiddenInput(), }