from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
# Importez les modèles nécessaires
from .models import Joueur, Organisateur, Arbitre

User = get_user_model()


class SyncSupabaseUser(APIView):
    def post(self, request):
        """
        Synchronise un utilisateur Supabase avec la base de données Django
        Attend en paramètres:
        - uid (string): L'ID unique Supabase
        - email (string)
        - username (string, optionnel)
        - role (string: 'joueur', 'organisateur' ou 'arbitre')
        """
        supabase_uid = request.data.get("uid")
        email = request.data.get("email")
        username = request.data.get("username", email.split(
            "@")[0])  # Par défaut: partie avant @
        role = request.data.get("role", "joueur")  # Rôle par défaut: joueur

        # Validation minimale
        if not supabase_uid or not email:
            return Response(
                {"error": "UID and email are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1. Crée ou met à jour l'utilisateur principal
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": username,
                    "supabase_uid": supabase_uid,
                    "role": role,
                    "password": "supabase_no_password_123!"  # Mot de passe factice
                }
            )

            # 2. Si l'utilisateur existait déjà mais sans UID
            if not created and not user.supabase_uid:
                user.supabase_uid = supabase_uid
                user.save()

            # 3. Crée le profil spécifique selon le rôle
            if role == "joueur" and not hasattr(user, 'joueur_profile'):
                Joueur.objects.create(utilisateur=user)
            elif role == "organisateur" and not hasattr(user, 'organisateur_profile'):
                Organisateur.objects.create(
                    utilisateur=user, nom_organisation=username)
            elif role == "arbitre" and not hasattr(user, 'arbitre_profile'):
                Arbitre.objects.create(
                    utilisateur=user, certification="En attente")

            return Response(
                {
                    "status": "success",
                    "user_id": user.id,
                    "created": created
                },
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
