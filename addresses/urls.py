from django.urls import path

from . import views

# Définir les routes pour l'application addresses
urlpatterns = [
    # Route pour ajouter une adresse
    path('', views.AddressView.as_view(), name='address_view'),
    # Route pour obtenir les risques associés à une adresse
    path('<int:id>/risks/', views.RiskView.as_view(), name='risk_view'),
]

