from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"class": "w-full px-4 py-2 mb-4 border border-gray-300 rounded", "placeholder": "Your Name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "w-full px-4 py-2 mb-4 border border-gray-300 rounded", "placeholder": "Your Name"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "w-full px-4 py-2 mb-4 border border-gray-300 rounded", "placeholder": "Your Message"})
    )
