from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from Warehouse1.models import WarehouseSupervisor, WarehouseWorker, Driver, WarehouseWorkerDriver
from MainOffice.models import President, OperationalManager, AccountsReceivableManager, AccountsReceivable, \
    AccountsPayable, MainOfficeEmployee
from custom_users.models import Client, DeliveryAddress


class OrderStatus(models.TextChoices):
    RECEIVED = 'Received', 'Received'
    OPERATOR_REVIEW = 'OperatorReview', 'Operator Review'
    WAREHOUSE_PROCESSING = 'WarehouseProcessing', 'Warehouse Processing'
    TRUCK_LOADING = 'TruckLoading', 'Truck Loading'
    DELIVERY = 'Delivery', 'Delivery'
    COMPLETED = 'Completed', 'Completed'
    CANCELED = 'Canceled', 'Canceled'

class Order(models.Model):
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.RECEIVED)
    president = models.ForeignKey(President, null=True, blank=True, on_delete=models.SET_NULL)
    operational_manager = models.ForeignKey(OperationalManager, null=True, blank=True, on_delete=models.SET_NULL)
    accounts_receivable_manager = models.ForeignKey(AccountsReceivableManager, null=True, blank=True, on_delete=models.SET_NULL)
    accounts_receivable = models.ForeignKey(AccountsReceivable, null=True, blank=True, on_delete=models.SET_NULL)
    accounts_payable = models.ForeignKey(AccountsPayable, null=True, blank=True, on_delete=models.SET_NULL)
    warehouse_supervisor = models.ForeignKey(WarehouseSupervisor, null=True, blank=True, on_delete=models.SET_NULL)
    warehouse_worker = models.ForeignKey(WarehouseWorker, null=True, blank=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.SET_NULL)
    warehouse_Worker_Driver = models.ForeignKey(WarehouseWorkerDriver, null=True, blank=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=100, verbose_name='Company Name', blank=True)

    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    tax_exemption_document = models.FileField(upload_to='tax_exemption_documents/', blank=True, null=True)

    postal_code = models.CharField(max_length=15, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    is_loaded = models.BooleanField(default=False, null=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    truck_fully_loaded = models.BooleanField(default=False, null=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_paid = models.BooleanField(default=False, null=True)
    payment_method = models.CharField(max_length=100, default='offline', null=True)
    transaction_id = models.UUIDField(null=True)

    def send_for_loading(self):
        self.sent_for_loading_at = timezone.now()
        self.save()

    def mark_as_loaded(self):
        self.is_loaded = True
        self.loaded_at = timezone.now()
        self.save()

    def mark_truck_as_fully_loaded(self):
        self.truck_fully_loaded = True
        self.save()
        for order in Order.objects.filter(driver=self, status=OrderStatus.TRUCK_LOADING):
            order.change_status(OrderStatus.DELIVERY)

    def get_total_amount(self):
        return sum(item.get_total_price() for item in self.items.all())


    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    def cancel_order(self):
        self.change_status(OrderStatus.CANCELED)

    def change_status(self, new_status):
        self.status = new_status
        self.save()
        OrderStatusHistory.objects.create(order=self, status=new_status)

    def process_in_office(self, employee):
        """
        Обработка заказа сотрудником офиса.
        """
        self.change_status(OrderStatus.OPERATOR_REVIEW)

    def pass_to_warehouse(self):
        """
        Передача заказа на склад после обработки в офисе.
        """
        if self.status != OrderStatus.OPERATOR_REVIEW:
            raise ValueError("Заказ еще не обработан в офисе.")
        self.change_status(OrderStatus.WAREHOUSE_PROCESSING)

    def pass_to_driver(self):
        """
        Передача заказа водителю для доставки.
        """
        if self.status != OrderStatus.WAREHOUSE_PROCESSING:
            raise ValueError("Заказ должен быть обработан на складе перед передачей водителю.")

        self.status = OrderStatus.DELIVERY
        self.save()
        OrderStatusHistory.objects.create(order=self, status=OrderStatus.DELIVERY)


class OrderStatusHistory(models.Model):
    order = models.ForeignKey('Order', related_name='status_history', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order.id} changed to {self.status} at {self.timestamp}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('MainWepSite.Product', related_name='order_items', on_delete=models.CASCADE)
    product_size = models.ForeignKey('MainWepSite.ProductSize', related_name='order_items', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_at_time_of_purchase = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_sku = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"OrderItem #{self.id} for Order #{self.order.id}"

    def get_total_price(self):
        if self.price_at_time_of_purchase is None:
            return 0
        return self.price_at_time_of_purchase * self.quantity


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)
    is_read = models.BooleanField(default=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


