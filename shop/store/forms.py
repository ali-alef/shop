from django import forms

from .models import Product


class ProductModelForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    price = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'image',
        ]
