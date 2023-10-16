from django.urls import path

from . import views

urlpatterns = [
    path('carts/', views.CartView.as_view()),
    path('carts/<int:cart_id>', views.SingleCartUtils.as_view()),
    ]