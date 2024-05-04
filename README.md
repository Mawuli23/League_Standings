# League_Standings

Cette application permet de faire des classements des équipes de foot après une partie.

## Pour l'utiliser:

1. Télécharge le dépôt.

``` bash
git clone https://github.com/Mawuli23/League_Standings.git
```

2. Se positionner dans le votre dossier de travail et Installer les paquages nécessaire

``` bash
pip install -r Requierements.txt
```

3. lancer l'app : 
``` bash
python manage.py runserver
```
et se rendre sur le lien indiqué

## Pour créer un superutilisateur
``` bash
python manage.py createsuperuser
```

## Ajout d'équipes 
Il faut le faire dans l'interface administrateur en allant sur `localhost:port/admin`

## Ajout de match
Se fait via: `localhost:port/add/`

## Tips:

- en cliquant sur une équipe vous avez les détails des l'ensemble des matchs jouer par ce dernier


