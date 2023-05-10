from django.contrib import admin

from nested_inline.admin import NestedModelAdmin, NestedTabularInline

from .models import Event, Item, Transaction, TransactionItem


class NestedTransactionItemInline(NestedTabularInline):
    model = TransactionItem
    extra = 0
    readonly_fields = ('total',)

    def total(self, obj):
        return obj.quantity * obj.item.sale_price


class TransactionInline(NestedTabularInline):
    model = Transaction
    extra = 0
    show_change_link = True
    inlines = [NestedTransactionItemInline,]


@admin.register(Event)
class EventAdmin(NestedModelAdmin):
    search_fields = ['title', 'partner']
    list_display = ('title', 'start_date', 'end_date', 'partner')
    ordering = ('start_date',)
    readonly_fields = ['gross_donation', 'expenses', 'overhead', 'total_donation']
    inlines = [TransactionInline,]

    def total_donation(self, obj):
        total = 0
        for transaction in obj.transaction_set.all():
            total += transaction.donation_total
        return total

    def expenses(self, obj):
        total = 0
        for transaction in obj.transaction_set.all():
            total += transaction.expenses
        return total

    def overhead(self, obj):
        total = 0
        for transaction in obj.transaction_set.all():
            total += transaction.overhead
        return total

    def gross_donation(self, obj):
        total = 0
        for transaction in obj.transaction_set.all():
            total += transaction.gross_total
        return total


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'quantity', 'sale_price', 'cost')
    ordering = ('id',)

    def item_name(self, model):
        return model.__str__()


class TransactionItemInline(admin.TabularInline):
    model = TransactionItem
    extra = 0
    readonly_fields = ('total',)

    def total(self, obj):
        return obj.quantity * obj.item.sale_price


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['event']
    list_display = ('id_string', 'event', 'gross_total', 'donation_total', 'created')
    inlines = [TransactionItemInline,]
    ordering = ('-created',)

    def id_string(self, obj):
        trans_id = str(obj.id).split('-')[-1][-4:]
        return obj.description or '{} - transaction {}'.format(obj.event.title, trans_id)

