from django.urls import path
from . import views
from .views import register_user, login_user
from .views import RegisterAPI
from .views import SyncSupabaseUser
from .models import (
    User,  # Si vous utilisez un modèle User personnalisé
    Joueur,
    Organisateur,
    Arbitre
)
urlpatterns = [
    path('api/sync-user/', SyncSupabaseUser.as_view(), name='sync_user'),
    path('tournois/', views.liste_tournois, name='liste-tournois'),
    path('api/auth/register/', RegisterAPI.as_view(), name='register'),
    path('login/', login_user, name='login'),
]
