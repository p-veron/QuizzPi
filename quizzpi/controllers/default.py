# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import os
import subprocess
import re
import ast
import sys
from urllib.parse import unquote

def index():
# definir un formulaire pour remplir les champs d'une BD
#    form = SQLFORM(db.quizz_banque).process()
#    rows = db(db.quizz_banque).select()
# il faut penser à modifier le layout
#    return form
    return locals()

def execute_script_verif(rep_etud,qid,Langage,script_verif):
        Langage = "Python"
        #todo pour une prochaine version, integrer verification en Sage
        pid = os.getpid()
        interprete_python = "/usr/bin/python3"
        interprete_sage = "/opt/SageMath/local/bin/python3"
        if (Langage == "Python"):
            run_time_limit = 5 # secondes
            interprete = interprete_python
        else:
            interprete = interprete_sage
            run_time_limit = 7 # secondes            
        if interprete == interprete_sage:
            script = "/tmp/verif_question_"+str(qid)+"_"+str(pid)+".sage.py"
        else:
            script = "/tmp/verif_question_"+str(qid)+"_"+str(pid)+".py"            
        try:
            fic_q = open(script,"wt",encoding="utf-8")
        except Exception as erreur:
            message = "Erreur lors de la sauvegarde de votre script : "+str(erreur)
            return False,message
        else:
            #if interprete == interprete_sage:
            #    fic_q.write("from sage.all_cmdline import *\n")
            #rep_tempo = rep_etud.replace('"',r'\"')
            rep_tempo = rep_etud
            fic_q.write("try:\n    "+rep_tempo+"\nexcept:\n    print('Error')\n")
            fic_q.close()
            env = os.environ.copy()
            env['HOME'] = "/tmp"
            check_script_= subprocess.run([interprete,script],timeout=run_time_limit,universal_newlines=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT, encoding="utf-8",env=env)
            if check_script_.returncode!=0:
                    message = """<strong>Erreur de syntaxe dans votre réponse</strong><br>
"""+check_script_.stdout.lstrip()
                    return False,message
            fic_q = open(script,"wt",encoding="utf-8")
            script_verif = script_verif.replace('reponse_etudiant',rep_etud)    
            fic_q.write(script_verif)
            #fic_q.write(script_verif.replace('"',r'\"')+"\n")
            #if interprete != interprete_python:
            #    fic_q.write("sage_eval('None',cmds=__toexec,locals=__dicX_)\n")
            #if interprete != interprete_python:
            #    fic_q.write('        __retdicX_[__locvar_] = str(__dicX_[__locvar_])\n')
            fic_q.close()
            try:
                # on lance l'execution du script cree
                # les sorties standard et erreur seront recuperees dans check_script_.stdout
                env = os.environ.copy()
                env['HOME'] = "/tmp"
                check_script_= subprocess.run([interprete,script],timeout=run_time_limit,universal_newlines=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT, encoding="utf-8",env=env)
                #check_script_= subprocess.check_output([interprete,script],timeout=run_time_limit,universal_newlines=True,stderr=subprocess.STDOUT, encoding="utf-8",env=env)
            except Exception as erreur:
                message = str(erreur).lstrip().split(' ')
                #message = str(erreur).lstrip()+'\n'+str(erreur.output)
                mess_err = """<strong>Erreur lors de l'exécution
de votre script de vérification:</strong><br>
"""+script+"""
"""+" ".join(message[3:])
                message = mess_err
                #fic_q=open("/tmp/err.txt","w")
                #fic_q.write("ooo : ")
                #fic_q.close()
                return False,message
            else:
                if check_script_.returncode!=0:
                    message = """<strong>Erreur code retour lors de l'exécution
de votre script de vérification:</strong><br>
"""+check_script_.stdout.lstrip()
                    return False,message
                else:
                    return check_script_.stdout.strip(),""
#                return check_script_.strip(),""
        


def verif_reponse():
# fonction utiliser uniquement dans le mode preview
# TODO faire un merge avec ec qui est fait en mode quizzmode
    ok = False
    mess = ""
    if request.args[1] == 'multiple':
        lareponse = ast.literal_eval(request.vars.lareponse)
        labonnereponse = db((db.gen_question.QuestionId == request.args[2]) & (db.gen_question.user_id == auth.user.id)).select(db.gen_question.Reponse_calcule)
        labonnereponse = ast.literal_eval(labonnereponse[0].Reponse_calcule)
        labonnereponse.sort()
        ok = (lareponse == labonnereponse)
        if request.args[0] == 'get':
            return labonnereponse
    else:
        # on est sur une question simple
        champs = db((db.gen_question.QuestionId == request.args[2]) & (db.gen_question.user_id == auth.user.id)).select(db.gen_question.QuestionId,db.gen_question.Langage,db.gen_question.Verification,db.gen_question.Reponse_calcule)
        if request.args[0] == 'get':
            return champs[0].Reponse_calcule
        if champs[0].Verification is None:
            #labonnereponse = db(db.gen_question.QuestionId == request.args[2]).select(db.gen_question.Reponse_calcule)
            labonnereponse = champs[0].Reponse_calcule
            lareponse = unquote(request.vars.lareponse)
            ok = (lareponse == labonnereponse)
        else:
            if request.args[0] == 'get':
                return "A vous de le faire !"
            ok2,mess = execute_script_verif(unquote(request.vars.lareponse),champs[0].QuestionId,champs[0].Langage,champs[0].Verification)
            if mess == "":
                # le script s'est execute
                # soit il a renvoye True car resultat correct
                # soit il a renvoye False car resultat incorrect
                # soit il a renvoye False + message car syntaxe de la reponse incorrect
                ok = (ok2 == 'True')
                if not(ok) and str(ok2[5:])!="":                        
                   mess = '<div class="myerror">'+str(ok2[5:])+'</div>' 
            else:
                ok = False
                mess = '<div class="myerror">'+mess+'</div>'
    #return("<b>"+ok2+"</b>&nbsp;<b>"+mess+"</b>")                
    if ok:    
#        return ("<BR><SPAN style='color:green;'>Bonne r&eacute;ponse !</span>  "+str(lareponse)+" "+str(labonnereponse))
        return ("<SPAN style='color:green;'>&nbsp;Bonne r&eacute;ponse !</span>")
    else:
#        return("<BR><SPAN style='color:red;'>Mauvaise r&eacute;ponse !</span>  "+str(lareponse)+" "+str(labonnereponse))
        return("<SPAN style='color:red;'>&nbsp;Mauvaise r&eacute;ponse !</span><BR>"+mess)
    
def view_enonce():
    enonce = db(db.quizz_banque.id == request.args(0)).select(db.quizz_banque.Titre, db.quizz_banque.Enonce)
    titre, enonce = enonce[0].Titre, enonce[0].Enonce
    return locals()

