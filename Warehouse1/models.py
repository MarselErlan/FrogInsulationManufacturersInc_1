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


class WarehouseEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15, null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_TYPE, null=True)
    # Другие общие поля и методы для всех сотрудников

    class Meta:
        abstract = True

    def can_manage(self, other_employee):
        # Если текущий сотрудник начальник склада, он может управлять всеми
        if isinstance(self, WarehouseSupervisor):
            return True

        # Все остальные сотрудники не могут управлять другими
        return False


class WarehouseSupervisor(WarehouseEmployee):
    pass

class WarehouseWorker(WarehouseEmployee):
    pass

class Driver(WarehouseEmployee):
    truck_fully_loaded = models.BooleanField(default=False, null=True)


class WarehouseWorkerDriver(WarehouseEmployee):
    pass


