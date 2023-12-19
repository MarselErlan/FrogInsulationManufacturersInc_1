from django import forms
from orders.models import OrderItem


class UpdateOrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'price_at_time_of_purchase']

    quantity = forms.IntegerField(
        label="Quantity",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        required=True
    )
    price = forms.DecimalField(
        label="Price",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        required=True
    )



    def clean(self):
        cleaned_data = super().clean()
        # Если вам нужны дополнительные проверки или валидации, вы можете добавить их здесь.
        return cleaned_data

    def update(self, instance, commit=True, cleaned_data=None):
        # Здесь мы обновляем instance объекта.
        for field in self.Meta.fields:
            setattr(instance, field, cleaned_data.get(field))

        if commit:
            instance.save()

        return instance