from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path
from .views import register
from backend.views import SyncSupabaseUser  # Import correct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sync-user/', SyncSupabaseUser.as_view(), name='sync_user'),
    path('api/register/', register, name='register'),
]
