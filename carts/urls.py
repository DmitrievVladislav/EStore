from django.urls import path

from . import views

urlpatterns = [
    path('carts/', views.CartView.as_view()),
    path('carts/<int:cart_id>', views.SingleCartView.as_view()),
    path('promocodes/', views.PromocodesView.as_view()),
    path('carts/cart_calc/', views.CartCalculationView.as_view()),
]
