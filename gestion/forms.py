from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# On importe get_user_model() pour obtenir notre modèle Utilisateur personnalisé
from django.contrib.auth import get_user_model
from .models import Client, Assurance, Branche, Utilisateur

# On récupère le modèle utilisateur actif (notre Utilisateur personnalisé)
Utilisateur = get_user_model()

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class AssuranceForm(forms.ModelForm):
    class Meta:
        model = Assurance
        fields = '__all__'

class BrancheForm(forms.ModelForm):
    class Meta:
        model = Branche
        fields = '__all__'


# --------- FORMULAIRES D'AUTHENTIFICATION ---------

class LoginForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé.
    Hérite de AuthenticationForm qui gère déjà username et password.
    On peut ajouter du style ou des champs supplémentaires si besoin.
    """
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe'
        })
    )


class AddEmployeeForm(UserCreationForm):
    """
    Formulaire pour ajouter un nouvel employé (réservé aux administrateurs).
    Hérite de UserCreationForm qui gère déjà username, password1, password2.
    On ajoute les champs spécifiques : email, role, branch.
    """
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemple@email.com'
        })
    )
    role = forms.ChoiceField(
        label="Rôle",
        choices=Utilisateur.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    branch = forms.ModelChoiceField(
        label="Branche",
        queryset=Branche.objects.all(),
        required=False,  # Pas obligatoire car SuperAdmin n'a pas de branche
        empty_label="Aucune branche",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'password1', 'password2', 'role', 'branch')
    
    def __init__(self, *args, **kwargs):
        """
        Personnalisation du formulaire pour ajouter des classes CSS aux champs.
        """
        super().__init__(*args, **kwargs)
        # On ajoute des classes Bootstrap à tous les champs
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        """
        Surcharge de la méthode save() pour enregistrer l'email et le role.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.branch = self.cleaned_data.get('branch')  # Peut être None
        
        if commit:
            user.save()
        return user