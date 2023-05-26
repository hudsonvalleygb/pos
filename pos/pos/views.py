from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from pytz import timezone

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from .forms import EventForm, NewUserForm
from .models import Event, Item, Transaction, TransactionItem, UserInfo

from pprint import pprint

class POSView(LoginRequiredMixin, TemplateView):
    template_name = 'pos/pos.html'
    login_url = '/users/login/'

    def get(self, request, *args, **kwargs):
        items = Item.objects.filter(org=request.user.userinfo.org)
        events = Event.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now(), org=request.user.userinfo.org)
        if not events:
            events = Event.objects.filter(start_date__gte=datetime.now() - timedelta(days=30), org=request.user.userinfo.org)
        context = self.get_context_data(**kwargs)
        context.update({'items': items, 'events': events})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = request.user
        if 'paid_cash' in request.POST.keys():
            paid_cash = True
        else:
            paid_cash = False
        event_id = int(request.POST['events'])
        event = Event.objects.get(id=event_id)
        count = Transaction.objects.filter(event=event).count()
        context = self.get_context_data(**kwargs)
        # Sanity check quantities
        errors = {}
        quantity_dicts = {x['id']: {'quantity': x['quantity'], 'unlimited': x['unlimited']} for x in Item.objects.all().values('id', 'quantity', 'unlimited')}
        for key, val in request.POST.items():
            if 'quantity' not in key or int(val) == 0:
                continue
            item_id = int(key.split('_')[0])
            if quantity_dicts[item_id]['quantity'] < int(val) and not quantity_dicts[item_id]['unlimited']:
                errors.update({item_id: int(val)})
        if errors:
            items = Item.objects.filter(org=request.user.userinfo.org)
            events = Event.objects.filter(start_date__lte=datetime.now(), end_date__gte=datetime.now(), org=request.user.userinfo.org)
            if not events:
                events = Event.objects.filter(start_date__gte=datetime.now() - timedelta(days=30), org=request.user.userinfo.org)
            for item in items:
                if item.id in errors.keys():
                    item.error = errors[item.id]
            context.update({'errors': errors, 'items': items, 'events': events})
            return self.render_to_response(context)
        # If everything is okay, continue
        transaction = Transaction.objects.create(cash=paid_cash, event=event, description='{0} transaction {1}'.format(event.title, count + 1), created_by=user)
        tis = []
        for key, val in request.POST.items():
            if 'quantity' not in key or int(val) == 0:
                continue
            item_id = int(key.split('_')[0])
            # Sanity check quantities, in case someone else sold some while you were setting up the transaction
            if Item.objects.get(id=item_id).quantity < int(val):
                errors.append({'item': Item.objects.get(id=item_id), 'qty_wanted': int(val)})
            ti = TransactionItem.objects.create(transaction=transaction, item_id=item_id, quantity=int(val))
            tis.append(ti)
        gross_total = 0
        for ti in tis:
            gross_total += ti.item.sale_price * ti.quantity
            if not ti.item.unlimited:
                ti.item.quantity -= ti.quantity
                ti.item.save()
        transaction.gross_total = gross_total
        transaction.save() 
        return HttpResponseRedirect(reverse('transaction_success', args=(transaction.id,))) 


class CreationSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pos/success.html'

    def get_template_names(self):
        if 'event' in self.request.path:
            template_name = 'pos/event_success.html'
        elif 'user' in self.request.path:
            template_name = 'pos/new_user_success.html'
        else:
            template_name = self.template_name
        return [template_name]

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'transaction_id' in kwargs.keys():
            transaction_id = kwargs['transaction_id']
            transaction = Transaction.objects.get(id=transaction_id)
            transaction_items = transaction.transactionitem_set.all()
            context.update({'transaction': transaction, 'transaction_items': transaction_items})
        elif 'event_id' in kwargs.keys():
            event_id = kwargs['event_id']
            event = Event.objects.get(id=event_id)
            context.update({'event': event})
        else:
            user_id = kwargs['user_id']
            new_user = User.objects.get(id=user_id)
            context.update({'new_user': new_user})
        return self.render_to_response(context)
        

class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    login_url = '/users/login/'

    def form_valid(self, form):
        self.object = form.save()
        self.object.org = self.request.user.userinfo.org
        if self.request.user.userinfo.timezone:
            offset = self.calculate_time_offset()
            self.object.start_date += timedelta(hours=offset)
            self.object.end_date += timedelta(hours=offset)
        self.object.save()
        return super(CreateEventView, self).form_valid(form)

    def get_success_url(self):
        return reverse('event_success', args=(self.object.id,))

    def calculate_time_offset(self):
        tz1 = timezone(self.request.user.userinfo.timezone)
        tz2 = timezone('UTC')
        test_date = datetime.now()
        return int((tz1.localize(test_date).astimezone(tz2) - tz2.localize(test_date)).seconds/3600)


class EventListView(LoginRequiredMixin, TemplateView):
    login_url = '/users/login/'
    template_name = 'pos/event_list.html'

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(org=request.user.userinfo.org)
        context = self.get_context_data(**kwargs)
        context.update({'events': events})
        return self.render_to_response(context)


class EventView(LoginRequiredMixin, TemplateView):
    login_url = '/users/login/'
    template_name = 'pos/event_detail.html'

    def get(self, request, *args, **kwargs):
        event_id = int(kwargs['event_id'])
        event = Event.objects.get(id=event_id)
        context = self.get_context_data(**kwargs)
        context.update({'event': event})
        return self.render_to_response(context)
        

class NewUserView(LoginRequiredMixin, CreateView):
    model = User
    form_class = NewUserForm
    login_url = '/users/login/'

    def form_valid(self, form):
        response = super(NewUserView, self).form_valid(form)
        user = self.object
        user.set_password(form.cleaned_data['password'])
        user.is_superuser = True
        user.is_staff = True
        user.save()
        org = self.request.user.userinfo.org
        UserInfo.objects.create(user=user, org=org, is_limited=True)
        return response

    def get_success_url(self):
        return reverse('new_user_success', args=(self.object.id,))
