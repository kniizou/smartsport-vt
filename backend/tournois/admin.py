# tournois/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'telephone')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(Utilisateur, CustomUserAdmin)
admin.site.register(Joueur)
admin.site.register(Organisateur)
admin.site.register(Administrateur)
admin.site.register(Arbitre)
admin.site.register(Equipe)
admin.site.register(Tournoi)
admin.site.register(Rencontre)
admin.site.register(Paiement)
