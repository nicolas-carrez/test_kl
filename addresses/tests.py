import json
from typing import Any
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from .models import Address

class AddressViewTests(TestCase):
    """
    Tests pour la vue AddressView.
    """

    @patch('addresses.views.requests.get')
    def test_post_valid_query_creates_address(self, mock_get: Any) -> None:
        """
        Vérifie qu'une adresse valide est correctement créée et renvoyée.

        Args:
            mock_get (Any): Mock de la fonction requests.get.
        """
        # Simuler une réponse de l'API externe
        mock_response = {
            "features": [
                {
                    "properties": {
                        "label": "123 Main St, Paris",
                        "name": "123 Main St",
                        "postcode": "75001",
                        "citycode": "75101"
                    },
                    "geometry": {
                        "coordinates": [2.3522, 48.8566]
                    }
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Effectuer une requête POST avec une adresse valide
        response = self.client.post(
            reverse('address_view'),
            data=json.dumps({"q": "123 Main St"}),
            content_type="application/json"
        )

        # Vérifier que la réponse est correcte et que l'adresse est créée
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Address.objects.count(), 1)
        address = Address.objects.first()
        self.assertEqual(address.label, "123 Main St, Paris")

    def test_post_invalid_query_returns_400(self) -> None:
        """
        Vérifie qu'une requête avec un champ 'q' invalide retourne une erreur 400.
        """
        # Effectuer une requête POST avec un champ 'q' vide
        response = self.client.post(
            reverse('address_view'),
            data=json.dumps({"q": ""}),
            content_type="application/json"
        )

        # Vérifier que la réponse contient une erreur 400
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    @patch('addresses.views.requests.get')
    def test_post_no_results_returns_404(self, mock_get: Any) -> None:
        """
        Vérifie qu'une requête avec une adresse inexistante retourne une erreur 404.

        Args:
            mock_get (Any): Mock de la fonction requests.get.
        """
        # Simuler une réponse de l'API externe sans résultats
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"features": []}

        # Effectuer une requête POST avec une adresse inexistante
        response = self.client.post(
            reverse('address_view'),
            data=json.dumps({"q": "Nonexistent Address"}),
            content_type="application/json"
        )

        # Vérifier que la réponse contient une erreur 404
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())

class RiskViewTests(TestCase):
    """
    Tests pour la vue RiskView.
    """

    @patch('addresses.views.requests.get')
    def test_get_valid_address_returns_risk_data(self, mock_get: Any) -> None:
        """
        Vérifie qu'une adresse valide retourne les données de risque.

        Args:
            mock_get (Any): Mock de la fonction requests.get.
        """
        # Créer une adresse dans la base de données
        address = Address.objects.create(
            label="123 Main St, Paris",
            name="123 Main St",
            postcode="75001",
            citycode="75101",
            latitude=48.8566,
            longitude=2.3522
        )

        # Simuler une réponse de l'API Géorisques
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"risks": "some risk data"}

        # Effectuer une requête GET pour récupérer les risques
        response = self.client.get(reverse('risk_view', args=[address.id]))

        # Vérifier que la réponse est correcte et contient les données de risque
        self.assertEqual(response.status_code, 200)
        self.assertIn("risks", response.json())

    def test_get_invalid_address_returns_404(self) -> None:
        """
        Vérifie qu'une requête avec une adresse inexistante retourne une erreur 404.
        """
        # Effectuer une requête GET avec un ID d'adresse inexistant
        response = self.client.get(reverse('risk_view', args=[999]))

        # Vérifier que la réponse contient une erreur 404
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())
