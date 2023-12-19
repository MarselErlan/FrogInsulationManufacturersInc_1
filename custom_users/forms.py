from django import forms
from .models import Client, DeliveryAddress
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['username', 'email', 'customer_phone', 'customer_name', 'avatar', 'age', 'gender', 'password1', 'password2']



from django import forms

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = [
            'address_line1', 'address_line2', 'city',
            'state', 'country', 'postal_code', 'additional_info',
            'company_name', 'tax_exemption_document'
        ]
        widgets = {


            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean_customer_email(self):
        email = self.cleaned_data.get('customer_email')
        if email and Client.objects.filter(customer_email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A client with this email already exists.')
        return email

    def save(self, commit=True):
        client = super().save(commit=False)
        # You can add custom save logic here
        if commit:
            client.save()
        return client
