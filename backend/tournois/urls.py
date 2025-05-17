from django.urls import path
from . import views
from .views import register_user, login_user

urlpatterns = [
    path('tournois/', views.liste_tournois, name='liste-tournois'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
]