def preload_question():
  if request.args[0] == 'quizzmode':
      # on met a jour dans la bd du quizz actif, l'id de la question courante
      db(db.running_quizz.idrunning==1).update(idquestion = int(request.args[1]))
  return locals()    

def view_question():
    # lors du clic pour voir une question, on met a jour la bd gen_question 
    # pour consigner la bonne reponse apres interpretation du script python si necessaire
    # ceci permet au script verif_reponse de verifier l'exactitude de la bonne reponse
    # en fonction des données aleatoires générées lors de la visualisation de la question
    # request.args = 0:'quizzmode' ou 'preview', 1:id_question, 2:id_quizz, 3:position_question dans le quizz, 4: nbetudiants
    def update_genquestion(id,Reponse,Script_verif,Lang):
        existe = db((db.gen_question.QuestionId == id) & (db.gen_question.user_id == auth.user.id)).select()
        if len(existe) == 0:
            db.gen_question.insert(Reponse_calcule = Reponse, QuestionId = id, Langage = Lang, Verification = Script_verif)
        else:
            db((db.gen_question.QuestionId == id) & (db.gen_question.user_id == auth.user.id)).update(Reponse_calcule=Reponse, Langage = Lang, Verification = Script_verif)
                
    q_ = db.quizz_banque(request.args(1))
    if request.args[0] == 'quizzmode':
        id_quizz = int(request.args(2))
        position_question = int(request.args(3))
#        liste_questions = db(db.quizz_quizz.id == id_quizz).select(db.quizz_quizz.Questions)
        liste_questions = db(db.running_quizz.idrunning==1).select(db.running_quizz.liste_questions)
#        liste_questions = liste_questions[0].Questions
        liste_questions = liste_questions[0].liste_questions
        b_prev = -1
        b_next = -1
        if position_question > 0:
            position_prev_question = position_question - 1
            id_prev_question = liste_questions[position_prev_question]
            b_prev = XML(P(A(SPAN(_class="icon fa fa-arrow-circle-left fa-lg"),_href=URL('preload_question',args=['quizzmode',id_prev_question,id_quizz,position_prev_question,request.args(4)])),_class='navbar-brand'))
        if position_question < len(liste_questions)-1:
            position_next_question = position_question + 1
            id_next_question = liste_questions[position_next_question]
            b_next = XML(P(A(SPAN(_class="icon fa fa-arrow-circle-right fa-lg"),_href=URL('preload_question',args=['quizzmode',id_next_question,id_quizz,position_next_question,request.args(4)])),_class='navbar-brand'))                        
    num_question = request.args[1]
    if (q_.Langage !='Aucun') and (q_.Script is not None):
        # on va verifier que le temps d'execution du code ne depasse pas
        # le timeout prévu
        pid = os.getpid()
        # tout d'abord on cree un fichier python contenant le source
        # python de la question en rajoutant pour chaque ligne de la forme
        # __val = expression
        # une instruction de la forme print('val_=',val_) 
        # de façon a generer un script qui renvoie sur la sortie standard
        # le nom des variables et leurs valeurs
        interprete_python = "/usr/bin/python3"
        interprete_sage = "/opt/SageMath/local/bin/python3"
        if (q_.Langage == "Python"):
            interprete = interprete_python
            run_time_limit = 5 # secondes
        else:
            interprete = interprete_sage
            run_time_limit = 7 # secondes
        if interprete == interprete_sage:
            script = "/tmp/question_"+str(num_question)+"_"+str(pid)+".sage.py"
        else:
            script = "/tmp/question_"+str(num_question)+"_"+str(pid)+".py"            
        try:
            fic_q = open(script,"wt",encoding="utf-8")
        except Exception as erreur:
            response.flash = "Erreur lors de la sauvegarde de votre script : "+str(erreur)
            return(locals())
        else:
            if interprete == interprete_sage:
                fic_q.write("from sage.all_cmdline import *\n")
            fic_q.write('__toexec="""\n')
            fic_q.write(q_.Script.replace('"',r'\"'))
            fic_q.write('\n"""\n')
            fic_q.write("import re\n__dicX_={}\n")
            if interprete == interprete_python:
                fic_q.write("exec(__toexec,{},__dicX_)")
            else:
                fic_q.write("sage_eval('None',cmds=__toexec,locals=__dicX_)\n")
            fic_q.write("""
__p = re.compile('^\s*(__[^ :]+)$')
__retdicX_ = {}
for __locvar_ in __dicX_:
    __mXx_ = __p.match(__locvar_)
    if __mXx_ is not None:
""")
            if interprete == interprete_python:
                fic_q.write('        __retdicX_[__locvar_] = __dicX_[__locvar_]\n')
            else:
                fic_q.write('        __retdicX_[__locvar_] = str(__dicX_[__locvar_])\n')
            fic_q.write('print(__retdicX_)\n')
            fic_q.close()
            try:
                # on lance l'execution du script cree
                # les sorties standard et erreur seront recuperees dans check_script_.stdout
#                check_script_=subprocess.run(["/usr/bin/python3",script_python],timeout=run_time_limit,universal_newlines=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT, encoding="utf-8")
                env = os.environ.copy()
                env['HOME'] = "/tmp"
#                env['PATH'] = "/home/pascalveron/.local/lib/python3.8/site-packages"
#                env['PYTHONPATH'] = "/home/pascalveron/.local/lib/python3.8/site-packages"        
     
#                check_script_= subprocess.run([interprete,script],timeout=run_time_limit,universal_newlines=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT, encoding="utf-8",env=env)
#                check_script_= subprocess.run([interprete,script],timeout=run_time_limit,universal_newlines=True,text=True,stdout=subprocess.PIPE, encoding="utf-8",env=env)
                check_script_= subprocess.check_output([interprete,script],timeout=run_time_limit,universal_newlines=True,stderr=subprocess.STDOUT, encoding="utf-8",env=env)
            except Exception as erreur:
                #fic_q = open("/tmp/toto.txt","wt",encoding="utf-8")
#                erreur = sys.exc_info()[0]
                message = str(erreur).lstrip()+'<BR>'+str(erreur.output)
                message = message.replace('\n','<BR>')
                #fic_q.write(message)
                #fic_q.close()
                erreur_message = """___Erreur lors de l'exécution
de votre script : 
<BR>"""+script+"""
"""+" "+message
                erreur_message=XML(erreur_message[3:])
                return locals()
            else:
               # if check_script_.returncode!=0:
               #     response.flash = """___Erreur code retour lors de l'exécution
