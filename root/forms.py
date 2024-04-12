from django import forms
from django.forms import ModelForm
from .models import Unit


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class OrderForm(ModelForm):
    """To Select Orders in Drop down"""

    class Meta:
        model = Unit
        fields = ["unit_name"]
        labels = {"unit_name": "Select Unit"}
        # widgets = {"unit_name": forms.Select(attrs={"class": "form-control"})}
