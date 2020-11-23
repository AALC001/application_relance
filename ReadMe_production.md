# APPOINTMENT SCHEDULING

### Cloner le projet localement sur la machine qui servira de serveur

```
$ git clone https://github.com/projet14/appointment_scheduling.git
```

### Installer Docker

* Windows 10 64-bits, Editions Pro / Entreprise / Education
  * Pré-requis:
    * Les fonctionnalités Windows suivantes doivent être activées : Hyper-V, Containers Windows
    * Processeur 64 bits, avec Second Level Address Translation (SLAT)
    * 4 Gb de mémoire ram
    * Prise en charge de la virtualisation matérielle au niveau BIOS devant être activée dans les réglages du BIOS
  * Exécuter l’installeur au moyen d’un double-clic. Prenez soin de
sélectionner l’option « Enable Hyper-V Windows Features »
lorsque l’option est présentée sur la page de configuration
  * Suivre les instructions suivantes pour terminer l’installation
  * Si votre compte utilisateur n’est pas administrateur, il vous faudra
l’ajouter au groupe docker-users. (Accéder à Gestion de l’ordinateur
-> Groupes et utilisateurs locaux -> Groupes => docker-users, puis
effectuer un clic-droit pour ajouter l’utilisateur. Ensuite se déconnecter
et se reconnecter à la session Windows pour la prise en compte des
modifications
* Windows 10 64-bits Edition Home (version 2004 ou supérieure)
  * Prérequis:
    * Processeur 64 bits, avec Second Level Address Translation (SLAT)
    * 4 Gb de mémoire ram
    * Prise en charge de la virtualisation matérielle au niveau BIOS devant être activée dans les réglages du BIOS
  * Activer la fonctionnalité WSL2 en suivant les instructions au lien
suivant :
https://docs.microsoft.com/en-us/windows/wsl/install-win10
* Télécharger et installer le package de mise à jour du Kernel Linux :
https://docs.microsoft.com/fr-fr/windows/wsl/wsl2-kernel
* Exécuter l’installeur au moyen d’un double-clic. Prenez soin de sélectionner l’option « Enable WSL 2 Features » lorsque l’option est présentée sur la page de configuration
* Suivre les instructions suivantes pour terminer l’installation

### Configurer Docker

* Démarrer l’application Docker Desktop
* Dans ses paramètres, veiller à définir le maximum de mémoire RAM
utilisée à 1 Go
* Et activer le partage de fichiers

### Créer les images et containers nécessaires
* En ligne de commande Powershell, se déplacer dans le dossier relance_patient
* Exécuter la commande suivante : docker-compose up --build
* Patienter le temps que les lignes ci-dessous soient affichées


### Accéder à l’application

Dans un navigateur, accéder à l’adresse http://127.0.0.1:8000
* Dans le fichier relance_patient/start.sh, vous pouvez voir l'utilisateur superadmin
* Ajustez-le au besoin

`DJANGO_SUPERUSER_PASSWORD=my_password python manage.py createsuperuser --no-input --email=my_user@domain.com`
* Remplacez 'my_password'par le mot de passe que vous voulez et 'my_user@domain.com' par votre adresse mail

# Démarrer l’application après un redémarrage de l’ordinateur

* Veiller à ce que le service Docker soit en cours d’exécution
* En ligne de commande Powershell, exécuter la commande suivante
`docker start ap_apps_nginx ap_apps relance_patient_db_1`

### Redémarrer l’application

* Veiller à ce que le service Docker soit en cours d’exécution
* En ligne de commande Powershell, exécuter la commande suivante

`docker restart ap_apps_nginx ap_apps relance_patient_db_1`

### Arrêter l’application

* Veiller à ce que le service Docker soit en cours d’exécution
* En ligne de commande Powershell, exécuter la commande suivante

`docker stop ap_apps_nginx ap_apps relance_patient_db_1`
