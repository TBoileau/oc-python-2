![Book Online](logo.png)

# Book To Scrape

[![Continuous integration](https://github.com/TBoileau/oc-python-3/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/TBoileau/oc-python-3/actions/workflows/ci.yml)

## Installation
Dans un premier temps, cloner le repository :
```
git clone https://github.com/TBoileau/oc-python-3.git
```

Procéder à l'installation du projet :
```
make install
```

Activer votre environnement :
```
source venv/bin/activate
```

## Usage
Lancer l'application :
```
make run
```

Vous retrouverez les images et les fichiers CSV dans le dossier `dist/[Date et heure]/`.

## Tests
Lancer la suite de tests :
```
make tests
```

*Note : Pour le bon fonctionnement des tests, le serveur HTTP est bouchonné (mock). Vous trouverez dans le dossier `fixtures` les fichiers servies par le serveur HTTP créé spécialement pour les tests.*

## Contribuer
Veuillez prendre un moment pour lire le [guide sur la contribution](CONTRIBUTING.md).

## Changelog
[CHANGELOG.md](CHANGELOG.md) liste tous les changements effectués lors de chaque release.

## À propos
Book To Scrape a été conçu initialement par [Thomas Boileau](https://github.com/TBoileau). 
Ceci est un projet du parcours **Développeur d'application - Python** de la plateforme [Openclassrooms](https://openclassrooms.com/).
Ce projet n'a donc pas vocation a être utilisé.
Si vous avez le moindre question, contactez [Thomas Boileau](mailto:t-boileau@email.com?subject=[Github]%20Book%20To%20Scrape)
