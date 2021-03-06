# Reconnaissance de caractères

## Présentation

Un utilitaire de reconnaissance de caractère pour le projet de POO2 réalisé en Python 3 en utilisant la bibliothèque PyGTK

![Reconnaissance de caractères](img/screenshot.png)

## Auteurs

* François Grabenstaetter
* Danyl El-Kabir

## Utilisation

Le programme essaie de reconnaître le caractère dessiné dans la zone de gauche (penser a choisir le bon type de caractère). Si le caractère reconnu n'est pas le bon, il est possible de corriger cela en faisant ré-apprendre au programme le bon caractère.

Il est possible de remettre les données d'apprentissage par défaut depuis le menu.

**Caractères possibles:**

Tous les caractères sur cette images sont supportés:

![Graffiti dessins](img/graffiti.png)

*Note: Space: SP, Back-Space: BS, Return: CR, Shift: SH, Caps Lock: CL, Tabulation: TB*

## Lancer le programme

```bash
chmod +x run.py
./run.py
```

## Paquets requis

Les paquets suivants sont requis pour le bon fonctionnement du programme (dépendances pkg-config):

- python3 (>= 3.5)
- gtk+-3.0
- pygobject-3.0
- py3cairo
