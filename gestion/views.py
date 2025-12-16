from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Client, Assurance, Branche
from .forms import ClientForm, AssuranceForm, BrancheForm, LoginForm, AddEmployeeForm

# On récupère le modèle utilisateur personnalisé
Utilisateur = get_user_model()
from rest_framework import viewsets
from .serializers import ClientSerializer, AssuranceSerializer, BrancheSerializer

# --------- VUES WEB PROTÉGÉES (nécessitent une connexion) ---------
# LoginRequiredMixin : redirige vers la page de login si l'utilisateur n'est pas connecté
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = '/clients/'

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = '/clients/'

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = '/clients/'

# Web Views pour Assurance (protégées)
class AssuranceListView(LoginRequiredMixin, ListView):
    model = Assurance
    template_name = 'assurance_list.html'
    context_object_name = 'assurances'
    paginate_by = 10

class AssuranceCreateView(LoginRequiredMixin, CreateView):
    model = Assurance
    form_class = AssuranceForm
    template_name = 'assurance_form.html'
    success_url = '/assurances/'

class AssuranceUpdateView(LoginRequiredMixin, UpdateView):
    model = Assurance
    form_class = AssuranceForm
    template_name = 'assurance_form.html'
    success_url = '/assurances/'

class AssuranceDeleteView(LoginRequiredMixin, DeleteView):
    model = Assurance
    success_url = '/assurances/'

# Web Views pour Branche (protégées)
class BrancheListView(LoginRequiredMixin, ListView):
    model = Branche
    template_name = 'branche_list.html'
    context_object_name = 'branches'
    paginate_by = 10

class BrancheCreateView(LoginRequiredMixin, CreateView):
    model = Branche
    form_class = BrancheForm
    template_name = 'branche_form.html'
    success_url = '/branches/'

class BrancheUpdateView(LoginRequiredMixin, UpdateView):
    model = Branche
    form_class = BrancheForm
    template_name = 'branche_form.html'
    success_url = '/branches/'

class BrancheDeleteView(LoginRequiredMixin, DeleteView):
    model = Branche
    success_url = '/branches/'

# API Viewsets
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class AssuranceViewSet(viewsets.ModelViewSet):
    queryset = Assurance.objects.all()
    serializer_class = AssuranceSerializer

class BrancheViewSet(viewsets.ModelViewSet):
    queryset = Branche.objects.all()
    serializer_class = BrancheSerializer


# --------- VUES D'AUTHENTIFICATION ---------

@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vue pour la page de connexion.
    Si l'utilisateur est déjà connecté, on le redirige vers la page d'accueil.
    Sinon, on affiche le formulaire de connexion.
    """
    # Si l'utilisateur est déjà connecté, on le redirige
    if request.user.is_authenticated:
        return redirect('/')
    
    # Si c'est une requête POST (formulaire soumis)
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # On récupère l'utilisateur depuis le formulaire
            user = form.get_user()
            # On connecte l'utilisateur (crée une session)
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} !')
            # On redirige vers la page demandée ou la page d'accueil
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            # Si le formulaire n'est pas valide, on affiche un message d'erreur
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        # Si c'est une requête GET, on affiche le formulaire vide
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def add_employee_view(request):
    """
    Vue pour ajouter un nouvel employé (réservée aux administrateurs).
    Seuls les SuperAdmin et BranchAdmin peuvent créer de nouveaux comptes.
    """
    # Vérification que l'utilisateur est un administrateur
    if not (request.user.is_super_admin() or request.user.is_branch_admin()):
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires pour ajouter un employé.')
        return redirect('/')
    
    # Si c'est une requête POST (formulaire soumis)
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            # On sauvegarde le nouvel employé
            user = form.save()
            messages.success(request, f'Employé {user.username} créé avec succès !')
            return redirect('employee_list')
        else:
            # Si le formulaire n'est pas valide, on affiche les erreurs
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        # Si c'est une requête GET, on affiche le formulaire vide
        form = AddEmployeeForm()
    
    return render(request, 'add_employee.html', {'form': form})


@login_required
def logout_view(request):
    """
    Vue pour la déconnexion.
    Le décorateur @login_required garantit que seul un utilisateur connecté peut se déconnecter.
    """
    # On déconnecte l'utilisateur (supprime la session)
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')


def home_view(request):
    """
    Vue pour la page d'accueil.
    Si l'utilisateur est connecté, on affiche un tableau de bord.
    Sinon, on redirige vers la page de connexion.
    """
    if request.user.is_authenticated:
        return render(request, 'home.html', {'user': request.user})
    else:
        return redirect('login')


@login_required
def employee_list_view(request):
    """
    Vue pour lister tous les employés.
    Accessible seulement aux administrateurs.
    """
    # Vérification que l'utilisateur est un administrateur
    if not (request.user.is_super_admin() or request.user.is_branch_admin()):
        messages.error(request, 'Vous n\'avez pas les permissions nécessaires pour voir la liste des employés.')
        return redirect('/')
    
    # Récupération de tous les utilisateurs
    employees = Utilisateur.objects.all().order_by('username')
    
    return render(request, 'employee_list.html', {'employees': employees})