#de votre script :
#"""+check_script_.lstrip()
#                    return(locals())
                # si tout s'est bien passe
                # on evalue la sortie standard de façon à ce que
                # les variables déclarées dans le formulaire
                # soient créées, elles vont être placées dans dico_loc_
                # qui est l'équivalent de locals()
                # le deuxième paramètre de exec est utilisé pour passer
                # le dico globals(), ici c'est inutile
                # on doit placer check_script_ dans dico_loc pour que exec puisse fonctionner
                #dico_loc_= {'q_':q_}
                sortie__ = ast.literal_eval(check_script_)
                #vars_attribute =  re.compile(r'\{\{=__[^ _}]*(_inline-fig|_inline-tex|_center-fig|_center-tex)\}\}')
                vars_attribute =  re.compile(r'\{\{=__[^ _}]*(_inline-fig|_center-fig|_inline-python)\}\}')
                for var_ in sortie__:
                    enonce = q_.Enonce
                    has_attribute = vars_attribute.search(enonce)
                    if has_attribute is not None:
#                        q_.Enonce = enonce.replace('{{='+var_+has_attribute.group(1)+'}}', '``'+str(sortie__[var_])+'``:'+has_attribute.group(1)[1:])
                        q_.Enonce = enonce.replace('{{='+var_+has_attribute.group(1)+'}}', '<div class="'+has_attribute.group(1)[1:]+'">'+str(sortie__[var_])+'</div>')
                    else:
                        q_.Enonce = q_.Enonce.replace('{{='+var_+'}}', str(sortie__[var_]))
                    has_attribute = vars_attribute.search(q_.Reponse)
                    if has_attribute is not None:
                        q_.Reponse = q_.Reponse.replace('{{='+var_+has_attribute.group(1)+'}}', '<div class="'+has_attribute.group(1)[1:]+'">'+str(sortie__[var_])+'</div>')
                    else:
                        q_.Reponse = q_.Reponse.replace('{{='+var_+'}}', str(sortie__[var_]))
                    if (q_.Verification) is not None:
                        q_.Verification = q_.Verification.replace('{{='+var_+'}}', str(sortie__[var_]))    
                    if q_.Nature == 'Multiple':
                        for j in range(1,9):
                            qchoix = q_['Choix'+str(j)]
                            if qchoix is not None:
                                has_attribute = vars_attribute.search(qchoix)
                                if has_attribute is not None:
                                    q_['Choix'+str(j)] = qchoix.replace('{{='+var_+has_attribute.group(1)+'}}', '<div class="'+has_attribute.group(1)[1:]+'">'+str(sortie__[var_])+'</div>')
                                else:
                                    q_['Choix'+str(j)] = qchoix.replace('{{='+var_+'}}',str(sortie__[var_]))
                if q_.Verification is None:
                    update_genquestion(q_.id,q_.Reponse,None,q_.Langage)
                else:
                    update_genquestion(q_.id,q_.Reponse,q_.Verification,q_.Langage)                    
                if request.args[0] == 'quizzmode':
                    return({'q_': q_, 'ok_': num_question, 'b_prev': b_prev, 'b_next': b_next, 'num_question': position_question+1})
                else:
                    return({'q_': q_, 'ok_': num_question})
    update_genquestion(q_.id,q_.Reponse,q_.Verification,None)
    if request.args[0] == 'quizzmode':
        return({'q_': q_, 'ok_': num_question, 'b_prev': b_prev, 'b_next': b_next, 'num_question': position_question+1})
    else:
        return({'q_': q_, 'ok_': num_question})

@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers')) 
def show_selectcat(base1,base2,id_cat,nb_space,id_option_selected,id_cat_select,oncontinue):
# permet de generer le <select></select> contenant l'arborescence des categories
# en excluant les branches filles de id_cat_select et aussi id_cat_select (si cette valeur vaut -1 tout est affiche)
# la fonction est recursive et appelee avec id_cat = id de Racine
#  nb_space permet de gerer les espaces a mettre dans <option> pour simuler le niveau d'arborescence 
# id_option_selected permet de specifier l'option qui doit avoir l'attribut selected
# oncontinue permet de controler le niveau de recursivite
# il prend la valeur False lorsque la categorie courante dans la boucle for vaut id_cat_select
# ainsi on ne parcourera pas les categories filles.
# ceci empeche de pouvoir deplacer une categorie a l'interieur d'elle meme
    if oncontinue:
        rows = db(base1.Parent_Id == id_cat).select(orderby=base1.Nom)
        chaine = ""
        for row in rows:
            nb_questions_in_cat = db(base2.Categorie == row.id).count()
            oncontinue = (row.id != id_cat_select)
            if (row.id == id_option_selected):
                chaine += '<option selected value="'+str(row.id)+'">'
            elif oncontinue:
                chaine += '<option value="'+str(row.id)+'">'
            for j in range(nb_space*2):
                chaine += '&nbsp;'
            chaine+=row.Nom+"&nbsp;("+str(nb_questions_in_cat)+")</option>\n"
            prochain = show_selectcat(base1,base2,row.id,nb_space+2,id_option_selected,id_cat_select,oncontinue)
            if prochain != -1:
                chaine += prochain
        return(chaine)
    else:
        return -1
        
