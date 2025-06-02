from django.urls import path

from authentication.views import LoginFormView , RegisterFormView , AuthTemplateView





urlpatterns = [
       path('auth', AuthTemplateView.as_view(), name="auth"),
       path('register', RegisterFormView.as_view(), name="register"),
       path('login', LoginFormView.as_view(), name="login"),
]
