from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    AssuranceListView, AssuranceCreateView, AssuranceUpdateView, AssuranceDeleteView,
    BrancheListView, BrancheCreateView, BrancheUpdateView, BrancheDeleteView,
    ClientViewSet, AssuranceViewSet, BrancheViewSet,
    login_view, logout_view, add_employee_view, employee_list_view, home_view
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'assurances', AssuranceViewSet)
router.register(r'branches', BrancheViewSet)

urlpatterns = [
    # --------- URL D'ACCUEIL ---------
    path('', home_view, name='home'),
    
    # --------- URLs D'AUTHENTIFICATION ---------
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # --------- URLs POUR LA GESTION DES EMPLOYÉS (réservé aux admins) ---------
    path('employees/', employee_list_view, name='employee_list'),
    path('employees/add/', add_employee_view, name='add_employee'),
    
    # --------- URLs POUR LES CLIENTS ---------
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_add'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('assurances/', AssuranceListView.as_view(), name='assurance_list'),
    path('assurances/add/', AssuranceCreateView.as_view(), name='assurance_add'),
    path('assurances/<int:pk>/edit/', AssuranceUpdateView.as_view(), name='assurance_edit'),
    path('assurances/<int:pk>/delete/', AssuranceDeleteView.as_view(), name='assurance_delete'),

    path('branches/', BrancheListView.as_view(), name='branche_list'),
    path('branches/add/', BrancheCreateView.as_view(), name='branche_add'),
    path('branches/<int:pk>/edit/', BrancheUpdateView.as_view(), name='branche_edit'),
    path('branches/<int:pk>/delete/', BrancheDeleteView.as_view(), name='branche_delete'),
    path('api/', include(router.urls)),
]