@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers')) 
def manage():
    global categorie_courante
    
    def move_item(liste_id):
        # ici le dernier element de la liste est l'id de la categorie destination
        # les autres elements sont les id des questions
        cat_to_go = liste_id[-1]
        for id in liste_id[:-1]:
            db(banque.id == id).update(Categorie=cat_to_go)
        if banque_name == 'quizz_quizz':
            session.flash = str(len(liste_id)-1)+XML(" quizz(es) déplacé(s)")
        else:
            session.flash = str(len(liste_id)-1)+XML(" question(s) déplacée(s)")

    def delete_item(liste_id):
        for id in liste_id:
            db(banque.id == id).delete()
        if banque_name == 'quizz_quizz':
            session.flash = str(len(liste_id))+XML(" quizz(es) effacée(s)")
        else:
            session.flash = str(len(liste_id))+XML(" question(s) effacée(s)")

    def save_categorie(form):
        # ici on recupere la derniere categorie selectionnee en cas d'erreur dans le formulaire
        global categorie_courante

        categorie_courante = form.vars.Categorie

    def save_or_update(form):
        if banque_name == 'quizz_quizz':
            # on recupere la liste des id pour l'ordre d'affichage des questions
            liste_id_quizz = request.vars.liste_id_quizz.split(':')
            # on met à jour le champ du formulaire contenant cette liste
            # ainsi ceci mettra automatiquement à jour la BD lors de la validation
            # du formulaire
            # si on est sur la page d ecreation d'un quizz, ce champ contiendra par defaut la liste ['-1']
            form.vars.Questions = liste_id_quizz
        # ici on regarde si c'est la premiere sauvegarde d'une nouvelle question
        # auquel cas on cree l'entree dans la BD (form.process()) puis on passe en mode edition
        # ou on quitte le formulaire selon ce que l'utilisateur a choisi
        if (request.vars.justsave == '1' or request.vars.justsave == '3'):
            form.vars.id = banque.insert(**dict(form.vars))
            session.flash = XML("Sauvegarde effectuée")
            if request.vars.justsave == '1':
                redirect(URL('manage', args = [request.args[0],'edit',banque_name, form.vars.id] , user_signature=True))
            else:
                if 'keywords' in request.vars:
                    redirect(URL('manage', args = [request.args[0]], vars=dict(keywords=request.vars.keywords) , user_signature=True,  hash_vars=False))
                else:
                    redirect(URL('manage', args = [request.args[0]], user_signature=True))
        # sinon si c'est une sauvegarde alors que l'on etait en mode edition on fait une mise a jour de la db
        # et on active une erreur invisible, ce qui evite la soumission du formulaire
        elif (request.vars.justsave =='2' or request.vars.justsave =='4'):
            form.record.update_record(**dict(form.vars))
            form.errors.justsave = "Sauvegarde OK"
            response.flash = XML("Sauvegarde effectuée")
            # si justsave vaut4 on veut quitter la page
            if (request.vars.justsave == '4'):
                session.flash = XML("Sauvegarde effectuée")
                # on regarde si une categorie n'a pas ete selectionnee
                # auquel cas il faut revenir avec cette selection active
                if 'keywords' in request.vars:
                    redirect(URL('manage', args = [request.args[0]], vars=dict(keywords=request.vars.keywords) , user_signature=True,  hash_vars=False))
                else:
                    redirect(URL('manage', args = [request.args[0]], user_signature=True))
                
    def check_reponse(form):
        erreur = False
        message_erreur = XML("Votre réponse doit être une liste non vide <b>d'au plus</b> 8 entiers <b>distincts</b> compris entre 1 et 8<br>ou une expression du type <b>{{=__variable}}</b>")
        if (form.vars.Nature == "Multiple"):
            reponse = form.vars.Reponse
            reponse = reponse.strip()
            if ((reponse[0:5] != "{{=__") or reponse[-2:] != "}}"):
                if ((reponse[0] != '[') or (reponse[-1] !=']')):
                    form.errors.Reponse = message_erreur
                    response.flash = XML("Erreur(s) dans le champ Réponse")
                    erreur = True
                else:
                    try:
                        reponse_l = ast.literal_eval(reponse)
                    except:
                        form.errors.Reponse = message_erreur
                        response.flash = XML("Erreur(s) dans le champ Réponse")
                        erreur = True
                    else:
                        reponse_s = set(reponse_l)
                        taille = len(reponse_l)
                        if (taille != len(reponse_s)):
                            form.errors.Reponse = message_erreur
                            response.flash = XML("Erreur(s) dans le champ Réponse")
                            erreur = True
                        else:
                            ok = ((taille <= 8) and isinstance(reponse_l[0],int) and (reponse_l[0] > 0) and (reponse_l[0] < 9))
                            i = 1
                            while ((ok) and ( i < taille)):
                                ok = (isinstance(reponse_l[i],int) and (reponse_l[i] > 0) and (reponse_l[i] < 9))
                                i = i + 1
                            if not(ok):
                                form.errors.Reponse = message_erreur
                                response.flash = XML("Erreur(s) dans le champ Réponse")
                                erreur = True
                            else:
                                reponse_l.sort()
                                form.vars.Reponse = str(reponse_l)
            else:
                #ici on verifie que si la reponse donnee est de la forme {{=_reponse}} que _reponse fait bien partie du script
                reponse = reponse[3:] # on supprime {{= 
                reponse = reponse[:-2] # on supprime }}
                import re
                p = re.compile(reponse+' *=')
                if p.search(form.vars.Script) is None:
                    form.errors.Reponse = XML("Identifiant <B>"+reponse+"</B> inconnu dans le script")
                    response.flash = XML("Erreur(s) dans le champ Réponse")
                    erreur = True
                # il faudrait alors verifier que la variable correspond bien à une liste mais ceci ne peut se faire qu'au moment
                # de l'evaluation de la question. On reporte cette verification dans view_question.html

        if not(erreur):
            save_or_update(form)

    if len(request.args)==0:
       session.flash = XML(request.args)
       redirect(URL('index',user_signature=True))
    tablename = request.args(0)
    banque = db[request.args(0)]
    banque_name = request.args(0)
    banque_categorie_name = request.args(0)+'_Categorie'
    if request.args[0] == 'quizz_banque':
        banque_categorie = db.categorie_banque
        response.view = 'default/manage_questions.html'
    elif request.args[0] == 'quizz_quizz':
        banque_categorie = db.categorie_quizz
        response.view = 'default/manage_quizz.html'
    else:
        redirect(URL('index',user_signature=True))
    # variable utilisee pour afficher correctement en mode edition ou creation la derniere categorie
    # selectionnee en cas de sauvegarde d'un formulaire avec erreur
    racine = db(banque_categorie.Nom == 'Racine').select()
    categorie_courante = racine[0].id
    if 'keywords' in request.vars:
        categorie_courante = request.vars.keywords.split('=')
        if len(categorie_courante)>=2:
            categorie_courante = categorie_courante[1]
            categorie_courante = re.findall(r'\d+', categorie_courante)
            if len(categorie_courante) > 0:
                categorie_courante = int(categorie_courante[0])
            else:
                categorie_courante = racine[0].id
    elif len(request.args)>2:
        if request.args[1] == 'edit':
            # on recupere l'id categorie de l'objet edite
            record = banque(request.args(3)) or redirect(URL('manage',user_signature=True))
            categorie_courante = record.Categorie
    nb_questions_in_racine = db(banque.Categorie == racine[0].id).count()
    banque.modified_on.readable = True
    if tablename == 'quizz_banque':
        mygrid = SQLFORM.grid(db.quizz_banque,args=[request.args(0)],fields=[db.quizz_banque.Titre, db.quizz_banque.Nature, db.quizz_banque.Enonce, db.quizz_banque.Langage, db.quizz_banque.modified_on], headers = {'quizz_banque.Enonce':'Enoncé','quizz_banque.Nature':'Type'}, deletable=True, duplicatable=True, editable=True, showbuttontext=False,selectable = [('Déplacer vers >>',lambda ids : move_item(ids)),('Supprimer',lambda ids : delete_item(ids))],exportclasses=dict(xml=False,html=False,tsv=False,tsv_with_hidden_cols=False,csv=False,csv_with_hidden_cols=False),orderby=db.quizz_banque.modified_on,user_signature=True,onvalidation=check_reponse,onfailure=save_categorie,maxtextlength=65, client_side_delete=True)
    else:
        mygrid = SQLFORM.grid(db.quizz_quizz,args=[request.args(0)], fields=[db.quizz_quizz.Titre], deletable=True, duplicatable=True, editable=True, searchable=True, showbuttontext=False,selectable = [('Déplacer vers >>',lambda ids : move_item(ids)),('Supprimer',lambda ids : delete_item(ids))],exportclasses=dict(xml=False,html=False,tsv=False,tsv_with_hidden_cols=False,csv=False,csv_with_hidden_cols=False),orderby=db.quizz_quizz.modified_on,onvalidation=save_or_update,onfailure=save_categorie,user_signature=True,maxtextlength=40,client_side_delete=True)
        # dans le cas ou on affiche le quizz il faut rajouter un formulaire permettant de selectionner
        # les questions que l'on souhaite enlever du formulaire
        # on passera la liste des id dans un champ cache intitul'e liste_q_to_del
        form_delete = FORM(INPUT(_type='submit', _id="remove_from_quizz", _class="button btn btn-default btn-secondary", _value=XML("Supprimer du quizz la s&eacute;lection")), hidden=dict(liste_q_to_del='-1'),_name='form_delete')
        if form_delete.process(formname='form_delete').accepted:
            # on recupere dans la balise de type hidden la liste des id des questions a supprimer
            liste_q_to_del = request.vars.liste_q_to_del.split(':')
            liste_q_quizz = db(db.quizz_quizz.id == request.args[3]).select(db.quizz_quizz.Questions)
            liste_q_quizz = liste_q_quizz[0].Questions
            #liste_q_before = copy.copy(liste_q_quizz)
            for id_q in liste_q_to_del:
                liste_q_quizz.remove(int(id_q))
            # si la liste est vide on la reinitialise avec -1
            if len(liste_q_quizz) == 0:
                liste_q_quizz = [-1]
            db(db.quizz_quizz.id == request.args[3]).update(Questions = liste_q_quizz)    
            response.flash = str(len(liste_q_to_del))+ XML(' question(s) supprimée(s) du quizz')       
        
    # ajout d'une case a cocher cachee pour gerer les categories a deplacer
    my_extra_element = INPUT(_type='checkbox', _name='records', _id='cat_to_move', _value=racine[0].id)
    mygrid[1][0].append(my_extra_element)
    # ajout d'un input cache pour gerer l'icone "Sauvegarder" en mode creation et edition de question
    my_extra_element = INPUT(_type='hidden', _name='justsave',  _value='0')
    mygrid[1][0].append(my_extra_element)
    # ajout d'un input cache pour gerer l'ordre d'affichage des questions du quizz
    my_extra_element = INPUT(_type='hidden', _name='liste_id_quizz',  _value='-1')
    mygrid[1][0].append(my_extra_element)
    if len(request.args)>1:
        if request.args[1] == 'edit':
            to_select = categorie_courante
        elif request.args[1] == 'new':
