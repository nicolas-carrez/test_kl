import json
import requests
from typing import Any, Dict
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views import View
from .models import Address


class AddressView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        Gère les requêtes POST pour ajouter une adresse à la base de données.

        Args:
            request (HttpRequest): La requête HTTP contenant un champ 'q' avec l'adresse à rechercher.

        Returns:
            JsonResponse: La réponse contenant les détails de l'adresse ou un message d'erreur.
        """
        try:
            # Vérifier que le corps de la requête est un JSON valide
            body: Dict[str, Any] = json.loads(request.body)
            query: str = body.get('q', '')
            if not query or not isinstance(query, str):
                # Si le champ 'q' est manquant ou n'est pas une chaîne
                return JsonResponse(
                    {"error": "Le champ 'q' est requis et doit être une chaîne non vide."},
                    status=400
                )

            # Appel à l'API externe pour rechercher l'adresse
            response = requests.get(
                f"https://api-adresse.data.gouv.fr/search/?q={query}&limit=1"
            )
            # Vérifier si la réponse est valide
            response.raise_for_status()
            data = response.json()

            if data['features']:
                feature = data['features'][0]
                properties = feature['properties']
                geometry = feature['geometry']

                # Vérifier si l'adresse existe déjà dans la base de données
                existing_address = Address.objects.filter(
                    label=properties.get('label'),
                    latitude=geometry['coordinates'][1],
                    longitude=geometry['coordinates'][0]
                ).first()
                if existing_address:
                    # Si l'adresse existe déjà, retourner ses détails
                    return JsonResponse(
                        existing_address.to_dict(),
                        status=200
                    )

                # Créer une nouvelle adresse
                address = Address.objects.create(
                    label=properties.get('label'),
                    name=properties.get('name'),
                    postcode=properties.get('postcode'),
                    citycode=properties.get('citycode'),
                    latitude=geometry['coordinates'][1],
                    longitude=geometry['coordinates'][0],
                )
                # Retourner les détails de l'adresse nouvellement créée
                return JsonResponse(address.to_dict(), status=200)
            else:
                # Si aucune adresse n'est trouvée
                return JsonResponse(
                    {"error": "Adresse non trouvée. Aucun résultat ne correspond à votre recherche."},
                    status=404
                )
        except requests.RequestException:
            # Si la requête à l'API échoue
            return JsonResponse(
                {"error": "Erreur serveur : impossible de contacter l'API externe."},
                status=500
            )
        except json.JSONDecodeError:
            # Si le corps de la requête n'est pas un JSON valide
            return JsonResponse(
                {"error": "Le corps de la requête doit être un JSON valide."},
                status=400
            )


class RiskView(View):
    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        """
        Gère les requêtes GET pour récupérer les risques associés à une adresse.

        Args:
            request (HttpRequest): La requête HTTP.
            id (int): L'identifiant de l'adresse.

        Returns:
            JsonResponse: La réponse contenant les données de risque ou un message d'erreur.
        """
        try:
            # Récupérer l'adresse par son ID
            address = Address.objects.get(id=id)
            # Effectuer la requête à l'API de Géorisques
            response = requests.get(
                f"https://georisques.gouv.fr/api/v1/resultats_rapport_risque?latlon={address.longitude},{address.latitude}"
            )
            # Vérifier si la réponse est valide
            response.raise_for_status()
            return JsonResponse(response.json(), safe=False, status=200)
        except Address.DoesNotExist:
            # Si l'adresse n'existe pas dans la base de données
            return JsonResponse(
                {"error": "Adresse non trouvée."},
                status=404
            )
        except requests.RequestException:
            # Si la requête à l'API échoue
            return JsonResponse(
                {"error": "Erreur serveur : échec de la récupération des données de Géorisques."},
                status=500
            )