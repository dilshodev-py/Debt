import re
from email.policy import default

from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms import ModelForm, Form
from django.forms.fields import IntegerField, CharField

from apps.models import Debt, Contact, Payment


class DebtModelForm(ModelForm):
    class Meta:
        model = Debt
        fields = 'amount' , 'given_date' , 'due_date' , 'description','category' , 'user' , 'contact'

class ContactModelForm(ModelForm):
    class Meta:
        model = Contact
        fields = 'fullname' , 'phone_number'

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        phone = re.sub(r'\D','', phone)
        return phone

class DebtFilterForm(Form):
    category = CharField(required=False)
    status = CharField(max_length=30 , required=False)
    search = CharField(max_length=255 , required=False)

class PaymentModelForm(ModelForm):
    class Meta:
        model =Payment
        fields = 'amount' , 'debt' , 'paid_date' , 'notes'

    def clean_amount(self):
        payment_amount = self.cleaned_data.get("amount")
        debt_id = self.data.get("debt")
        amount_list = Debt.objects.filter(pk=debt_id).annotate(paid=Sum('payments__amount',default=0)).values('paid' , 'amount').first()
        left_amount = amount_list.get('amount') - amount_list.get('paid')
        if left_amount < payment_amount:
            raise ValidationError("Ortiqcha summa to'lanmoqda !")

        if payment_amount < 0:
            raise ValidationError("To'lov summasi manfiy bo'lmasin!")
        return payment_amount