#           on recupere la categorie courante
            to_select = categorie_courante
#            response.flash=XML("Yo "+str(to_select))
        elif request.args[1] == 'view' and request.args[2] == 'quizz_banque':
        # ici on est dans la banque des questions et on a clique pour visualiser une question
            redirect(URL('preload_question',args=['preview',request.args[3]], user_signature=True))
        elif len(request.args) > 4:
        # ici on est sur la liste des quizz, on a clique pour ajouter une question et on a clique pour visualiser le contenu d'une question    
            redirect(URL('preload_question',args=['preview',request.args[5]], user_signature=True))            
        elif request.args[1] == 'duplicate':
            new_record = db(banque.id == request.args[3]).select()
            new_record[0].Titre = '(Copie) ' + new_record[0].Titre
            banque.insert(**banque._filter_fields(dict(new_record[0])))
            if banque_name == 'quizz_quizz':
                session.flash = XML("Quizz dupliqué")
            else:
                session.flash = XML("Question dupliquée")
            redirect(URL('manage',args=[request.args[0]],vars=request.vars,user_signature=True))
        elif request.args[1] == 'update':
            to_select = racine[0].id
            # ici on active l'option selectable pour avoir simplement automatiquement les cases a cocher
            # mais la gestion se fait dans la view
            mygrid = SQLFORM.grid(db.quizz_banque,args=[request.args(0),request.args(1),request.args(2)],fields=[db.quizz_banque.Titre, db.quizz_banque.Nature, db.quizz_banque.Enonce, db.quizz_banque.Langage, db.quizz_banque.modified_on], headers = {'quizz_banque.Enonce':'Enoncé','quizz_banque.Nature':'Type'}, deletable=False, duplicatable=False, editable=False, showbuttontext=False,orderby=db.quizz_banque.modified_on,exportclasses=dict(xml=False,html=False,json=False,tsv=False,tsv_with_hidden_cols=False,csv=False,csv_with_hidden_cols=False),selectable = [('Ajouter',lambda ids : none_func(ids))], user_signature=True,maxtextlength=65)
            my_extra_element = INPUT(_type='hidden', _name='liste_id_to_add',  _value='-1')
            mygrid[1][0].append(my_extra_element)   
            form_add = FORM(INPUT(_type='submit', _id="add_to_quizz", _class="button btn btn-default btn-secondary", _value=XML("Ajouter")), hidden=dict(liste_q_to_add='-1'),_name='form_add')
            # variable permettant de savoir si on doit rafraichir la page presentant le contenu du quizz
            refresh_page = 0
            if form_add.process(formname='form_add').accepted:
                # on recupere dans la balise de type hidden la liste des id des questions a ajouter
                # ainsi que l'id du quizz qui est le premier element de la liste
                liste_q_to_add = request.vars.liste_q_to_add.split(':')
                liste_q_to_add = list(map(int,liste_q_to_add))
                id_quizz = liste_q_to_add[0]
                # on recupere la liste actuelle des questions
                liste_q_quizz = db(db.quizz_quizz.id == id_quizz).select(db.quizz_quizz.Questions)
                liste_q_quizz = liste_q_quizz[0].Questions
                if liste_q_quizz[0] == -1:
                    liste_q_quizz = []
                nbq_in_oldquizz = len(liste_q_quizz)
                # on fait l'union des 2 listes
                new_liste_q_quizz = list(dict.fromkeys(liste_q_quizz + liste_q_to_add[1:]))
                if liste_q_quizz != new_liste_q_quizz:
                    db(db.quizz_quizz.id == id_quizz).update(Questions = new_liste_q_quizz)    
                    session.flash = str(len(new_liste_q_quizz)-nbq_in_oldquizz)+ XML(' question(s) ajoutées au quizz')
                else:
                    session.flash = str(XML('Question(s) déjà présente(s) dans le quizz'))                    
                    # on indique a la view qu'elle doit rafraichir l'affichage du quizz
                refresh_page = 1
            response.view = 'default/update_quizz.html'
        __select = show_selectcat(banque_categorie,banque,racine[0].id,1,to_select,-1,True).replace('\n','')
        select_code = XML('<SELECT class="form-control select" name="Categorie" id="'+banque_categorie_name+'"><OPTION value="'+str(racine[0].id)+'">Racine ('+str(nb_questions_in_racine)+')</OPTION>'+__select+'</SELECT>')
        if request.args[1] == 'update':
            racine = db(db.categorie_banque.Nom == 'Racine').select()
            __select = show_selectcat(db.categorie_banque,db.quizz_banque,racine[0].id,1,to_select,-1,True).replace('\n','')
            nb_questions_tot = db(db.quizz_banque).count()
            nb_questions_in_racine = db(db.quizz_banque.Categorie == racine[0].id).count()
            select_code = XML('<SELECT class="form-control select" name="Categorie" id="quizz_banque_Categorie"><OPTION value="-1">Tout ('+str(nb_questions_tot)+')</OPTION><OPTION value="'+str(racine[0].id)+'">Racine ('+str(nb_questions_in_racine)+')</OPTION>'+__select+'</SELECT>')
    else:
        # on est sur la page d'entree de manage/xxxx
        # on recupere le code HTML de l'arborescence des categories
        to_select = racine[0].id
        __select = show_selectcat(banque_categorie,banque,racine[0].id,1,to_select,-1,True).replace('\n','')
        nb_questions_tot = db(banque).count()
        select_code = XML('<SELECT class="form-control select" name="Categorie" id="'+banque_categorie_name+'"><OPTION value="-1">Tout ('+str(nb_questions_tot)+')</OPTION><OPTION value="'+str(racine[0].id)+'">Racine ('+str(nb_questions_in_racine)+')</OPTION>'+__select+'</SELECT>')
        select_move = XML('<SELECT class="select" name="Categorie" id="_move_select"><OPTION value="'+str(racine[0].id)+'">Racine ('+str(nb_questions_in_racine)+')</OPTION>'+__select+'</SELECT>')
        # on cree le bouton ajouter qui permet d'aller sur le formulaire de creation en indiquant que c'est son 1er affichage
