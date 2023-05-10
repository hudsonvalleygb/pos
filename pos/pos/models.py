from decimal import Decimal
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    description = models.CharField(max_length=50)
    size = models.CharField(max_length=6, blank=True)
    quantity = models.IntegerField(default=0)
    sale_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=4)
    cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=4)

    def __str__(self):
        if self.size:
            return self.description + ', ' + self.size
        return self.description

class Event(models.Model):
    title = models.CharField(max_length=200)
    partner = models.CharField(max_length=200)
    host = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)

    def __str__(self):
        return self.title

class Transaction(models.Model):
    description = models.CharField(max_length=200, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items = models.ManyToManyField(Item, through='TransactionItem')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    gross_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    expenses = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    overhead = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    donation_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=5)
    cash = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.gross_total > 0:
            expenses = 0
            for ti in self.transactionitem_set.all():
                expenses += ti.item.cost
            self.expenses = expenses
            self.overhead = (self.gross_total - self.expenses) * Decimal(0.2)
            self.donation_total = (self.gross_total - self.expenses) * Decimal(0.8)
        super().save(*args, **kwargs)

class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
