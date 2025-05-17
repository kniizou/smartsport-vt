# backend/tournois/apps.py
from django.apps import AppConfig


class TournoisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tournois'  # Doit correspondre exactement au nom du dossier
    # label = 'tournois'  # Optionnel - si présent, doit être unique
