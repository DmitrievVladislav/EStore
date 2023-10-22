from django.urls import path

from . import views

urlpatterns = [
    path('offers/', views.OfferView.as_view()),
    path('offers/<int:product_id>/', views.SOfferView.as_view())
]
