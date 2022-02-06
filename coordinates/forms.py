from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file')


class AdressAndRadiusForm(forms.Form):
    address = forms.CharField(max_length=255)
    radius = forms.IntegerField(min_value=0)
