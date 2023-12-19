from django.contrib import admin
from .models import President, OperationalManager, AccountsReceivableManager, AccountsReceivable, \
    AccountsPayable
from django.contrib.auth.models import Group


admin.site.register(President)
admin.site.register(OperationalManager)
admin.site.register(AccountsReceivableManager)
admin.site.register(AccountsReceivable)
admin.site.register(AccountsPayable)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)  # отображаемые поля
    search_fields = ('name',)  # поля для поиска

admin.site.unregister(Group)  # Сначала отмените регистрацию стандартной модели
admin.site.register(Group, GroupAdmin)  # Затем зарегистрируйте вашу кастомную модель











AccountsPayable

