from django.urls import path

from . import views

urlpatterns = [
    path('offers/', views.OfferView.as_view()),
    path('offers/<int:product_id>/', views.ProductOfferView.as_view())
]
