from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db.models import CheckConstraint, Q, UniqueConstraint


class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé qui remplace le modèle User par défaut de Django.
    """
    ROLE_CHOICES = [
        ('joueur', 'Joueur'),
        ('organisateur', 'Organisateur'),
        ('administrateur', 'Administrateur'),
        ('arbitre', 'Arbitre'),
    ]

    # On désactive le champ username et on utilise email comme identifiant
    username = None
    email = models.EmailField('email address', unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_inscription = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-date_joined']


class Joueur(models.Model):
    """
    Modèle représentant un joueur, qui hérite de Utilisateur.
    """
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='joueur_profile'
    )

    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('expert', 'Expert'),
    ]

    niveau = models.CharField(
        max_length=20, choices=NIVEAU_CHOICES, default='debutant')
    classement = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    date_naissance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Joueur: {self.utilisateur.get_full_name()}"

    class Meta:
        verbose_name = "Joueur"
        verbose_name_plural = "Joueurs"


class Organisateur(models.Model):
    """
    Modèle représentant un organisateur, qui hérite de Utilisateur.
    """
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='organisateur_profile'
    )
    nom_organisation = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    site_web = models.URLField(blank=True)
    logo = models.ImageField(
        upload_to='organisateurs/logos/', null=True, blank=True)
    est_verifie = models.BooleanField(default=False)

    def __str__(self):
        return f"Organisateur: {self.nom_organisation}"

    class Meta:
        verbose_name = "Organisateur"
        verbose_name_plural = "Organisateurs"


class Administrateur(models.Model):
    """
    Modèle représentant un administrateur, qui hérite de Utilisateur.
    """
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='administrateur_profile'
    )
    niveau_acces = models.CharField(
        max_length=20,
        choices=[('basique', 'Basique'), ('moderateur', 'Modérateur'),
                 ('superadmin', 'Super Admin')],
        default='basique'
    )

    def __str__(self):
        return f"Admin: {self.utilisateur.get_full_name()}"

    class Meta:
        verbose_name = "Administrateur"
        verbose_name_plural = "Administrateurs"


class Arbitre(models.Model):
    """
    Modèle représentant un arbitre, qui hérite de Utilisateur.
    """
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='arbitre_profile'
    )
    certification = models.CharField(max_length=100)
    experience = models.IntegerField(
        default=0, help_text="Années d'expérience")
    specialite = models.CharField(max_length=100, blank=True)
    est_certifie = models.BooleanField(default=False)

    def __str__(self):
        return f"Arbitre: {self.utilisateur.get_full_name()}"

    class Meta:
        verbose_name = "Arbitre"
        verbose_name_plural = "Arbitres"


class Paiement(models.Model):
    """
    Modèle représentant un paiement effectué par un joueur.
    """
    METHODE_CHOICES = [
        ('carte', 'Carte bancaire'),
        ('virement', 'Virement bancaire'),
        ('especes', 'Espèces'),
        ('autre', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('refuse', 'Refusé'),
        ('rembourse', 'Remboursé'),
    ]

    joueur = models.ForeignKey(
        Joueur,
        on_delete=models.PROTECT,
        related_name='paiements'
    )
    montant = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date_paiement = models.DateTimeField(auto_now_add=True)
    methode = models.CharField(max_length=20, choices=METHODE_CHOICES)
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default='en_attente')
    reference = models.CharField(max_length=100, blank=True)
    details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Paiement #{self.id} - {self.montant}€ ({self.get_statut_display()})"

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ['-date_paiement']


class Equipe(models.Model):
    """
    Modèle représentant une équipe eSport.
    """
    nom = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='equipes/logos/', null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    organisateur = models.ForeignKey(
        Organisateur,
        on_delete=models.CASCADE,
        related_name='equipes'
    )
    jeu = models.CharField(
        max_length=100, help_text="Jeu principal de l'équipe")
    tag = models.CharField(max_length=10, blank=True,
                           help_text="Tag court de l'équipe (ex: FNC)")

    def __str__(self):
        return f"{self.nom} ({self.tag})" if self.tag else self.nom

    class Meta:
        verbose_name = "Équipe"
        verbose_name_plural = "Équipes"
        ordering = ['nom']


class JoueurEquipe(models.Model):
    """
    Table de liaison pour la relation many-to-many entre Joueur et Equipe.
    """
    ROLE_CHOICES = [
        ('capitaine', 'Capitaine'),
        ('membre', 'Membre'),
        ('remplacant', 'Remplaçant'),
    ]

    joueur = models.ForeignKey(
        Joueur,
        on_delete=models.CASCADE,
        related_name='membre_equipes'
    )
    equipe = models.ForeignKey(
        Equipe,
        on_delete=models.CASCADE,
        related_name='membres'
    )
    date_ajout = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='membre'
    )
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.joueur} dans {self.equipe} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Membre d'équipe"
        verbose_name_plural = "Membres d'équipe"
        constraints = [
            UniqueConstraint(
                fields=['joueur', 'equipe'],
                name='unique_joueur_equipe'
            )
        ]


class Tournoi(models.Model):
    """
    Modèle représentant un tournoi eSport.
    """
    TYPE_CHOICES = [
        ('elimination', 'Élimination simple'),
        ('round-robin', 'Round Robin'),
        ('mixte', 'Format mixte'),
    ]
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    regles = models.TextField(blank=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    prix_inscription = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='planifie'
    )
    organisateur = models.ForeignKey(
        Organisateur,
        on_delete=models.CASCADE,
        related_name='tournois'
    )
    jeu = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to='tournois/logos/', null=True, blank=True)
    nombre_equipes_max = models.PositiveIntegerField(default=16)
    recompense = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Récompense totale pour le tournoi"
    )

    def __str__(self):
        return f"{self.nom} ({self.get_statut_display()})"

    class Meta:
        verbose_name = "Tournoi"
        verbose_name_plural = "Tournois"
        ordering = ['-date_debut']
        constraints = [
            CheckConstraint(
                check=Q(date_fin__gt=models.F('date_debut')),
                name='check_date_fin_apres_debut'
            )
        ]


class Rencontre(models.Model):
    """
    Modèle représentant un match entre deux équipes.
    """
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
        ('reporte', 'Reporté'),
    ]

    tournoi = models.ForeignKey(
        Tournoi,
        on_delete=models.CASCADE,
        related_name='rencontres'
    )
    nom = models.CharField(max_length=100, blank=True)
    date_heure = models.DateTimeField()
    duree = models.PositiveIntegerField(
        help_text="Durée estimée en minutes",
        null=True,
        blank=True
    )
    score_equipe1 = models.PositiveIntegerField(null=True, blank=True)
    score_equipe2 = models.PositiveIntegerField(null=True, blank=True)
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='planifie'
    )
    equipe1 = models.ForeignKey(
        Equipe,
        on_delete=models.CASCADE,
        related_name='rencontres_equipe1'
    )
    equipe2 = models.ForeignKey(
        Equipe,
        on_delete=models.CASCADE,
        related_name='rencontres_equipe2'
    )
    arbitre = models.ForeignKey(
        Arbitre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rencontres_arbitrees'
    )
    terrain = models.CharField(max_length=100, blank=True)
    stream_url = models.URLField(blank=True)
    vod_url = models.URLField(
        blank=True, help_text="Lien vers la vidéo du match")

    def __str__(self):
        return f"{self.equipe1} vs {self.equipe2} - {self.tournoi}"

    class Meta:
        verbose_name = "Rencontre"
        verbose_name_plural = "Rencontres"
        ordering = ['date_heure']
        constraints = [
            CheckConstraint(
                check=~Q(equipe1=models.F('equipe2')),
                name='check_equipes_differentes'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.nom:
            self.nom = f"{self.equipe1} vs {self.equipe2}"
        super().save(*args, **kwargs)
