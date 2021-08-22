##### Table des matières
- [QuizzPi](#QuizzPi)<br>
- [Installation sur un Raspberry 4](#Install)
- [Connexion à l'interface de gestion](#Connexion)
- [Menu de l'interface de gestion](#Menus)
  - [Catégorie-Questions](#Catégorie-Questions)
  - [Banque de questions](#Banque)

<a name="QuizzPi"></a>

## QuizzPi

Environnement de développement de quizz interactifs sur Raspberry

L'objectif de ce projet et de proposer un environnement autonome s'exécutant sur un Raspberry et permettant à un enseignant d'organiser un quizz interactif avec ses étudiants.

Les questions peuvent intégrées des données aléatoires générées à partir d'un script Python. De même la vérification de la réponse peut être effectué à partir d'un script Python.

QuizzPi autorise la gestion de 2 types de question :

- simple : la réponse est une chaîne de caractères saisie par l'utilisateur,
- multiple : la réponse est choisie en cliquant parmi un ensemble de réponses proposées.

<a name="Install"></a>

## Installation sur un Raspberry 4

<a name="Connexion"></a>
## Connexion à l'interface de gestion

Pour se connecter à l'interface de QuizzPi, il suffit de lancer un navigateur et de saisir l'adresse :

http://192.168.3.14/quizzpi

afin d'obtenir la page d'accueil du site

<img src="img/00_accueil.png">



Via le menu **"Se Connecter"**, l'enseignant entre son login et son mot de passe.

<img src="img/01_login.png">

Une fois identifié, il accède à l'interface de gestion 

<img src="img/02_dashboard.PNG">

<a name="Menus"></a>

## Menus de l'interface de gestion

<a name="Categorie-Questions"></a>

### Catégorie-Questions

Ce menu permet de créer des catégories afin d'y classer les questions. Pour chaque catégorie créée, le nombre de questions présentes dans cette dernière est indiqué entre parenthèses.

<img src="img/03_accueil_cat.PNG">

L'ajout d'une catégorie via  le bouton **+Ajouter** consiste à spécifier le nom de la nouvelle catégorie et à sélectionner sa catégorie parente.

<img src="img/04_creation_cat.PNG">

<a name="Banque"></a>

### Banque de questions

C'est à partir de ce menu que l'on peut lister les questions disponibles, ajouter de nouvelles questions, modifier les questions existantes ou en supprimer certaines.

<img src="img/05_accueil_banque_questions.PNG">

L'option *Choisir une catégorie* permet de n'afficher que les questions de la catégorie sélectionnée. 

La zone de saisie pour la *sélection de filtres* permet de faire une recherche de certaines questions en spécifiant des critères de sélection.

En cliquant sur l'énoncé d'une question, on a un aperçu rapide de son contenu (à ce niveau là pas d'interprétation des graphiques s'il y en a, et pas d'interprétation des variables aléatoires).

<img src="img/06_apercu_intitule_question.PNG">



Pour chaque question affichée, un ensemble d'action est possible via la barre d'icones

<center> <img src="img/07_menu_banque_questions.PNG" height="45"></center>

Les actions disponibles sont (de gauche à droite):

- **Aperçu de la question** : en cliquant sur la loupe, un aperçu de la question tel quelle sera présentée à l'utilisateur final est affichée. Si l'énoncé initial de la question contient des données aléatoires, chaque click sur l'aperçu de la question affiche un énoncé différent.
  <img src="img/08_apercu_questions.PNG">

  Dans la fenêtre d'aperçu, vous pouvez tester votre question en soumettant une réponse (pour l'exemple ci-dessus, en cliquant sur les choix disponibles). Ceci aura pour effet de faire apparaître le bouton Vérifier Réponse qui permettra de contrôler la validité de votre réponse en cliquant dessus. 
  <img src="img/09_verif_reponse.PNG">

- **Edition d'une question** : en cliquant sur le crayon, on accède à l'interface permettant d'éditer les différents paramètres d'une question (voir le paragraphe Création d'une question).

- **Dupliquer une question** : en cliquant sur l'icone représentant deux rectangles superposés, on créé une copie de la question actuelle dans la banque de questions.

- **Supprimer une question** : en cliquant sur l'icone de la poubelle, la question sera effacée. Pour supprimer un ensemble de questions, il suffit de les sélectionner en cliquant sur la case à cocher située à côté du titre de la question, puis de cliquer sur le bouton **Supprimer** situé en bas de page. 
  *Remarque : en cliquant sur la case à cocher située à coté de l'intitulé <font color="blue">Titre</font>, on séléctionne l'ensemble des questions de la catégorie courante.*

  Création d'un question

  

