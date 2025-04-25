from django.db import models

from django.contrib.auth.models import AbstractUser


class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('J', 'Joueur'),
        ('O', 'Organisateur'),
        ('A', 'Administrateur'),
        ('R', 'Arbitre'),
    ]

    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    # Les champs de base comme username, email, password sont déjà dans AbstractUser


class Joueur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True)
    # Autres champs spécifiques au joueur


class Organisateur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True)


class Administrateur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True)


class Arbitre(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur, on_delete=models.CASCADE, primary_key=True)


class Equipe(models.Model):
    nom = models.CharField(max_length=100)
    joueurs = models.ManyToManyField(Joueur)


class Tournoi(models.Model):
    TYPE_CHOICES = [
        ('S', 'Simple elimination'),
        ('D', 'Double elimination'),
        ('R', 'Round-robin'),
    ]

    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    regles = models.TextField()
    organisateur = models.ForeignKey(Organisateur, on_delete=models.CASCADE)
    equipes = models.ManyToManyField(Equipe)


class Match(models.Model):
    STATUT_CHOICES = [
        ('P', 'Planifié'),
        ('E', 'En cours'),
        ('T', 'Terminé'),
    ]

    tournoi = models.ForeignKey(Tournoi, on_delete=models.CASCADE)
    equipe1 = models.ForeignKey(
        Equipe, related_name='matches_equipe1', on_delete=models.CASCADE)
    equipe2 = models.ForeignKey(
        Equipe, related_name='matches_equipe2', on_delete=models.CASCADE)
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    statut = models.CharField(
        max_length=1, choices=STATUT_CHOICES, default='P')
    arbitre = models.ForeignKey(
        Arbitre, on_delete=models.SET_NULL, null=True, blank=True)
    date_heure = models.DateTimeField()


class Paiement(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
