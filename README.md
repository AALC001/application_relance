# APPOINTMENT SCHEDULING

### Cloner le projet en local sur votre machine

```
$ git clone https://github.com/projet14/appointment_scheduling.git
```

### Créer un environnement virtuel appelé ```venv``` puis l'activer dans le dossier cloné

* Mac OS & Linux

```
$ cd scheduling_appointment
$ python3 -m venv venv
$ source venv/bin/activate
```

* Sur windows

```
$ venv\Scripts\activate
```

#### Mettre à jour la commande pip

```
$python -m pip install --upgrade pip
```

### Installer les dépendances à l'aide du fichier requirements.txt

```
$ python -m pip install -r requirements.txt
```

### Création et configuration de la base de donnée

Pour la création utiliser le nom de la base de donnée inscrit dans le fichier ```base.py``` qui se trouve dans ```relance_patient/settings``` (paramètre: ```NAME```)

Pour la configuration à la base de donnée adapter le fichier ```base.py``` qui se trouve dans ```relance_patient/settings``` en fonction des configurations de mysql de votre système:

    - Nom utilisateur (USER)
    - Mot de passe (PASSWORD)
    - Adresse serveur (HOST)
    - port (PORT)

### Migrer les changemements dans la base de donnée

```
$ python manage.py makemigrations
$ python manage.py migrate
```
```NB```: Assurez-vous que l'environnment virtuel soit activé

### Création d'un super utilisateur

```
$ python manage.py createsuperuser
```


### Lancer le serveur (Vérifier qu'aucune instance de django est lancée)
```
$ python manage.py runserver
```


***
Le projet est découpé en pluiseurs grandes applications avec des modèles interdépendants. 
* ```authentication``` : pour gérer l'authentification et la gestion des utilisateurs
* ```dashboard```: pour gérer les pages du tableau de bord.

La modification des vues se fait dans chaque application
il est aussi présent dans chaque application un fichier ```urls.py``` différent du fichier ```urls.py``` du projet pour permettre une clarté du code.