#        bouton_ajout = A(SPAN(_class="icon plus icon-plus glyphicon glyphicon-plus"),SPAN('Ajouter',_class="buttontext button",_title="Add record to database"),_class="button btn btn-default btn-secondary", _href=URL('manage_questions',args=['new','quizz_banque'], user_signature=True,  vars=dict(_init='1'), hash_vars=False), _title="Add record to database")
    return locals()
        
@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers')) 
def manage_cat():
    mygrid = SQLFORM.grid(db.categorie_banque, deletable=True, editable=True, showbuttontext=False,user_signature=True)
    return locals()

@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers')) 
def manage_categories():
    def delete_space_and_update(form,id_cat_parent):
        form.vars.Nom = form.vars.Nom.strip()
#        existe = db((db.categorie_banque.Parent_Id == id_cat_parent) & (db.categorie_banque.Nom == form.vars.Nom)).select()
        existe = db((labasecat.Parent_Id == id_cat_parent) & (labasecat.Nom == form.vars.Nom)).select()
        if len(existe)>0:
            cat_parent = labasecat(id_cat_parent)
            form.errors.Nom = XML(form.vars.Nom+' existe d&eacute;j&agrave; dans la cat&eacute;gorie '+cat_parent.Nom);
                # on met a jour l'id du parent dont le nom a ete selectionne
                # via la balise select
        else:
            form.vars.Parent_Id = id_cat_parent

        
    def show_listcat(id_cat):
#        rows = db(db.categorie_banque.Parent_Id == id_cat).select(orderby=db.categorie_banque.Nom)
        rows = db(labasecat.Parent_Id == id_cat).select(orderby=labasecat.Nom)
        chaine = ""
        for row in rows:
            nb_questions_in_cat = db(labase2.Categorie == row.id).count()
            auxchaine = row.Nom+'&nbsp;('+str(nb_questions_in_cat)+')'
            auxchaine += '&nbsp;&nbsp;'+str(A(SPAN(_class="icon trash icon-trash glyphicon glyphicon-trash"), data = {'action': 'delete'} ,_href=URL("manage_categories",args=[request.args(0),"delete",row.id],user_signature=True)))
            auxchaine += '&nbsp;&nbsp;'+str(A(SPAN(_class="icon pen icon-pencil glyphicon glyphicon-pencil"),_href=URL("manage_categories",args=[request.args(0),"edit",row.id],user_signature=True)))
            chaine += str(LI(XML(auxchaine),_class='select_ok'))+'\n'
            souschaine = show_listcat(row.id)
            if souschaine is not None:
                chaine += souschaine
        if len(chaine) > 0:
            return('<UL>\n'+XML(chaine)+'\n</UL>\n')
        else:
            return("")
        
    if len(request.args) == 0:
        response.flash = "Base inexistante"
        return locals()
    if request.args[0] == "question":
        labasecat = db.categorie_banque
        labase2 = db.quizz_banque
    elif request.args[0] == "quizz":
        labasecat = db.categorie_quizz
        labase2 = db.quizz_quizz
    else:
        response.flash = "Base inexistante"
        return locals()
#    racine = db(db.categorie_banque.Nom == 'Racine').select()
    ok_ = 1
    racine = db(labasecat.Nom == 'Racine').select()
#    nb_questions_racine = db(db.quizz_banque.Categorie == racine[0].id).count()
    nb_objets_racine = db(labase2.Categorie == racine[0].id).count()
    if len(request.args)>1:
        if request.args[1] == 'edit':
            # on recupere le nom de la categorie qui est editee
            record = labasecat(request.args(2)) or redirect(URL('manage_categories',args=[request.args[0]],user_signature=True))
            # on recupere les infos sur la categorie parente
