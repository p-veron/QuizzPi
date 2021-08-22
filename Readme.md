##### Table des matières
- [QuizzPi](#QuizzPi)
- [Installation sur un Raspberry 4](#Install)
- [Connexion à l'interface de gestion](#Connexion)
- [Menus de l'interface de gestion](#Menus)
  - [Catégorie-Questions](#Catégorie-Questions)
  - [Banque de questions](#Banque)
    - [Editer une question](#Editer)
    - [Dupliquer une question](#Dupliquer)
    - [Supprimer une question](#Supprimer)
    - [Ajouter une question](#AjoutQuestion)

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

  Dans la fenêtre d'aperçu, vous pouvez tester votre question en soumettant une réponse (pour l'exemple ci-dessus, en cliquant sur les choix disponibles). Ceci aura pour effet de faire apparaître le bouton **Vérifier Réponse** qui permettra de contrôler la validité de votre réponse en cliquant dessus. 
  <img src="img/09_verif_reponse.PNG">

  <a name="Editer"></a>

- **Editer une question** : en cliquant sur le crayon, on accède à l'interface permettant d'éditer les différents paramètres d'une question (voir le paragraphe [Ajouter une question](#AjoutQuestion)).
  <a name="Dupliquer"></a>

- **Dupliquer une question** : en cliquant sur l'icone représentant deux rectangles superposés, on créé une copie de la question actuelle dans la banque de questions.
  <a name="Supprimer"></a>

- **Supprimer une question** : en cliquant sur l'icone de la poubelle, la question sera effacée. Pour supprimer un ensemble de questions, il suffit de les sélectionner en cliquant sur la case à cocher située à côté du titre de la question, puis de cliquer sur le bouton **Supprimer** situé en bas de page. 
  *Remarque : en cliquant sur la case à cocher située à coté de l'intitulé **Titre** située dans la première ligne de la banque de questions, on séléctionne l'ensemble des questions de la catégorie courante.*
  <a name="AjoutQuestion"></a>
  
- **Ajouter une question** : afin de créer une nouvelle question, il suffit de cliquer sur le bouton **Ajouter**. Les différentes informations à fournir pour élaborer une question sont :
  
  - *Titre* : le titre de la question
  - *Catégorie* : le nom de la catégorie dans laquelle ranger la question
  - *Type* : permet de préciser si la  question est de type simple ou multiple. Par défaut, le type simple est sélectionné. En sélectionnant le type multiple, de nouveaux champs apparaissent permettant de :
    -  préciser si lors de la visualisation de la question, les différents choix possibles doivent être mélangés aléatoirement ou non,
    - proposer jusqu'à 8 choix possibles de réponse.
      <img src="img/11_exemple_multiple.PNG">
  - Points : le nombre de points attribués à la question (non utilisé dans la version actuelle de QuizzPi)
  - Enoncé : l'énoncé de la question.
  - Langage : permet de sélectionner le langage qui sera utilisé pour écrire le script de génération des données aléatoires (Python ou SageMath). Seul Python est géré par la version actuelle de QuizzPi.
  - Réponse : champ contenant la réponse attendue. Ce champ est aussi utilisé pour afficher la réponse aux étudiants lors du déroulement du quizz.
  - Vérification : script Python permettant de vérifier la réponse de l'étudiant. Si ce champ est vide, la réponse de l'étudiant est comparée avec la valeur présente dans le champ *Réponse*. Dans le cas contraire, le concepteur de la question peut utiliser dans le script de vérification la variable prédéfinie reponse_etudiant pour récupérer la réponse de l'étudiant. Dans l'exemple ci-dessous, la réponse correcte est *s=s+i*. Pour éviter de ne pas prendre en compte des réponses du type *s = s + i*  ou *s=   s+i*, on écrit un script de vérification afin de filtrer les espaces présents dans la réponse de l'étudiant.
    <img src="img/10_exemple_verif.PNG">
  
  <a name="Alea"></a>
  
  ## Questions aléatoires
  
  Afin de générer des questions dépendant de données aléatoires, il suffit de sélectionner **Python** dans le champ **Langage** du formulaire de création d'une question. Ceci fait apparaître un nouveau champ intitulé **Script** dans lequel l'utilisateur pourra générer des variables qui pourront être utilisées dans l'énoncé de la question ainsi que dans le champ **Reponse** et les différents champs de Choix dans le cas d'une question à choix multiple. 
  
  **Attention** : dans les champs **Enoncé**, **Reponse** ou les champs **Choix**, on ne peut utiliser qu'une variable définie dans le script, on ne peut pas utiliser une instruction Python.
  
  Dans le script Python, le nom des variables destinées à être utilisées dans les champs **Enoncé** , **Reponse**  ou **Choix** doit commencer par **__**.  
  
  Dans les champs **Enoncé**, **Reponse** ou **Choix**, afin d'utiliser une variable définie dans le script, on utilise la syntaxe **{{__nom-variable}}**.
  
  Dans l'exemple ci-dessous, on créé une question qui demande à l'étudiant de calculer le pgcd de 2 entiers. Les 2 entiers sont générés aléatoirement  grâce à un script Python et la bonne réponse est aussi calculée par le script.
  <img src="img/13_exemple_alea2.PNG">
  
  On utilise alors les 2 variables \_\_val1 et \__val2 dans l'énoncé.
  <img src="img/12_exemple_alea1.PNG">

