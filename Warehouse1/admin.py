from django.contrib import admin
from .models import WarehouseSupervisor, WarehouseWorker, Driver, WarehouseWorkerDriver
from django.contrib.auth.models import Group


admin.site.register(WarehouseSupervisor)
admin.site.register(WarehouseWorker)
admin.site.register(Driver)
admin.site.register(WarehouseWorkerDriver)



class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)  # отображаемые поля
    search_fields = ('name',)  # поля для поиска

admin.site.unregister(Group)  # Сначала отмените регистрацию стандартной модели
admin.site.register(Group, GroupAdmin)  # Затем зарегистрируйте вашу кастомную модель

