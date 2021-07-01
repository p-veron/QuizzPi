# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# table contenant la reponse calculee par rapport aux donnees aleatoires et le code de la verification a effectuer
db.define_table('gen_question',Field('Reponse_calcule'),Field('QuestionId'),Field('Verification'),Field('Langage'),Field('user_id','reference auth_user', default=auth.user_id))
# banque de questions
# ici Reponse ne contient pas forcement la vertitable Reponse à la question
# mais plutôt la Réponse à afficher , ce peut donc être éventuellement du code TeX
# la vraie Reponse est stockée dans la bd gen_question
db.define_table('quizz_banque',Field('Titre',length=70,required=True,requires=IS_NOT_EMPTY(),unique=True),
                           Field('Categorie', 'integer', requires=IS_NOT_EMPTY()),
                           Field('Nature',requires=IS_IN_SET(['Simple','Multiple']), sort=True),
                           Field('Points','double',requires=IS_NOT_EMPTY(), searchable=False),
                           Field('Enonce','text',required='True',requires=IS_NOT_EMPTY()),
                           Field('Langage',requires=IS_IN_SET(['Aucun','Python','Sage']), sort=True),
                           Field('Script','text',searchable=False),
                           Field('Melange',requires=IS_IN_SET(['Oui','Non']), sort=False),
                           Field('Choix1',searchable=False),
                           Field('Choix2',searchable=False),
                           Field('Choix3',searchable=False),
                           Field('Choix4',searchable=False),
                           Field('Choix5',searchable=False),
                           Field('Choix6',searchable=False),
                           Field('Choix7',searchable=False),
                           Field('Choix8',searchable=False),
                           Field('Reponse',required='True',requires=IS_NOT_EMPTY(), searchable=False),
                           Field('Verification','text', searchable=False),auth.signature)
#table des quizz
db.define_table('quizz_quizz',Field('Titre',length=70,required=True,requires=[IS_NOT_EMPTY(), IS_MATCH("^[ \-\w]*$",error_message="Enter only letters, numbers, and underscore")],unique=True),
                           Field('Categorie', 'integer', requires=IS_NOT_EMPTY()),
                Field('Questions', 'list:integer'),
                Field('Melange',requires=IS_IN_SET(['Oui','Non']), sort=False),
auth.signature)

#table des categories de questions
db.define_table('categorie_banque',Field('Nom',length=70,required=True,requires=[IS_NOT_EMPTY(),IS_MATCH("^[ \-\w]*$",error_message="Enter only letters, numbers, and underscore")]),
                           Field('Parent_Id','integer',requires=IS_NOT_EMPTY())
               )
#contrainte pour que l'id d'une categorie dans la table des questions soit selectionne a partir de la table des categories pour les questions
db.quizz_banque.Categorie.requires = IS_IN_DB(db,'categorie_banque.id', '%(Nom)s', zero=T('Choisir une categorie'))

#table des categories pour les quizz
db.define_table('categorie_quizz',Field('Nom',length=70,required=True,requires=[IS_NOT_EMPTY(),IS_MATCH("^[ \w]*$",error_message="Enter only letters, numbers, and underscore")]),
                           Field('Parent_Id','integer',requires=IS_NOT_EMPTY())
               )

#contrainte pour que l'id d'une categorie dans la table des quizz soit selectionne a partir de la table des categories pour les quizz
db.quizz_quizz.Categorie.requires = IS_IN_DB(db,'categorie_quizz.id', '%(Nom)s', zero=T('Choisir une categorie'))

# table pour stocker les emails des etudiants et savoir s'ils sont connectes
db.define_table('etudiants',Field('Nom', length=70,required=True,requires=[IS_NOT_EMPTY(),IS_MATCH("^[ \-\w]*$",error_message="Enter only letters, numbers, and underscore")]),Field('Prenom',length=70,required=True,requires=[IS_NOT_EMPTY(),IS_MATCH("^[ \-\w]*$",error_message="Enter only letters, numbers, and underscore")]),Field('Courriel', requires = IS_EMAIL(error_message='invalid email!')), Field('Filiere',requires=[IS_NOT_EMPTY(),IS_MATCH("^[ \w]*$",error_message="Enter only letters, numbers, and underscore")]), Field('logged', 'boolean', default=False), auth.signature)

# table pour stocker le quizz actif et l'id de la question active ainsi que la liste des questions afin de pouvoir gerer le melange des questions
# idrunning=1 pour definir le quizz actif , champ défini pour eviter le pb de la gestion automatique du champ id par web2py si on oublie de reinitialiser la bd
# idquizz : id du quizz actif
# idquestion : id de la question en cours
# liste_choix : liste des choix possibles si c'est une question multiple
# liste_questions : liste des id des questions du quizz actif
# TODO ce dernie champs pourrait etre recupere de la table quizz_quizz

db.define_table('running_quizz',Field('idrunning','integer'),Field('idquizz','integer'),Field('idquestion','integer'),Field('liste_choix','list:string'),Field('liste_questions','list:integer'))

# table pour enregistrer les reponses des etudiants
db.define_table('reponses_etudiants',Field('idquestion','integer'),Field('idetudiant','integer'),Field('reponse',length=80),Field('correct','boolean',default=False),Field('incomplet','boolean',default=False),Field('nonrepondu','boolean',default=False))
