from django import forms


class OrderModelForm(forms.Form):
    phone = forms.CharField(max_length=110)
    address = forms.CharField(max_length=110)
