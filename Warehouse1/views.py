from Warehouse1.models import WarehouseSupervisor, WarehouseWorker, Driver, WarehouseWorkerDriver
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from Warehouse1.forms import (
    WarehouseSupervisorForm, WarehouseWorkerForm, DriverForm,
    WarehouseWorkerDriverForm
)
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse



class BaseEmployeeWarehouseCreateView(CreateView):
    template_name = 'templates_for_warehouse/employee_warehouse_create_update_form.html'
    success_url = reverse_lazy('Warehouse1:all_employees_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

class WarehouseSupervisorCreateView(BaseEmployeeWarehouseCreateView):
    model = WarehouseSupervisor
    form_class = WarehouseSupervisorForm

class WarehouseWorkerCreateView(BaseEmployeeWarehouseCreateView):
    model = WarehouseWorker
    form_class = WarehouseWorkerForm

class DriverCreateView(BaseEmployeeWarehouseCreateView):
    model = Driver
    form_class = DriverForm

class WarehouseWorkerDriverCreateView(BaseEmployeeWarehouseCreateView):
    model = WarehouseWorkerDriver
    form_class = WarehouseWorkerDriverForm





class BaseEmployeeWarehouseListView(ListView):
    template_name = 'templates_for_warehouse/employee_warehouse_list.html'


class WarehouseSupervisorListView(BaseEmployeeWarehouseListView):
    model = WarehouseSupervisor

class WarehouseWorkerListView(BaseEmployeeWarehouseListView):
    model = WarehouseWorker

class DriverListView(BaseEmployeeWarehouseListView):
    model = Driver

class WarehouseWorkerDriverListView(BaseEmployeeWarehouseListView):
    model = WarehouseWorkerDriver






class BaseEmployeeWarehouseUpdateView(UpdateView):
    template_name = 'templates_for_warehouse/employee_warehouse_create_update_form.html'
    success_url = reverse_lazy('Warehouse1:all_employees_list')  # или любой другой соответствующий list-view

class WarehouseSupervisorUpdateView(BaseEmployeeWarehouseUpdateView):
    model = WarehouseSupervisor
    form_class = WarehouseSupervisorForm

class WarehouseWorkerUpdateView(BaseEmployeeWarehouseUpdateView):
    model = WarehouseWorker
    form_class = WarehouseWorkerForm

class DriverUpdateView(BaseEmployeeWarehouseUpdateView):
    model = Driver
    form_class = DriverForm

class WarehouseWorkerDriverUpdateView(BaseEmployeeWarehouseUpdateView):
    model = WarehouseWorkerDriver
    form_class = WarehouseWorkerDriverForm





class BaseEmployeeWarehouseDeleteView(DeleteView):
    template_name = 'templates_for_warehouse/employee_warehouse_confirm_delete.html'
    success_url = reverse_lazy('Warehouse1:all_employees_list')  # или любой другой соответствующий list-view

class WarehouseSupervisortDeleteView(BaseEmployeeWarehouseDeleteView):
    model = WarehouseSupervisor

class WarehouseWorkerDeleteView(BaseEmployeeWarehouseDeleteView):
    model = WarehouseWorker

class DriverDeleteView(BaseEmployeeWarehouseDeleteView):
    model = Driver

class WarehouseWorkerDriverDeleteView(BaseEmployeeWarehouseDeleteView):
    model = WarehouseWorkerDriver










class BaseWarehouseLoginView(LoginView):
    template_name = 'templates_for_warehouse/warehouse_login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name="warehouse_supervisor").exists():
            return reverse("Warehouse1:list_warehouse_supervisor")
        elif user.groups.filter(name="warehouse_worker").exists():
            return reverse("Warehouse1:list_warehouse_worker")
        elif user.groups.filter(name="driver").exists():
            return reverse("Warehouse1:list_driver")
        elif user.groups.filter(name="warehouse_worker_driver").exists():
            return reverse("Warehouse1:list_warehouse_worker_driver")
        else:
            return reverse("Warehouse1:all_employees_list")


class WarehouseSupervisorLoginView(BaseWarehouseLoginView):
    pass

class WarehouseWorkerLoginView(BaseWarehouseLoginView):
    pass

class DriverLoginView(BaseWarehouseLoginView):
    pass

class WarehouseWorkerDriverLoginView(BaseWarehouseLoginView):
    pass








from django.views.generic import TemplateView

class AllEmployeesWarehouseListView(TemplateView):
    template_name = "templates_for_warehouse/all_employees_warehouse_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouse_supervisors'] = WarehouseSupervisor.objects.all()
        context['warehouse_workers'] = WarehouseWorker.objects.all()
        context['drivers'] = Driver.objects.all()
        context['warehouse_worker_drivers'] = WarehouseWorkerDriver.objects.all()
        return context














from django.contrib.auth.models import Group

class EmployeeWarehouseRegistrationView(FormView):
    template_name = 'templates_for_warehouse/warehouse_register.html'
    success_url = reverse_lazy('Warehouse1:warehouse_login')  # Redirect to login.html page after registration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserCreationForm(request.POST)
        role = request.POST.get('role')

        if user_form.is_valid():
            user = user_form.save()

            # Add user to a group based on their role
            group = Group.objects.get(name=role)
            user.groups.add(group)

            # Create corresponding employee entry
            if role == "warehouse_supervisor":
                warehouse_supervisor = WarehouseSupervisor(user=user)
                warehouse_supervisor.save()
            elif role == "warehouse_worker":
                warehouse_worker = WarehouseWorker(user=user)
                warehouse_worker.save()
            elif role == "driver":
                driver = Driver(user=user)
                driver.save()
            elif role == "warehouse_worker_driver":
                warehouse_worker_driver = WarehouseWorkerDriver(user=user)
                warehouse_worker_driver.save()

            return self.form_valid(user_form)
        else:
            return self.form_invalid(user_form)

    def get_form_class(self):
        role = self.request.POST.get('role', None)
        if role == "warehouse_supervisor":
            return WarehouseSupervisorForm
        elif role == "warehouse_worker":
            return WarehouseWorkerForm
        elif role == "driver":
            return DriverForm
        elif role == "warehouse_worker_driver":
            return WarehouseWorkerDriverForm
        else:
            return UserCreationForm

