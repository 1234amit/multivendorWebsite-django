from django import forms
from .models import Product, Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'zipcode', 'city',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'w-full px-4 py-2 border rounded-lg appearance-none'

        # Add additional classes or attributes as needed
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Your Address'
        self.fields['zipcode'].widget.attrs['placeholder'] = 'Enter Your Zipcode'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter yout City'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'title', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            })
        }