#            record_parent = db(db.categorie_banque.id == record.Parent_Id).select(db.categorie_banque.id)
            record_parent = db(labasecat.id == record.Parent_Id).select(labasecat.id)
            nomcategorie = record.Nom
            id_categorie_parent = record.Parent_Id
            id_categorie = record.id
            message = XML('Modification effectu&eacute;e')
            form = SQLFORM(labasecat, record)
        elif request.args[1] == 'new':
            nomcategorie = ""
            id_categorie_parent = racine[0].id
            id_categorie = -1
            message = XML('Ajout effectu&eacute;')
            form = SQLFORM(labasecat)
        elif request.args[1] == 'delete':
            #on verifie si la categorie possede des sous-categories
            vide = db(labasecat.Parent_Id == request.args[2]).select(labasecat.id)
            if len(vide) > 0:
                session.flash = XML("La cat&eacute;gorie contient des sous-cat&eacute;gories, suppression impossible");
            else:
                db(labasecat.id == request.args[2]).delete()
                session.flash = XML("Cat&eacute;gorie supprim&eacute;e");                
            redirect(URL('manage_categories',args=[request.args(0)],user_signature=True))
        if request.args[1] in ['edit','new']:  
            zeform = FORM(DIV(LABEL(labasecat.fields[1],_class='form-control-label col-sm-3'),DIV(INPUT(_name = "Nom", _value = nomcategorie, _class = "form-control string"),_class="col-sm-9"),_class='form-group row'),
                          DIV(LABEL(XML('Cat&eacute;gorie Parente'),_class='form-control-label col-sm-3'),DIV(XML('<SELECT class="form-control select" name="select_id">\n<OPTION value="'+str(racine[0].id)+'">Racine ('+str(nb_objets_racine)+')</OPTION>'+show_selectcat(labasecat,labase2,racine[0].id,1,id_categorie_parent,id_categorie,True)+'</SELECT>'),_class="col-sm-9"),_class='form-group row'), 
                          INPUT(_type='hidden', _name='_formname', _value='editcat'),
                          INPUT(_type='hidden', _name='Parent_Id', _value=id_categorie_parent),
                          INPUT(_type='hidden', _name='id', _value=id_categorie),
                          DIV(DIV(INPUT(_value="Soumettre",_class="btn btn-primary",_type='submit'),_class="col-sm-9 col-sm-offset-3"),_class="form-group row", _id="submit_record__row"),
                          _action='#', _enctype = 'multipart/form-data',_method='post', _class='web2py_form')
            def dsau(form,newval = request.vars.select_id):
                delete_space_and_update(form,newval)
            ok = form.process(session=None,formname='editcat',onvalidation=dsau,  message_onsuccess=message,message_on_failure= 'Erreurs dans le formulaire', next=URL('manage_categories',args=[request.args(0)],user_signature='True')).accepted
                #record.update_record(Parent_Id = request.vars.select_id)
                #session.flash = XML('Modification effectu&eacute;e')
               # redirect(URL('manage_categories',user_signature='True'))
            if form.errors:
                if form.errors.Nom:
                    response.flash = form.errors.Nom
                else:
                    response.flash = 'Erreur(s) dans le formulaire'
            return dict(liste_cat=zeform)
    else:
        menu_ajout = DIV(A(SPAN(_class="icon plus icon-plus glyphicon glyphicon-plus"),SPAN("Ajouter",_class="buttontext button", _title="Add record to database"),_class="button btn btn-default btn-secondary",_href=URL("manage_categories",args=[request.args(0),"new"],vars=dict(_init='1'),user_signature=True)),_class="web2py_console")
        return dict(liste_cat=XML('\n'+XML(menu_ajout)+'\n<BR>\n<UL id="_liste_categories">\n<LI>'+racine[0].Nom+'&nbsp;('+str(nb_objets_racine)+')</LI>\n'+show_listcat(racine[0].id)+'\n</UL><BR>\n'))


@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers'))     
def makeqrcode():
    import socket, qrcode
        
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip = s.getsockname()[0]
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4)
    qr.add_data('https://'+ip+'/quizzpi/runquizz')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("/home/www-data/web2py/applications/quizzpi/static/images/qrcode.png")
    return locals()
    
@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers'))     
def prelaunchquizz():
    # TODO : on pourrait faire un merge de prelaunchquizz et launchquizz
    idquizz = int(request.args[0])
    first_question = db(db.quizz_quizz.id == idquizz).select(db.quizz_quizz.Questions,db.quizz_quizz.Melange,db.quizz_quizz.Titre)
    # on recupere la liste des questions
    liste_q = first_question[0].Questions
    titre = first_question[0].Titre
    first_question = liste_q[0]
    vide=False
    if first_question != -1 :
        form_start = FORM(INPUT(_id='envoi',_type='submit',_class ='button btn btn-default btn-primary',_value='Commencer'),
                              hidden=dict(nbtotaletu='-1'))
        if form_start.process().accepted:
            redirect(URL('launchquizz',args=request.args+[request.vars.nbtotaletu]))
        else:
            # on reinitialise la table des connexions
            db(db.etudiants.id >= 0).update(logged=False)
            # on initialise la table des reponses
            db.reponses_etudiants.truncate()    
            # on initialise la table des questions generees
            db.gen_question.truncate()    
            db.running_quizz.update_or_insert(db.running_quizz.idrunning==1,idrunning=1,idquizz = idquizz)
    else:
        vide = True
    return locals()

@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers'))     
def launchquizz():
    idquizz = int(request.args[0])
    first_question = db(db.quizz_quizz.id == idquizz).select(db.quizz_quizz.Questions,db.quizz_quizz.Melange)
    # on recupere la liste des questions
    liste_q = first_question[0].Questions
    melange = first_question[0].Melange
    first_question = liste_q[0]
    if melange == 'Oui':
        import random
        random.shuffle(liste_q)    
        first_question = liste_q[0]
    db.running_quizz.update_or_insert(db.running_quizz.idrunning==1,idrunning=1,idquizz = idquizz,idquestion = first_question, liste_choix=[], liste_questions=liste_q)
    redirect(URL('preload_question',args=['quizzmode',first_question,idquizz,0,request.args(1)]))
    
@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers')) 
def students():
    def delete_item(liste_id):
        for id in liste_id:
            db(db.etudiants.id == id).delete()
        session.flash = str(len(liste_id))+XML(" étudiants(s) supprimé(s)")
    
    #TODO modifier la base et utiliser le mécanisme de login de web2py
    student_grid = SQLFORM.grid(db.etudiants, fields=[db.etudiants.Nom, db.etudiants.Prenom, db.etudiants.Courriel,db.etudiants.Filiere,db.etudiants.logged], deletable=True, editable=True, duplicatable=False, showbuttontext=False,selectable = [('Supprimer',lambda ids : delete_item(ids))], exportclasses=dict(xml=False,html=False,json=False,tsv=False,tsv_with_hidden_cols=False,csv=False,csv_with_hidden_cols=False), client_side_delete=True, user_signature=True)
    #my_extra_element = INPUT(_type='hidden', _name='liste_st_to_del',  _value='-1')
    #student[1][0].append(my_extra_element)   
    formcsv = FORM(XML('Cliquer sur <B>Parcourir</B> pour importer un fichier CSV '),BR(),BR(),
                       INPUT(_type='file', _name='csvfile'),
                       INPUT(_type='hidden', _value='db.etudiants', _name='table'),BR(),BR(),
                       INPUT(_type='submit', _value=T('import'), _class='btn btn-primary'))
    if formcsv.process().accepted:
        try:
            db.etudiants.import_from_csv_file(request.vars.csvfile.file)
            session.flash = T('Liste mise à jour')
        except Exception as e:
            response.flash = DIV(T('Erreur dans le fichier CSV'), PRE(str(e)))
        else:
            redirect(URL('students',user_signature=True))
    return locals()
    
