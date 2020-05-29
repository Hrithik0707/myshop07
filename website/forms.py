from django import forms 
from .models import Product

class UploadProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','img','des','price','slug']
