from rest_framework import serializers

# On importe les modèles que l'on veut exposer via l'API
from .models import Client, Assurance, Branche


# Un "serializer" transforme un objet Python/Django
# (par ex. un modèle) en données JSON, et inversement.


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Client.
    ModelSerializer permet de générer automatiquement
    les champs à partir du modèle.
    """

    class Meta:
        # Modèle cible
        model = Client
        # '__all__' = tous les champs du modèle seront sérialisés
        fields = '__all__'


class AssuranceSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Assurance.
    Utilisé dans les vues API (ViewSet) pour créer/lire/modifier/supprimer
    des assurances en JSON.
    """

    class Meta:
        model = Assurance
        fields = '__all__'


class BrancheSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Branche.
    Permet d'exposer les branches de l'assurance via l'API REST.
    """

    class Meta:
        model = Branche
        fields = '__all__'