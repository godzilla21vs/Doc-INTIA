# Doc-INTIA - Système de Gestion d'Assurance

Test pratique fullstack AFREETECH

## 📋 Description

Application web Django pour la gestion d'une compagnie d'assurance avec :
- Gestion des clients
- Gestion des contrats d'assurance
- Gestion des branches/succursales
- Système d'authentification avec rôles (SuperAdmin, BranchAdmin, Agent)
- API REST avec Django REST Framework

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. **Clonez le repository**
```bash
git clone https://github.com/godzilla21vs/Doc-INTIA.git
cd Doc-INTIA/intia_assurance
```

2. **Créez un environnement virtuel**
```bash
python -m venv venv
```

3. **Activez l'environnement virtuel**
   - Sur Windows :
   ```bash
   venv\Scripts\activate
   ```
   - Sur Linux/Mac :
   ```bash
   source venv/bin/activate
   ```

4. **Installez les dépendances**
```bash
pip install -r requirements.txt
```

5. **Effectuez les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créez un superutilisateur**
```bash
python manage.py createsuperuser
```

   Ou utilisez le superutilisateur par défaut :
   - Username : `admin`
   - Password : `admin123`

## 🏃 Lancement du serveur

```bash
python manage.py runserver
```

Par défaut, le serveur démarre sur `http://127.0.0.1:8000/`

Pour utiliser un autre port :
```bash
python manage.py runserver 8001
```

## 🔐 Accès à l'application

- **Application web** : `http://127.0.0.1:8000/`
- **Admin Django** : `http://127.0.0.1:8000/admin/`
- **Page de connexion** : `http://127.0.0.1:8000/login/`
- **API REST** : `http://127.0.0.1:8000/api/`

## 👥 Rôles utilisateurs

- **SuperAdmin** : Accès complet à toutes les fonctionnalités
- **BranchAdmin** : Gestion des employés et des données de sa branche
- **Agent** : Accès limité aux fonctionnalités de base

## 📁 Structure du projet

```
intia_assurance/
├── gestion/              # Application principale
│   ├── models.py         # Modèles (Client, Assurance, Branche, Utilisateur)
│   ├── views.py          # Vues (web et API)
│   ├── forms.py          # Formulaires
│   ├── serializers.py    # Serializers pour l'API REST
│   ├── urls.py           # URLs de l'application
│   ├── admin.py          # Configuration de l'admin Django
│   ├── tests.py          # Tests unitaires
│   └── templates/        # Templates HTML
├── intia_assurance/      # Configuration du projet
│   ├── settings.py       # Paramètres Django
│   └── urls.py           # URLs principales
└── manage.py             # Script de gestion Django
```

## 🧪 Tests

Pour lancer les tests :
```bash
python manage.py test gestion
```

## 📝 Fonctionnalités

- ✅ Authentification et autorisation par rôles
- ✅ CRUD complet pour Clients, Assurances et Branches
- ✅ API REST pour l'intégration avec d'autres applications
- ✅ Interface web moderne avec Bootstrap
- ✅ Tests unitaires pour les modèles, formulaires et vues

## 🛠️ Technologies utilisées

- Django 6.0
- Django REST Framework
- Bootstrap 5
- SQLite (base de données par défaut)

## 📄 Licence

Ce projet est un test pratique pour AFREETECH.

## 👤 Auteur

Test pratique fullstack AFREETECH

