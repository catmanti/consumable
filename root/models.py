"""
This has basic models
"""

from django.db import models
from django.contrib.auth.models import User


class Unit(models.Model):
    """Units Like Planning, Accounting"""

    unit_name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return f"{self.unit_name} - {self.id}"


class Employee(models.Model):
    """Employees like John, Mary, Peter"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=55, unique=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee_name}"


class Item(models.Model):
    """Items like Pens, A4Sheets, Punchers"""

    item_name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return f"{self.item_name}"


class Supplier(models.Model):
    """Suppiers like Paper Corner, Riched Trading"""

    supplier_name = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return f"{self.supplier_name} - {self.id}"


class Order(models.Model):
    """Item orders by Units signing the request form"""

    order_date = models.DateField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order_date} - {self.unit.unit_name}"


class OrderDetail(models.Model):
    """One order items and amounts"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order} - {self.item.item_name}- {self.amount}"


class Stock(models.Model):
    """Stocks avaiable"""

    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    stock_available = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.item.item_name} - {self.stock_available}"
