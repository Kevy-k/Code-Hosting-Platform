from django import forms
from .models import repository

class FileUploadForm(forms.Form):
    class Meta:
        model=repository
        fields=['myFile']
        # widgets={
        #     'myFile':forms.ClearableFileInput(attrs={'multiple':True})
        # }
