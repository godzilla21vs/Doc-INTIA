from django.db import models
# On importe AbstractUser pour créer un modèle utilisateur personnalisé
# AbstractUser contient déjà username, email, password et d'autres champs utiles
from django.contrib.auth.models import AbstractUser

# --------- MODÈLE BRANCHE ---------
class Branche(models.Model):
    """
    Modèle représentant une branche/succursale de l'assurance.
    """
    nom = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    def __str__(self): return self.nom

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    branche = models.ForeignKey(Branche, on_delete=models.CASCADE)
    date_inscription = models.DateField()
    def __str__(self): return f"{self.nom} {self.prenom}"

class Assurance(models.Model):
    type_assurance = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    branche = models.ForeignKey(Branche, on_delete=models.CASCADE)
    def __str__(self): return f"{self.type_assurance} pour {self.client}"


# --------- MODÈLE UTILISATEUR PERSONNALISÉ ---------
class Utilisateur(AbstractUser):
    
    # Choix pour le champ role (liste de tuples)
    # Format : (valeur_en_base, nom_affiché)
    ROLE_CHOICES = [
        ('SuperAdmin', 'Super Administrateur'),
        ('BranchAdmin', 'Administrateur de Branche'),
        ('Agent', 'Agent'),
    ]
    
    # Champ role avec choix limités
    # max_length=20 car les valeurs les plus longues font 11 caractères
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Agent',  # Par défaut, un nouvel utilisateur est Agent
        help_text="Rôle de l'utilisateur dans le système"
    )
    
    # ForeignKey vers Branche (relation Many-to-One)
    # null=True et blank=True car un SuperAdmin n'a pas forcément de branche
    # on_delete=models.SET_NULL : si la branche est supprimée, branch devient NULL
    branch = models.ForeignKey(
        Branche,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Branche assignée à l'utilisateur (optionnel pour SuperAdmin)"
    )
    
    # Méthode __str__ pour l'affichage dans l'admin et les templates
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    # Méthode pour vérifier si l'utilisateur est SuperAdmin
    def is_super_admin(self):
        """Retourne True si l'utilisateur est SuperAdmin"""
        return self.role == 'SuperAdmin'
    
    # Méthode pour vérifier si l'utilisateur est BranchAdmin
    def is_branch_admin(self):
        """Retourne True si l'utilisateur est BranchAdmin"""
        return self.role == 'BranchAdmin'
    
    # Méthode pour vérifier si l'utilisateur est Agent
    def is_agent(self):
        """Retourne True si l'utilisateur est Agent"""
        return self.role == 'Agent'