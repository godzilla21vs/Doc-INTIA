from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Branche, Client, Assurance, Utilisateur

# On récupère le modèle utilisateur personnalisé
Utilisateur = get_user_model()


# --------- ADMIN POUR LE MODÈLE UTILISATEUR PERSONNALISÉ ---------
@admin.register(Utilisateur)
class UtilisateurAdmin(BaseUserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'role', 'branch', 'is_staff', 'is_active', 'date_joined')
    
    # Filtres dans la barre latérale
    list_filter = ('role', 'branch', 'is_staff', 'is_active', 'date_joined')
    
    # Champs de recherche
    search_fields = ('username', 'email', 'role')
    
    # Organisation des champs dans le formulaire d'édition
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations personnalisées', {
            'fields': ('role', 'branch')
        }),
    )
    
    # Champs à afficher lors de la création d'un nouvel utilisateur
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations personnalisées', {
            'fields': ('email', 'role', 'branch')
        }),
    )


# --------- ADMIN POUR LES AUTRES MODÈLES ---------
admin.site.register(Branche)
admin.site.register(Client)
admin.site.register(Assurance)