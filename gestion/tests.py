from django.test import TestCase, Client as DjangoClient
from django.urls import reverse

# On importe les modèles que l'on veut tester
from .models import Client, Assurance, Branche

# On importe les formulaires pour vérifier leur validation
from .forms import ClientForm, AssuranceForm, BrancheForm


# --------- TESTS DES MODÈLES ---------
class ModelTests(TestCase):
    """
    Cette classe contient des tests unitaires pour les modèles Django.
    Chaque méthode test_... vérifie un comportement précis.
    """

    def setUp(self):
        """
        Méthode exécutée avant chaque test.
        On prépare ici des objets en base de données utilisables par les tests.
        """
        # Création d'une branche utilisée par les autres objets
        self.branche = Branche.objects.create(nom="Branche Test", ville="Ville Test")

        # Création d'un client lié à cette branche
        self.client = Client.objects.create(
            nom="Doe",
            prenom="John",
            adresse="Adresse test",
            email="john.doe@example.com",
            telephone="0123456789",
            branche=self.branche,
            date_inscription="2025-01-01",
        )

    def test_client_creation(self):
        """
        Vérifie que la création d'un Client fonctionne
        et que le __str__ renvoie bien le texte attendu.
        """
        # On doit avoir exactement 1 client dans la base
        self.assertEqual(Client.objects.count(), 1)

        # On récupère ce client
        client = Client.objects.first()

        # On vérifie la représentation texte du client (__str__)
        self.assertEqual(str(client), "Doe John")

    def test_assurance_creation(self):
        """
        Vérifie que la création d'une Assurance fonctionne.
        """
        # On crée une assurance liée au client et à la branche
        Assurance.objects.create(
            type_assurance="Auto",
            date_debut="2025-01-01",
            date_fin="2025-12-31",
            montant="1000.00",
            client=self.client,
            branche=self.branche,
        )

        # Il doit maintenant y avoir 1 assurance dans la base
        self.assertEqual(Assurance.objects.count(), 1)

        # On récupère l'assurance
        assurance = Assurance.objects.first()

        # On vérifie que le type "Auto" apparaît dans la chaîne de caractères
        self.assertIn("Auto", str(assurance))


# --------- TESTS DES FORMULAIRES ---------
class FormTests(TestCase):
    """
    Cette classe teste la validation des formulaires (ModelForm).
    L'idée est de vérifier qu'avec des données correctes, le formulaire est valide.
    """

    def setUp(self):
        # Branche utilisée pour remplir les formulaires (champ ForeignKey)
        self.branche = Branche.objects.create(nom="Branche Form", ville="Ville Form")

    def test_client_form_valid(self):
        """
        Vérifie qu'un formulaire ClientForm avec des données valides
        est bien reconnu comme valide.
        """
        data = {
            "nom": "Doe",
            "prenom": "Jane",
            "adresse": "Adresse form",
            "email": "jane.doe@example.com",
            "telephone": "0123456789",
            "branche": self.branche.id,  # on passe l'id de la branche
            "date_inscription": "2025-02-01",
        }
        form = ClientForm(data=data)

        # is_valid() doit renvoyer True
        # form.errors est passé pour afficher les erreurs en cas d'échec du test
        self.assertTrue(form.is_valid(), form.errors)

    def test_assurance_form_valid(self):
        """
        Vérifie qu'un formulaire AssuranceForm est valide
        lorsque toutes les données sont correctes.
        """
        # On a besoin d'un client pour remplir le champ ForeignKey 'client'
        client = Client.objects.create(
            nom="Test",
            prenom="Client",
            adresse="Adresse",
            email="test.client@example.com",
            telephone="0987654321",
            branche=self.branche,
            date_inscription="2025-03-01",
        )

        data = {
            "type_assurance": "Habitation",
            "date_debut": "2025-03-01",
            "date_fin": "2025-12-31",
            "montant": "1500.00",
            "client": client.id,          # id du client
            "branche": self.branche.id,   # id de la branche
        }
        form = AssuranceForm(data=data)

        # On s'attend à ce que le formulaire soit valide
        self.assertTrue(form.is_valid(), form.errors)

    def test_branche_form_valid(self):
        """
        Vérifie qu'un formulaire BrancheForm avec des données simples
        est bien valide.
        """
        data = {"nom": "Nouvelle Branche", "ville": "Nouvelle Ville"}
        form = BrancheForm(data=data)

        self.assertTrue(form.is_valid(), form.errors)


# --------- TESTS DES VUES (Views) ---------
class ViewTests(TestCase):
    """
    Cette classe teste que les vues principales répondent bien (code 200)
    et contiennent un texte clé dans la page HTML.
    """

    def setUp(self):
        # Client HTTP de test fourni par Django (simule un navigateur)
        self.client_http = DjangoClient()

        # On crée des objets pour que les listes ne soient pas vides
        self.branche = Branche.objects.create(nom="Branche Vue", ville="Ville Vue")

        # Client lié à la branche
        self.client_obj = Client.objects.create(
            nom="Vue",
            prenom="Client",
            adresse="Adresse vue",
            email="vue.client@example.com",
            telephone="0102030405",
            branche=self.branche,
            date_inscription="2025-04-01",
        )

        # Assurance liée au client et à la branche
        self.assurance = Assurance.objects.create(
            type_assurance="Santé",
            date_debut="2025-04-01",
            date_fin="2025-12-31",
            montant="2000.00",
            client=self.client_obj,
            branche=self.branche,
        )

    def test_client_list_view_status_code(self):
        """
        Vérifie que la vue de liste des clients renvoie un status code 200
        et contient le bon titre.
        """
        # reverse("client_list") construit l'URL à partir du nom de la route
        url = reverse("client_list")
        response = self.client_http.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liste des Clients")

    def test_assurance_list_view_status_code(self):
        """
        Vérifie que la vue de liste des assurances fonctionne (status 200)
        et contient le bon titre.
        """
        url = reverse("assurance_list")
        response = self.client_http.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liste des Assurances")

    def test_branche_list_view_status_code(self):
        """
        Vérifie que la vue de liste des branches fonctionne (status 200)
        et contient le bon titre.
        """
        url = reverse("branche_list")
        response = self.client_http.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Liste des Branches")

