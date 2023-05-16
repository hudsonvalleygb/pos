from decimal import Decimal
import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=10)
    overhead = models.DecimalField(default=0.00, decimal_places=2, max_digits=3)
    subtract_cost = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return self.name


class Item(models.Model):
    description = models.CharField(max_length=50)
    size = models.CharField(max_length=6, blank=True)
    quantity = models.IntegerField(default=0)
    sale_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=4)
    cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=4)
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    unlimited = models.BooleanField(default=False)

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
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if self.gross_total > 0:
            expenses = 0
            if self.created_by.userinfo.org.subtract_cost:
                for ti in self.transactionitem_set.all():
                    expenses += ti.item.cost
            self.expenses = expenses
            self.overhead = (self.gross_total - self.expenses) * self.created_by.userinfo.org.overhead
            self.donation_total = (self.gross_total - self.expenses) * (1 - self.created_by.userinfo.org.overhead)
        super().save(*args, **kwargs)


class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    is_limited = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)