def preload_resultat():
    # juste utiliser pour lancer la vue correspondante
    return locals()

@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers'))
def show_resultat():
    # code tres similaire a verif_reponse
    # code utilisé pour générer le camembert de la répartition des réponses
    # le & n'est utile que si plusieurs enseignants utilisent quizzpi sur la meme
    # machine. Cette fonctionnalité n'est pas encoe entièrement développé. TODO.
    q_good_answer = db((db.gen_question.QuestionId == request.args[2]) & (db.gen_question.user_id == auth.user.id)).select(db.gen_question.QuestionId,db.gen_question.Langage,db.gen_question.Verification,db.gen_question.Reponse_calcule)
    type_q = 'texte'
    is_multiple = db(db.running_quizz.idrunning == 1).select(db.running_quizz.liste_choix)
    is_multiple = is_multiple[0].liste_choix
    # on regarde si on est sur une question de type choix multiple
    nb_choix = len(is_multiple)
    # compteur pour les réponses incomplètes
    cpt_incomplet = 0
    # compteur pour les bonnes réponses
    cptok = 0
    # compteur du nombre total d'étudiants ayant répondu ou non
    cpt = 0
    # compteur du nombre de réponses reçues
    # NON UTILISE por l'instant
    cpt_rep = 0
    if nb_choix > 0:
        # on est sur une question à choix multiple mais c'est peut être une question
        # de type VRAI ou FAUX  auquel cas on ne devra pas aficher le compteur des réponses incomplètes
        type_q = 'multiple'
        good_answer = ast.literal_eval(q_good_answer[0].Reponse_calcule)
        good_answer.sort()
        nb_good_answer = len(good_answer)
        if nb_good_answer > 1:
            # plusieurs choix sont possibles, on positionne la variable type_q
            # de façon à ce que dans la vue correspondante, le compteur
            # des questions incomplètes ne soit pas affiché
            type_q = 'multiple_answer'
        for reponse in db(db.reponses_etudiants.idquestion == request.args(2)).select(db.reponses_etudiants.reponse,db.reponses_etudiants.idetudiant):
            # on verifie que l'etudiant a repondu
            if reponse.reponse != '__-1__':
                cpt_rep += 1
                # la reponse de l'etudiant est une chaine de car.
                # avec : pour séparateur
                liste_reponse = reponse.reponse.split(":")
                # on la transforme en liste d'entiers
                liste_reponse = list(map(int,liste_reponse))
                liste_reponse.sort()
                if liste_reponse == good_answer:
                    cptok += 1
                    db((db.reponses_etudiants.idquestion == request.args(2)) & (db.reponses_etudiants.idetudiant == reponse.idetudiant)).update(correct=True)
                else:
                    # on vérifie si c'est un sous-ensemble des réponses possibles
                    oncontinue = (liste_reponse[0] in good_answer)
                    j = 1
                    while oncontinue and (j < len(liste_reponse)):
                        oncontinue = (liste_reponse[j] in good_answer)
                        j += 1
                    if oncontinue:
                        cpt_incomplet += 1
                        db((db.reponses_etudiants.idquestion == request.args(2)) & (db.reponses_etudiants.idetudiant == reponse.idetudiant)).update(incomplet=True)
            else:
                 db((db.reponses_etudiants.idquestion == request.args(2)) & (db.reponses_etudiants.idetudiant == reponse.idetudiant)).update(nonrepondu=True)

            # on compte quand même, même si l'étudiant n'a pas répondu            
            cpt += 1
    else:
    # on est sur une simple question ou il faut saisir la reponse
        for reponse in db(db.reponses_etudiants.idquestion == request.args(2)).select(db.reponses_etudiants.reponse,db.reponses_etudiants.idetudiant):
            if reponse.reponse != '__-1__':
                cpt_rep += 1
                if q_good_answer[0].Verification is None:
                    good_answer = q_good_answer[0].Reponse_calcule
                    lareponse = unquote(reponse.reponse)
                    if lareponse == good_answer:
                        cptok += 1
                        db((db.reponses_etudiants.idquestion == request.args(2)) & (db.reponses_etudiants.idetudiant == reponse.idetudiant)).update(correct=True)
                else:
                    ok2,mess = execute_script_verif(unquote(reponse.reponse),q_good_answer[0].QuestionId,q_good_answer[0].Langage,q_good_answer[0].Verification)
                    if mess == "":
                        # le script s'est execute
                        # soit il a renvoye True car resultat correct
                        # soit il a renvoye False car resultat incorrect
                        # soit il a renvoye False + message car syntaxe de la reponse incorrect
                        ok = (ok2 == 'True')
                        if ok:
                            cptok += 1
                            db((db.reponses_etudiants.idquestion == request.args(2)) & (db.reponses_etudiants.idetudiant == reponse.idetudiant)).update(correct=True)
            else:
                # l'etudiant n'a pas repondu
                db((db.reponses_etudiants.idquestion == request.args(2)) & (db.reponses_etudiants.idetudiant == reponse.idetudiant)).update(nonrepondu=True)                
            cpt+=1
    if int(request.args(1)) == -1:
    # on est arrive a la fin du quizz    
        db.running_quizz.truncate()
        db.running_quizz.insert(idrunning=1,idquizz = -1,idquestion=-1, liste_choix=[])
        # on "deconnecte" les etudiants
        db(db.etudiants.id >= 0).update(logged=False)
    return locals()

@auth.requires(auth.has_membership(group_id='superuser') or auth.has_membership(group_id='managers'))
def checkstudent():
    # fonction qui renvoie le nombre d'etudiants connectes
    # ainsi que le nombre d'etudiants ayant repondu
    # request.args(0) = flag, si présent et égal à 0 on veur avoir le nombre d'etudiants qui ont répondu
    # request.args(1) = id question courante
    nbetu = db(db.etudiants.logged == True).count()
    if request.args(0) == '0':
        nbreponse = db(db.reponses_etudiants.idquestion == request.args(1)).count()
        return str(nbreponse)+'/'+str(nbetu)
    else:
        return str(nbetu)

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    # on initialise le quizz actif à -1
    db.running_quizz.truncate()
    db.running_quizz.insert(idrunning=1,idquizz = -1,idquestion=-1, liste_choix=[])
   # on initialise la table des reponses
    db.reponses_etudiants.truncate()
   # on initialise la table des questions generees
    db.gen_question.truncate()
    db(db.etudiants.id >= 0).update(logged=False)
    return dict(form=auth())

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires(auth.has_membership(group_id='superuser')) 
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.grid(db[tablename], args=[tablename], deletable=False, editable=True, user_signature=False)
    return locals()



# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
