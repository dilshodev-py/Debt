from email.policy import default

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F, Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DetailView, DeleteView, FormView

from apps.forms import DebtModelForm, ContactModelForm, DebtFilterForm, PaymentModelForm
from apps.models import Category, Debt, Contact, Payment


# Create your views here.

class HomeTemplateView(LoginRequiredMixin,TemplateView):
    template_name = 'apps/home.html'
    login_url = reverse_lazy('auth')



class DebtCreateView(CreateView):
    queryset = Debt.objects.all()
    form_class = DebtModelForm
    template_name = 'apps/debt_form.html'
    success_url = reverse_lazy('debt-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.all()
        context['categories'] = Category.objects.all()
        return context


class ContactCreateView(CreateView):
    queryset = Contact.objects.all()
    form_class = ContactModelForm
    template_name = 'apps/contact-form.html'
    success_url = reverse_lazy('home')


class DebtListView(ListView, FormView):
    queryset = Debt.objects.all()
    form_class = DebtFilterForm
    success_url = reverse_lazy('debt-list')
    template_name = 'apps/debt-list.html'
    context_object_name = "debts"

    def form_valid(self, form):
        search = form.cleaned_data.get("search")
        status = form.cleaned_data.get("status")
        category_id = form.cleaned_data.get("category")
        data = {}
        query = Debt.objects.annotate(
            paid_amount=Sum('payments__amount', default=0)
        ).annotate(
            left_amount=F("amount") - F('paid_amount'))
        if search:
            query = query.filter(Q(contact__fullname__icontains=search) | Q(contact__phone_number__icontains=search))
        if status and status != 'all':
            query = query.filter(status=status)
        if category_id and category_id != '-1':
            query = query.filter(category_id=category_id)
        query = query.values(
            'pk',
            'amount',
            'given_date',
            'due_date',
            'category__icon',
            'category__name',
            'status',
            'description',
            'contact__fullname',
            'contact__phone_number',
            'paid_amount',
            'left_amount',
        )
        data['debts'] = query
        data['status_list'] = Debt.StatusType.values
        data['categories'] = Category.objects.all()
        return render(self.request, 'apps/debt-list.html', context=data)

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        query = Debt.objects.annotate(
            paid_amount=Sum('payments__amount', default=0)
        ).annotate(
            left_amount=F("amount") - F('paid_amount')).values(
            'pk',
            'amount',
            'given_date',
            'due_date',
            'category__icon',
            'category__name',
            'status',
            'description',
            'contact__fullname',
            'contact__phone_number',
            'paid_amount',
            'left_amount',
        )
        data['debts'] = query
        data['status_list'] = Debt.StatusType.values
        data['categories'] = Category.objects.all()
        return data


class PaymentHistoryTemplateView(TemplateView):
    template_name = 'apps/payment.html'


class DebtDeleteView(DeleteView):
    queryset = Debt.objects.all()
    template_name = 'apps/debt-list.html'
    success_url = reverse_lazy('debt-list')
    pk_url_kwarg = 'pk'


class PaymentFormView(CreateView):
    queryset = Payment.objects.all()
    form_class = PaymentModelForm
    template_name = 'apps/payment-form.html'
    success_url = reverse_lazy('debt-list')
    context_object_name = 'debt'

    def get_context_data(self, **kwargs):
        debt_id = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        context['debt'] = Debt.objects.filter(pk=debt_id).annotate(
            left_amount=F("amount") - Sum("payments__amount", default=0)).values("pk", 'left_amount').first()
        return context

    def form_valid(self, form):
        debt_id = form.data.get("debt")
        debt = Debt.objects.filter(pk=debt_id).first()
        if debt.left_amount == 0:
            debt.status = Debt.StatusType.PAID.value
            debt.save()
        return super().form_valid(form)
