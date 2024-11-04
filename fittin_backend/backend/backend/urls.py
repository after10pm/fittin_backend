"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from authorization.views import RegisterView, LoginView, LogoutView, CodeGenerationView, CodeVerificationView, \
    ResetPasswordView, VKLoginView, VKAuthCompleteView
from user.views import UserAPIView
from cart.views import CartView
from products_catalog.views import ProductsView, ProductDetailView, CategoryView
from order.views import OrderView
from payments.views import PayKeeperAPIView, PayKeeperNotificationAPIView


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,

)

urlpatterns = [
    path('registration/', RegisterView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('products/', ProductsView.as_view()),
    path('product/<int:pk>', ProductDetailView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('cart/', CartView.as_view()),
    path('order/', OrderView.as_view()),
    path('generate_code/', CodeGenerationView.as_view()),
    path('verify_code/', CodeVerificationView.as_view()),
    path('reset_password/', ResetPasswordView.as_view()),
    path('auth/', include('social_django.urls', namespace='social')),
    path('auth/login/vk/', VKLoginView.as_view(), name='vk_login'),
    path('auth/vk/complete/', VKAuthCompleteView.as_view(), name='vk_auth_complete'),
    path('paykeeper/payment-link/', PayKeeperAPIView.as_view(), name='paykeeper_payment_link'),
    path('pay/notification/', PayKeeperNotificationAPIView.as_view(), name='paykeeper_notification'),
    re_path(
        r'^swagger(\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

