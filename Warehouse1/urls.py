from django.urls import path
from .views import (
    WarehouseSupervisorCreateView, WarehouseSupervisorListView, WarehouseSupervisorUpdateView,
    WarehouseSupervisortDeleteView, WarehouseWorkerCreateView, WarehouseWorkerListView, WarehouseWorkerUpdateView,
    WarehouseWorkerDeleteView, DriverCreateView, DriverListView, DriverUpdateView, DriverDeleteView,
    WarehouseWorkerDriverCreateView, WarehouseWorkerDriverListView, WarehouseWorkerDriverUpdateView,
    WarehouseWorkerDriverDeleteView, WarehouseSupervisorLoginView, WarehouseWorkerLoginView, DriverLoginView,
    WarehouseWorkerDriverLoginView, AllEmployeesWarehouseListView, EmployeeWarehouseRegistrationView,
    BaseWarehouseLoginView
)

app_name = 'Warehouse1'

urlpatterns = [
    # CRUD views for WarehouseSupervisor
    path('create/warehouse_supervisor/', WarehouseSupervisorCreateView.as_view(), name='create_warehouse_supervisor'),
    path('list/warehouse_supervisor/', WarehouseSupervisorListView.as_view(), name='list_warehouse_supervisor'),
    path('update/warehouse_supervisor/<int:pk>/', WarehouseSupervisorUpdateView.as_view(), name='update_warehouse_supervisor'),
    path('delete/warehouse_supervisor/<int:pk>/', WarehouseSupervisortDeleteView.as_view(), name='delete_warehouse_supervisor'),

    # CRUD views for WarehouseWorker
    path('create/warehouse_worker/', WarehouseWorkerCreateView.as_view(), name='create_warehouse_worker'),
    path('list/warehouse_worker/', WarehouseWorkerListView.as_view(), name='list_warehouse_worker'),
    path('update/warehouse_worker/<int:pk>/', WarehouseWorkerUpdateView.as_view(), name='update_warehouse_worker'),
    path('delete/warehouse_worker/<int:pk>/', WarehouseWorkerDeleteView.as_view(), name='delete_warehouse_worker'),

    # CRUD views for Driver
    path('create/driver/', DriverCreateView.as_view(), name='create_driver'),
    path('list/driver/', DriverListView.as_view(), name='list_driver'),
    path('update/driver/<int:pk>/', DriverUpdateView.as_view(), name='update_driver'),
    path('delete/driver/<int:pk>/', DriverDeleteView.as_view(), name='delete_driver'),

    # CRUD views for WarehouseWorkerDriver
    path('create/warehouse_worker_driver/', WarehouseWorkerDriverCreateView.as_view(), name='create_warehouse_worker_driver'),
    path('list/warehouse_worker_driver/', WarehouseWorkerDriverListView.as_view(), name='list_warehouse_worker_driver'),
    path('update/warehouse_worker_driver/<int:pk>/', WarehouseWorkerDriverUpdateView.as_view(), name='update_warehouse_worker_driver'),
    path('delete/warehouse_worker_driver/<int:pk>/', WarehouseWorkerDriverDeleteView.as_view(), name='delete_warehouse_worker_driver'),

    # Login views
    path('login/warehouse_supervisor/', WarehouseSupervisorLoginView.as_view(), name='login_warehouse_supervisor'),
    path('login/warehouse_worker/', WarehouseWorkerLoginView.as_view(), name='login_warehouse_worker'),
    path('login/driver/', DriverLoginView.as_view(), name='login_driver'),
    path('login/warehouse_worker_driver/', WarehouseWorkerDriverLoginView.as_view(), name='login_warehouse_worker_driver'),

    # Other views
    path('all_employees_list/', AllEmployeesWarehouseListView.as_view(), name='all_employees_warehouse_list'),
    path('warehouse_register/', EmployeeWarehouseRegistrationView.as_view(), name='warehouse_register'),
    path('warehouse_login/', BaseWarehouseLoginView.as_view(), name='warehouse_login'),

]
