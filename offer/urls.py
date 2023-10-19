from django.urls import path

from . import views

urlpatterns = [
    path('offer/', views.OfferView.as_view())
]
