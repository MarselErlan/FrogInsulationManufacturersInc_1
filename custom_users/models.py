from django.db import models
from django.contrib.auth.models import User

MALE = 1
FEMALE = 2
OTHER = 3
GENDER_TYPE = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other')
)

class Client(User):
    customer_name = models.CharField(max_length=100, verbose_name='Customer Name', blank=True, null=True)
    customer_email = models.EmailField(verbose_name='Customer Email', blank=True, null=True)
    customer_phone = models.CharField(max_length=100, verbose_name='Customer Phone', blank=True, null=True)
    age = models.PositiveIntegerField(verbose_name='Age', blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_TYPE, verbose_name='Gender', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Avatar')
    registration_date = models.DateField(auto_now_add=True, verbose_name='Registration Date')

    def __str__(self):
        return self.username


from django.db import models

class DeliveryAddress(models.Model):
    company_name = models.CharField(max_length=100, verbose_name='Company Name', blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='delivery_addresses')
    address_line1 = models.CharField(max_length=100, verbose_name='Address Line 1')
    address_line2 = models.CharField(max_length=100, verbose_name='Address Line 2', blank=True)
    city = models.CharField(max_length=100, verbose_name='City')
    state = models.CharField(max_length=100, verbose_name='State')
    country = models.CharField(max_length=100, verbose_name='Country')
    postal_code = models.CharField(max_length=20, verbose_name='Postal Code')
    tax_exemption_document = models.FileField(upload_to='tax_exemption_documents/', blank=True, null=True, verbose_name='Tax Exemption Document')
    additional_info = models.TextField(verbose_name='Additional Information', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.postal_code}"

