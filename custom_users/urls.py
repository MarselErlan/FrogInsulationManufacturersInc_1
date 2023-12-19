from django.urls import path
from custom_users import views
from custom_users.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = 'custom_users'  # только если вы используете пространство имен

urlpatterns = [

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_add'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('register_clients/', views.register, name='register_clients'),





    path('dashboard_customer/', views.dashboard_customer, name='dashboard_customer'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('address/add/', views.add_address, name='add_address'),
    path('address/edit/<int:address_id>/', views.edit_address, name='edit_address'),

]






