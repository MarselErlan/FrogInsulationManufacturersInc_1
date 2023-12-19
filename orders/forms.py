from django import forms

from custom_users.models import Client, DeliveryAddress
from .models import OrderItem, Order
from MainWepSite.models import Product, ProductSize, Size


class OrderForm(forms.ModelForm):

    delivery_address = forms.ModelChoiceField(queryset=DeliveryAddress.objects.none(), required=False)
    tax_exemption_document = forms.FileField(required=False)

    class Meta:
        model = Order
        fields = [
            # другие поля...
            'delivery_address',  # Убедитесь, что это поле здесь присутствует
            'client',  # Добавьте это поле
            'customer_name', 'customer_email', 'customer_phone', 'company_name',
            'address_line1', 'address_line2', 'city', 'state', 'country',
            'postal_code', 'additional_info', 'tax_exemption_document'
        ]

        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'tax_exemption_document': forms.FileInput(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if user and hasattr(user, 'client'):
            self.fields['delivery_address'].queryset = user.client.delivery_addresses.all()


class OrderItemForm(forms.ModelForm):
    product_price = forms.DecimalField(label="Цена", disabled=True, required=False)

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price_at_time_of_purchase', 'order_sku']

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()

        if self.instance and self.instance.product:
            self.fields['price_at_time_of_purchase'].initial = self.instance.product.price

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



from django import forms

class OrderItemFormSize(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label='Количество',
        initial=1
    )

















