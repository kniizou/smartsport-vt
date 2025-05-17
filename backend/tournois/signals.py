# tournois/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Utilisateur, Joueur, Organisateur, Administrateur, Arbitre


@receiver(post_save, sender=Utilisateur)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement le profil spécifique selon le rôle"""
    if created:
        if instance.role == 'joueur':
            Joueur.objects.create(utilisateur=instance)
        elif instance.role == 'organisateur':
            Organisateur.objects.create(utilisateur=instance)
        elif instance.role == 'administrateur':
            Administrateur.objects.create(utilisateur=instance)
        elif instance.role == 'arbitre':
            Arbitre.objects.create(utilisateur=instance)


@receiver(post_save, sender=Utilisateur)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde automatiquement le profil spécifique"""
    if instance.role == 'joueur' and hasattr(instance, 'joueur_profile'):
        instance.joueur_profile.save()
    elif instance.role == 'organisateur' and hasattr(instance, 'organisateur_profile'):
        instance.organisateur_profile.save()
    elif instance.role == 'administrateur' and hasattr(instance, 'administrateur_profile'):
        instance.administrateur_profile.save()
    elif instance.role == 'arbitre' and hasattr(instance, 'arbitre_profile'):
        instance.arbitre_profile.save()
