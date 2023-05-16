from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
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
        transaction = Transaction.objects.create(cash=paid_cash, event=event, description='{0} transaction {1}'.format(event.title, count + 1), created_by=user)
        tis = []
        for key, val in request.POST.items():
            if 'quantity' not in key:
                continue
            if int(val) == 0:
                continue
            item_id = int(key.split('_')[0])
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
        context = self.get_context_data(**kwargs)
        return HttpResponseRedirect(reverse('transaction_success', args=(transaction.id,))) 


def transaction_success(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'pos/success.html', {'transaction': transaction})


class CreateEventView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    login_url = '/users/login/'

    def form_valid(self, form):
        self.object = form.save()
        self.object.org = self.request.user.userinfo.org
        self.object.save()
        return super(CreateEventView, self).form_valid(form)

    def get_success_url(self):
        return reverse('event_success', args=(self.object.id,))


def event_created(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'pos/event_success.html', {'event': event})


class EventListView(LoginRequiredMixin, TemplateView):
    login_url = '/users/login/'
    template_name = 'pos/event_list.html'

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(org=request.user.userinfo.org)
        context = self.get_context_data(**kwargs)
        context.update({'events': events})
        return self.render_to_response(context)
        


class NewUserView(LoginRequiredMixin, CreateView):
    model = User
    form_class = NewUserForm
    login_url = '/users/login/'

    def form_valid(self, form):
        import pdb; pdb.set_trace()
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


def new_user_created(request, user_id):
    new_user = get_object_or_404(User, pk=user_id)
    return render(request, 'pos/new_user_success.html', {'new_user': new_user})
