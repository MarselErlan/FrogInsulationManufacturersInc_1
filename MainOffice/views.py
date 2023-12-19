from .models import President, OperationalManager, AccountsReceivableManager, AccountsReceivable,\
    AccountsPayable
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import (
    PresidentForm, OperationalManagerForm, AccountsReceivableManagerForm,
    AccountsReceivableForm, AccountsPayableForm, BaseEmployeeForm
)
from django.contrib.auth.forms import UserCreationForm


class BaseEmployeeCreateView(CreateView):
    template_name = 'templates_for_office/employee_create_update_form.html'
    success_url = reverse_lazy('MainOffice:all_employees_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

class PresidentCreateView(BaseEmployeeCreateView):
    model = President
    form_class = PresidentForm

class OperationalManagerCreateView(BaseEmployeeCreateView):
    model = OperationalManager
    form_class = OperationalManagerForm

class AccountsReceivableManagerCreateView(BaseEmployeeCreateView):
    model = AccountsReceivableManager
    form_class = AccountsReceivableManagerForm

class AccountsReceivableCreateView(BaseEmployeeCreateView):
    model = AccountsReceivable
    form_class = AccountsReceivableForm

class AccountsPayableCreateView(BaseEmployeeCreateView):
    model = AccountsPayable
    form_class = AccountsPayableForm





class BaseEmployeeListView(ListView):
    template_name = 'templates_for_office/employee_list.html'


class PresidentListView(BaseEmployeeListView):
    model = President

class OperationalManagerListView(BaseEmployeeListView):
    model = OperationalManager

class AccountsReceivableManagerListView(BaseEmployeeListView):
    model = AccountsReceivableManager

class AccountsReceivableListView(BaseEmployeeListView):
    model = AccountsReceivable

class AccountsPayableListView(BaseEmployeeListView):
    model = AccountsPayable


class BaseEmployeeUpdateView(UpdateView):
    template_name = 'templates_for_office/employee_create_update_form.html'
    success_url = reverse_lazy('MainOffice:all_employees_list')  # или любой другой соответствующий list-view

class PresidentUpdateView(BaseEmployeeUpdateView):
    model = President
    form_class = PresidentForm

class OperationalManagerUpdateView(BaseEmployeeUpdateView):
    model = OperationalManager
    form_class = OperationalManagerForm

class AccountsReceivableManagerUpdateView(BaseEmployeeUpdateView):
    model = AccountsReceivableManager
    form_class = AccountsReceivableManagerForm

class AccountsReceivableUpdateView(BaseEmployeeUpdateView):
    model = AccountsReceivable
    form_class = AccountsReceivableForm

class AccountsPayableUpdateView(BaseEmployeeUpdateView):
    model = AccountsPayable
    form_class = AccountsPayableForm




class BaseEmployeeDeleteView(DeleteView):
    template_name = 'templates_for_office/employee_confirm_delete.html'
    success_url = reverse_lazy('MainOffice:all_employees_list')  # или любой другой соответствующий list-view

class PresidentDeleteView(BaseEmployeeDeleteView):
    model = President

class OperationalManagerDeleteView(BaseEmployeeDeleteView):
    model = OperationalManager

class AccountsReceivableManagerDeleteView(BaseEmployeeDeleteView):
    model = AccountsReceivableManager

class AccountsReceivableDeleteView(BaseEmployeeDeleteView):
    model = AccountsReceivable

class AccountsPayableDeleteView(BaseEmployeeDeleteView):
    model = AccountsPayable





from django.urls import reverse

class BaseLoginView(LoginView):
    template_name = 'templates_for_office/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name="president").exists():
            return reverse("MainOffice:list_president")
        elif user.groups.filter(name="operational_manager").exists():
            return reverse("MainOffice:list_operational_manager")
        elif user.groups.filter(name="accounts_receivable_manager").exists():
            return reverse("MainOffice:list_accounts_receivable_manager")
        elif user.groups.filter(name="accounts_receivable").exists():
            return reverse("MainOffice:list_accounts_receivable")
        elif user.groups.filter(name="accounts_payable").exists():
            return reverse("MainOffice:list_accounts_payable")

        else:
            return reverse("MainOffice:all_employees_list")


class PresidentLoginView(BaseLoginView):
    pass

class OperationalManagerLoginView(BaseLoginView):
    pass

class AccountsReceivableManagerLoginView(BaseLoginView):
    pass

class AccountsReceivableLoginView(BaseLoginView):
    pass

class AccountsPayableLoginView(BaseLoginView):
    pass



from django.views.generic import TemplateView

class AllEmployeesListView(TemplateView):
    template_name = "templates_for_office/all_employees_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['presidents'] = President.objects.all()
        context['operational_managers'] = OperationalManager.objects.all()
        context['accounts_receivable_managers'] = AccountsReceivableManager.objects.all()
        context['accounts_receivables'] = AccountsReceivable.objects.all()
        context['accounts_payables'] = AccountsPayable.objects.all()
        return context


from django.contrib.auth.models import Group




from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

class EmployeeRegistrationView(FormView):
    template_name = 'templates_for_office/register.html'
    success_url = reverse_lazy('MainOffice:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        context["user_form"] = form_class()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            user = form.save()

            # Add user to a group based on their role
            role = request.POST.get('role')
            group = Group.objects.get(name=role)
            user.groups.add(group)

            # Depending on the role, create the employee
            if role == "president":
                President.objects.create(user=user)
            elif role == "operational_manager":
                OperationalManager.objects.create(user=user)
            elif role == "accounts_receivable_manager":
                AccountsReceivableManager.objects.create(user=user)
            elif role == "accounts_receivable":
                AccountsReceivable.objects.create(user=user)
            elif role == "accounts_payable":
                AccountsPayable.objects.create(user=user)
            # ... (do the same for other roles)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_class(self):
        role = self.request.POST.get('role', None)
        if role == "president":
            return PresidentForm
        elif role == "operational_manager":
            return OperationalManagerForm
        elif role == "accounts_receivable_manager":
            return AccountsReceivableManagerForm
        elif role == "accounts_receivable":
            return AccountsReceivableForm
        elif role == "accounts_payable":
            return AccountsPayableForm
        # ... (do the same for other roles)
        else:
            return PresidentForm








#
# class EmployeeRegistrationView(FormView):
#     template_name = 'templates_for_office/register.html'
#     success_url = reverse_lazy('MainOffice:login')  # Redirect to login.html page after registration
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["user_form"] = UserCreationForm()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         user_form = UserCreationForm(request.POST)
#         role = request.POST.get('role')
#
#         if user_form.is_valid():
#             user = user_form.save()
#
#             # Add user to a group based on their role
#             group = Group.objects.get(name=role)
#             user.groups.add(group)
#
#             # Create corresponding employee entry
#             if role == "president":
#                 president = President(user=user)
#                 president.save()
#             elif role == "operational_manager":
#                 operational_manager = OperationalManager(user=user)
#                 operational_manager.save()
#             elif role == "accounts_receivable_manager":
#                 accounts_receivable_manager = AccountsReceivableManager(user=user)
#                 accounts_receivable_manager.save()
#             elif role == "accounts_receivable":
#                 accounts_receivable = AccountsReceivable(user=user)
#                 accounts_receivable.save()
#             elif role == "accounts_payable":
#                 accounts_payable = AccountsPayable(user=user)
#                 accounts_payable.save()
#
#             return self.form_valid(user_form)
#         else:
#             return self.form_invalid(user_form)
#
#     def get_form_class(self):
#         role = self.request.POST.get('role', None)  # Используйте None вместо 'president'
#         if role == "president":
#             return PresidentForm
#         elif role == "operational_manager":
#             return OperationalManagerForm
#         elif role == "accounts_receivable_manager":
#             return AccountsReceivableManagerForm
#         elif role == "accounts_receivable":
#             return AccountsReceivableForm
#         elif role == "accounts_payable":
#             return AccountsPayableForm
#         else:
#             return UserCreationForm



