from django.urls import path
from .views import (
    PresidentCreateView, OperationalManagerCreateView, AccountsReceivableManagerCreateView,
    AccountsReceivableCreateView, AccountsPayableCreateView,
    PresidentListView, OperationalManagerListView, AccountsReceivableManagerListView,
    AccountsReceivableListView, AccountsPayableListView,
    PresidentUpdateView, OperationalManagerUpdateView, AccountsReceivableManagerUpdateView,
    AccountsReceivableUpdateView, AccountsPayableUpdateView,
    PresidentDeleteView, OperationalManagerDeleteView, AccountsReceivableManagerDeleteView,
    AccountsReceivableDeleteView, AccountsPayableDeleteView,
    PresidentLoginView, OperationalManagerLoginView, AccountsReceivableManagerLoginView,
    AccountsReceivableLoginView, AccountsPayableLoginView,
    AllEmployeesListView, EmployeeRegistrationView, BaseLoginView,

)

app_name = 'MainOffice'

urlpatterns = [
    # CRUD views for President
    path('create/president/', PresidentCreateView.as_view(), name='create_president'),
    path('list/president/', PresidentListView.as_view(), name='list_president'),
    path('update/president/<int:pk>/', PresidentUpdateView.as_view(), name='update_president'),
    path('delete/president/<int:pk>/', PresidentDeleteView.as_view(), name='delete_president'),

    # CRUD views for OperationalManager
    path('create/operational_manager/', OperationalManagerCreateView.as_view(), name='create_operational_manager'),
    path('list/operational_manager/', OperationalManagerListView.as_view(), name='list_operational_manager'),
    path('update/operational_manager/<int:pk>/', OperationalManagerUpdateView.as_view(),
         name='update_operational_manager'),
    path('delete/operational_manager/<int:pk>/', OperationalManagerDeleteView.as_view(),
         name='delete_operational_manager'),

    # CRUD views for AccountsReceivableManager
    path('create/accounts_receivable_manager/', AccountsReceivableManagerCreateView.as_view(),
         name='create_accounts_receivable_manager'),
    path('list/accounts_receivable_manager/', AccountsReceivableManagerListView.as_view(),
         name='list_accounts_receivable_manager'),
    path('update/accounts_receivable_manager/<int:pk>/', AccountsReceivableManagerUpdateView.as_view(),
         name='update_accounts_receivable_manager'),
    path('delete/accounts_receivable_manager/<int:pk>/', AccountsReceivableManagerDeleteView.as_view(),
         name='delete_accounts_receivable_manager'),

    # CRUD views for AccountsReceivable
    path('create/accounts_receivable/', AccountsReceivableCreateView.as_view(), name='create_accounts_receivable'),
    path('list/accounts_receivable/', AccountsReceivableListView.as_view(), name='list_accounts_receivable'),
    path('update/accounts_receivable/<int:pk>/', AccountsReceivableUpdateView.as_view(),
         name='update_accounts_receivable'),
    path('delete/accounts_receivable/<int:pk>/', AccountsReceivableDeleteView.as_view(),
         name='delete_accounts_receivable'),

    # CRUD views for AccountsPayable
    path('create/accounts_payable/', AccountsPayableCreateView.as_view(), name='create_accounts_payable'),
    path('list/accounts_payable/', AccountsPayableListView.as_view(), name='list_accounts_payable'),
    path('update/accounts_payable/<int:pk>/', AccountsPayableUpdateView.as_view(), name='update_accounts_payable'),
    path('delete/accounts_payable/<int:pk>/', AccountsPayableDeleteView.as_view(), name='delete_accounts_payable'),

    # Login views
    path('login/president/', PresidentLoginView.as_view(), name='login_president'),
    path('login/operational_manager/', OperationalManagerLoginView.as_view(), name='login_operational_manager'),
    path('login/accounts_receivable_manager/', AccountsReceivableManagerLoginView.as_view(),
         name='login_accounts_receivable_manager'),
    path('login/accounts_receivable/', AccountsReceivableLoginView.as_view(), name='login_accounts_receivable'),
    path('login/accounts_payable/', AccountsPayableLoginView.as_view(), name='login_accounts_payable'),

    # Other views
    path('contact/', AllEmployeesListView.as_view(), name='all_employees_list'),
    path('register/', EmployeeRegistrationView.as_view(), name='register_employee'),
    path('login/', BaseLoginView.as_view(), name='login_employee'),

]

