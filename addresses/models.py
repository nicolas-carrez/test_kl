from django.db import models
from typing import Dict, Any


class Address(models.Model):
    """
    Modèle représentant une adresse.

    Attributs :
        label (str) : L'adresse complète sous forme de chaîne.
        name (str) : Le nom ou la description de l'adresse (facultatif).
        postcode (str) : Le code postal de l'adresse (facultatif).
        citycode (str) : Le code INSEE de la ville (facultatif).
        latitude (float) : La latitude de l'adresse (facultatif).
        longitude (float) : La longitude de l'adresse (facultatif).
    """
    label: str = models.CharField(max_length=255)
    name: str = models.CharField(max_length=255, null=True, blank=True)
    postcode: str = models.CharField(max_length=20, null=True, blank=True)
    citycode: str = models.CharField(max_length=20, null=True, blank=True)
    latitude: float = models.FloatField(null=True, blank=True)
    longitude: float = models.FloatField(null=True, blank=True)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'instance du modèle en dictionnaire.

        Returns:
            Dict[str, Any]: Un dictionnaire contenant les détails de l'adresse.
        """
        return {
            "id": self.id,
            "label": self.label,
            "name": self.name,
            "postcode": self.postcode,
            "citycode": self.citycode,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }