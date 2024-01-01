from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MainWepSite.urls', namespace='MainWepSite')),
    path('', include('orders.urls', namespace='orders')),
    path('', include('MainOffice.urls', namespace='MainOffice')),
    path('', include('Warehouse1.urls', namespace='Warehouse1')),
    path("select2/", include("django_select2.urls")),
    path('', include('custom_users.urls', namespace='custom_users')),
    # path('', include('PaymentsApp.urls')),
    path('', include('paypal.standard.ipn.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
 + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
