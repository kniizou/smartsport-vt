# # tournois/serializers.py
# from rest_framework import serializers
# from .models import *


# class UtilisateurSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Utilisateur
#         fields = ['id', 'email', 'first_name', 'last_name', 'role']


# class JoueurSerializer(serializers.ModelSerializer):
#     utilisateur = UtilisateurSerializer()

#     class Meta:
#         model = Joueur
#         fields = '__all__'


# class TournoiSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tournoi
#         fields = '__all__'

# # Ajoutez des serializers pour les autres modèles...

# tournois/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'joueur')
        )
        return user
