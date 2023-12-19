from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client, DeliveryAddress
from .forms import ClientRegistrationForm, DeliveryAddressForm
from .models import Client
from .forms import DeliveryAddress
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import ClientRegistrationForm
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import DeliveryAddressForm



class ClientListView(ListView):
    model = Client
    template_name = 'templates_for_client/client_list.html'
    context_object_name = 'clients'

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientRegistrationForm
    template_name = 'templates_for_client/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientRegistrationForm
    template_name = 'templates_for_client/client_form.html'
    success_url = reverse_lazy('client_list')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'templates_for_client/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')




class DeliveryAddressCreateView(CreateView):
    model = DeliveryAddress
    form_class = DeliveryAddressForm
    # Остальные настройки

class DeliveryAddressUpdateView(UpdateView):
    model = DeliveryAddress
    form_class = DeliveryAddressForm
    # Остальные настройки

class DeliveryAddressDeleteView(DeleteView):
    model = DeliveryAddress
    # Остальные настройки



@login_required
def dashboard_customer(request):
    client = request.user.client
    addresses = client.delivery_addresses.all()
    return render(request, 'templates_for_client/dashboard_customer.html', {'client': client, 'addresses': addresses})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST, instance=request.user.client)
        if form.is_valid():
            form.save()
            # Redirect to dashboard with success message
    else:
        form = ClientRegistrationForm(instance=request.user.client)
    return render(request, 'templates_for_client/update_profile.html', {'form': form})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.client = request.user.client
            address.save()
            # Redirect to dashboard with success message
    else:
        form = DeliveryAddressForm()
    return render(request, 'templates_for_client/add_address.html', {'form': form})

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(DeliveryAddress, id=address_id, client=request.user.client)
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            # Redirect to dashboard with success message
    else:
        form = DeliveryAddressForm(instance=address)
    return render(request, 'templates_for_client/edit_address.html', {'form': form, 'address': address})





def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('MainOffice:login_employee')  # Или куда вы хотите перенаправить пользователя после регистрации
    else:
        form = ClientRegistrationForm()
    return render(request, 'templates_for_client/register_clients.html', {'form': form})

