from django import forms
from MainOffice.models import President, OperationalManager, AccountsReceivableManager, AccountsReceivable, AccountsPayable
from django.contrib.auth.models import User

MALE = 1
FEMALE = 2
OTHER = 3
GENDER_TYPE = (
    (MALE, 'MALE'),
    (FEMALE, 'FEMALE'),
    (OTHER, 'OTHER')
)

class BaseEmployeeForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=150,
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'info@example.com'})
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'})
    )
    age = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'Возраст'})
    )
    gender = forms.ChoiceField(choices=GENDER_TYPE, required=True)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'})
    )

    class Meta:
        fields = ['username', 'email', 'phone_number', 'age', 'gender', 'password1', 'password2']

    def save(self, commit=True):
        user = User(username=self.cleaned_data['username'], email=self.cleaned_data['email'])
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

class PresidentForm(BaseEmployeeForm):
    class Meta(BaseEmployeeForm.Meta):
        model = President

class OperationalManagerForm(BaseEmployeeForm):
    class Meta(BaseEmployeeForm.Meta):
        model = OperationalManager

class AccountsReceivableManagerForm(BaseEmployeeForm):
    class Meta(BaseEmployeeForm.Meta):
        model = AccountsReceivableManager

class AccountsReceivableForm(BaseEmployeeForm):
    class Meta(BaseEmployeeForm.Meta):
        model = AccountsReceivable

class AccountsPayableForm(BaseEmployeeForm):
    class Meta(BaseEmployeeForm.Meta):
        model = AccountsPayable
