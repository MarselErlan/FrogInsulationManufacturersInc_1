from django.contrib.auth.models import User
from django.db import models

MALE = 1
FEMALE = 2
OTHER = 3
GENDER_TYPE = (
    (MALE, 'MALE'),
    (FEMALE, 'FEMALE'),
    (OTHER, 'OTHER')
)

class MainOfficeEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_TYPE, null=True)

    class Meta:
        abstract = True

    def can_manage(self, other_employee):
        # Если текущий сотрудник президент, он может управлять всеми
        if isinstance(self, President):
            return True

        # Если текущий сотрудник операционный менеджер, он может управлять всеми, кроме президента
        elif isinstance(self, OperationalManager) and not isinstance(other_employee, President):
            return True

        # Операционный менеджер может управлять менеджерами по сбору средств
        elif isinstance(self, OperationalManager) and isinstance(other_employee, AccountsReceivableManager):
            return True

        # Менеджер по сбору средств может управлять сотрудниками по сбору средств и сотрудниками по оплате счетов
        elif isinstance(self, AccountsReceivableManager) and (
                isinstance(other_employee, AccountsReceivable) or isinstance(other_employee, AccountsPayable)):
            return True

        # Для всех других ситуаций возвращаем False
        return False


class President(MainOfficeEmployee):
    # Дополнительные поля и методы для президента
    pass


class OperationalManager(MainOfficeEmployee):
    # Дополнительные поля и методы для операционного менеджера
    pass


class AccountsReceivableManager(MainOfficeEmployee):
    # Дополнительные поля и методы для менеджера по сбору средств
    pass


class AccountsReceivable(MainOfficeEmployee):
    # Дополнительные поля и методы для сотрудника по сбору средств
    pass


class AccountsPayable(MainOfficeEmployee):
    # Дополнительные поля и методы для сотрудника по оплате счетов
    pass

