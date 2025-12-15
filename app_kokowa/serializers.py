from django.contrib.auth.models import User
from rest_framework import serializers
from . import models

class DonateurS(serializers.ModelSerializer):
    class Meta:
        model =  models.Donateur
        fields = ['id', 'nom', 'pays', 'cree_le']
        read_only_fields = ['id', 'cree_le']

class LutteurS(serializers.ModelSerializer):
    class Meta:
        model = models.Lutteur
        fields = ['id', 'nom', 'region', 'poids', 'photo', 'toise', 'total_soutiens', 'en_lisse', 'cree_le']
        read_only_fields = ['id', 'cree_le']

class SoutientS(serializers.ModelSerializer):
    class Meta:
        model = models.Soutient
        fields = ['lutteur', 'raison', 'cree_le']
        read_only_fields = ['cree_le']

class ContributionS(serializers.ModelSerializer):
    class Meta:
        model = models.Contribution
        fields = [
        'id', 'cible', 'donateur', 'montant', 'monnaie', 'pays',
        'statut', 'payment_provider_method', 'payment_ref', 'metadata',
        'cree_le', 'processed_at'
        ]
        read_only_fields = ['id', 'cree_le', 'processed_at']

class AffrontementS(serializers.ModelSerializer):
    class Meta:
        model = models.Affrontement
        fields = ['id', 'l1', 'l2', 'etape', 'date', 'vote1', 'status', 'vote2', 'cree_le']
        read_only_fields = ['id', 'vote1', 'vote2', 'cree_le']


class RegisterS(serializers.ModelSerializer):
    telephone = serializers.CharField(required=True)
    pays = serializers.CharField(required=True)
    region = serializers.CharField(required=True)
    favoris = serializers.UUIDField(required=True)
    #montant = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'password', 'favoris', 'telephone', 'pays', 'region']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        telephone = validated_data.pop('telephone')
        pays = validated_data.pop('pays')
        region = validated_data.pop('region')
        favoris_uuid = validated_data.pop('favoris')
        #montant = validated_data.pop('montant')

        # récupérer lutteur via UUID
        favoris_obj = models.Lutteur.objects.get(pk=favoris_uuid)

        # username = telephone
        username = telephone

        # créer User
        user = User.objects.create_user(
            username=username,
            first_name=validated_data.get('first_name', ''),
            password=validated_data['password']
        )

        # créer Utilisateur
        models.Utilisateur.objects.create(
            user=user,
            telephone=telephone,
            pays=pays,
            region=region,
            favoris=favoris_obj
        )
        #user.montant_initial = montant
        return user


# LOGIN SERIALIZER
class LoginS(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# USER PROFILE SERIALIZER
class UserProfileS(serializers.ModelSerializer):
    class Meta:
        model = models.Utilisateur
        fields = ['id', 'telephone', 'favoris', 'date_creation']
