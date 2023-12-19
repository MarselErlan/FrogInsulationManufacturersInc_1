from django import forms
from Warehouse1.models import WarehouseSupervisor, WarehouseWorker, Driver, WarehouseWorkerDriver




MALE = 1
FEMALE = 2
OTHER = 3
GENDER_TYPE = (
    (MALE, 'MALE'),
    (FEMALE, 'FEMALE'),
    (OTHER, 'OTHER')
)

class BaseEmployeeWarehouseForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=GENDER_TYPE, required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        fields = ['user', 'email', 'phone_number', 'age', 'gender', 'password1', 'password2']  # Общие поля для всех сотрудников

    def save(self, commit=True):
        user = super(BaseEmployeeWarehouseForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")
        return cleaned_data


class WarehouseSupervisorForm(BaseEmployeeWarehouseForm):
    class Meta(BaseEmployeeWarehouseForm.Meta):
        model = WarehouseSupervisor

class WarehouseWorkerForm(BaseEmployeeWarehouseForm):
    class Meta(BaseEmployeeWarehouseForm.Meta):
        model = WarehouseWorker


class DriverForm(BaseEmployeeWarehouseForm):
    class Meta(BaseEmployeeWarehouseForm.Meta):
        model = Driver


class WarehouseWorkerDriverForm(BaseEmployeeWarehouseForm):
    class Meta(BaseEmployeeWarehouseForm.Meta):
        model = WarehouseWorkerDriver

