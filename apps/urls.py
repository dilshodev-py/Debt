from django.contrib import admin
from django.urls import path, include

from apps.views import HomeTemplateView, DebtCreateView, PaymentHistoryTemplateView, \
       ContactCreateView, DebtListView, DebtDeleteView , PaymentFormView

urlpatterns = [
       path('', HomeTemplateView.as_view() , name='home'),
       path('debt-form', DebtCreateView.as_view() , name='debt-form'),
       path('contact-form', ContactCreateView.as_view() , name='contact-form'),
       path('debt-list', DebtListView.as_view() , name='debt-list'),
       path('debt-delete/<int:pk>', DebtDeleteView.as_view() , name='debt-delete'),
       path('payment-history', PaymentHistoryTemplateView.as_view() , name='payment-history'),
       path('payment-form/<int:pk>', PaymentFormView.as_view() , name='payment-form'),

]