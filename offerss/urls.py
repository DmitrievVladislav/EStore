from django.urls import path

from . import views

urlpatterns = [
    path('offerss/', views.OfferView.as_view())
]
