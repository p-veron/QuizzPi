def index():
    
    def check_email(form):
        global id_etud
        id_etud = db(db.etudiants.Courriel == form.vars.email).select(db.etudiants.id,db.etudiants.logged)
        if len(id_etud) == 0:
            form.errors.email = 'Identifiant inconnu'
        elif id_etud[0].logged:
            form.errors.email = 'Vous êtes déjà connecté'
        else:
            id_etud = id_etud[0].id
    
    message = ""
    form_ident = FORM(DIV(LABEL('e-mail : ', _class="form-control-label col-sm-3", _for="auth_user_email", _id="auth_user_email__label"),
         DIV(INPUT(_class="form-control string",_id="auth_user_email",_name="email",_type="text",_value="", requires=IS_EMAIL(error_message=T('invalid email'))),_class="col-sm-9"),_class="form-group row", _id="auth_user_email__row"),
        DIV(DIV(INPUT(_type='submit', _value=T('Connexion'), _class='btn btn-primary'),_class="col-sm-9 col-sm-offset-3"),_id="submit_record__row",_class="form-group row"))
    if form_ident.process(onvalidation=check_email,keepvalues=True).accepted:
        id_running_quizz = db(db.running_quizz.idrunning==1).select()
        # zapette recoit l'id de l'etudiant, l'id du quizz actif et l'id la question actuelle 
        idquizz = id_running_quizz[0].idquizz
        if idquizz != -1:
            #liste_questions = db(db.quizz_quizz.id==idquizz).select(db.quizz_quizz.Questions)
            db(db.etudiants.id == id_etud).update(logged=True)
            current_q = db(db.running_quizz.idrunning==1).select(db.running_quizz.idquestion)
            current_q = current_q[0].idquestion
            redirect(URL('zapette',args=[id_etud,idquizz,current_q]))
        else:
            message = XML("Le quizz n'est pas encore lan&ccedil;&eacute;")
    return locals()


def record_reponse():
    lareponse = request.vars.lareponse
    db.reponses_etudiants.update_or_insert((db.reponses_etudiants.idquestion == request.args(1)) & (db.reponses_etudiants.idetudiant == request.args(0)),idquestion = request.args(1),idetudiant = request.args(0),reponse=lareponse)
    message = XML("R&eacute;ponse enregistr&eacute;e")
    return message

def zapette():
    # request.args = id_etud(0) id_quizz(1) id_question que l'etudiant veut voir(2)
    # attention cette id_question n'est pas forcement l'id de la question en cours de projection
    # On verfiei si aucune question n'est active
    if int(request.args[2])==-1:
        contenu = DIV(IMG(_src=URL("static", "images",args="patience.gif"),_width='95%'),P(B(XML("Patience ..., r&eacute;essayez dans quelques secondes"),_class="patience")),_class="text-center")   
        # on interroge à nouveau la BD pour voir si un quizz a été lancé
        id_running_quizz = db(db.running_quizz.idrunning==1).select()
        next_button = P(A(SPAN(_class="icon fa fa-arrow-circle-right fa-lg"),_href=URL('zapette',args=[request.args[0],id_running_quizz[0].idquizz,id_running_quizz[0].idquestion]),_id='next_button'),_class='navbar-brand')     
        type_q = 'nothing'
        return locals()
 #  le quizz a été lancé , on récupère les infos
    liste_q = db(db.running_quizz.idrunning==1).select(db.running_quizz.liste_questions)
    liste_q = liste_q[0].liste_questions
    question_courante = int(request.args[2])
    position = liste_q.index(question_courante)
    nb_questions = len(liste_q)
   # question_courante = liste_questions[position]
    question_active = db(db.running_quizz.idrunning == 1).select(db.running_quizz.idquestion,db.running_quizz.liste_choix)
   # on s'assure que la question sur laquelle est l'etudiant correspond a la question courante
    if question_active[0].idquestion == question_courante:
        contenu = CAT(H2('Question '+str(position+1)),BR(),DIV(SPAN("  ",_id="record_ok"),_class="text-center",_style="height:20px;"),BR())
        liste_choix = question_active[0].liste_choix
        #si cette liste n'est pas vide on est sur une question multiple
        nb_choix = len(liste_choix)
        if nb_choix > 0:
        # la varaible type_q sert à modifier la vue
            type_q = 'choix'
            cpt = 0
            auxcontenu = ""
            while cpt < nb_choix:
                if ((cpt !=0) and ((cpt & 1)==0)):
                    auxcontenu = DIV(auxcontenu, _class='text-center')
                    contenu = CAT(contenu,auxcontenu)
                    auxcontenu=""
                auxcontenu = CAT(auxcontenu,DIV(A(SPAN(chr(ord('A')+cpt),_class="buttontext button"), _class="button btn btn-default btn-secondary btn-xl",_href="", data={'is_selected': 0},_id=liste_choix[cpt]),_class="btn-group btn-group-xl"))
                cpt = cpt + 1
            contenu = CAT(contenu,DIV(auxcontenu, _class='text-center'))              
        else:
            type_q = 'saisie'
            contenu = CAT(contenu,SPAN(XML('Votre r&eacute;ponse:'),_class='texte'),DIV(INPUT(_type='text',_class='saisie')))
        contenu = CAT(contenu,BR(),DIV(INPUT(_id="envoi",_type='button',_class ='button btn btn-default btn-primary',value='Envoyer'),_class='text-center'))    
        position = position + 1
    else:
        contenu = DIV(IMG(_src=URL("static", "images",args="patience.gif"),_width='95%'),P(B(XML("Patience ..., r&eacute;essayez dans quelques secondes"),_class="patience")),_class="text-center")
        type_q = 'nothing'
    if position < nb_questions:
        next_button = P(A(SPAN(_class="icon fa fa-arrow-circle-right fa-lg"),_href=URL('zapette',args=[request.args[0],request.args[1],liste_q[position]]),_id='next_button'),_class='navbar-brand') 
    else:
        # on est arrivé à la dernière question on envoie l'étudiant sur la page de ses résultats
        next_button = P(A(SPAN(_class="icon fa fa-arrow-circle-right fa-lg"),_href=URL('resultat_etudiant',args=[request.args[0]]),_id='next_button'),_class='navbar-brand')

    return locals()

def resultat_etudiant():
    # on regarde si l'enseignant a  affiché les résultats de la dernière question
    # si ce n'est pas le cas les données nécessaires à l'affichage des résultats individuels
    # ne sont pas disponible  
    resultats_ok = (db(db.running_quizz.idquizz==-1).count() == 1)
    if resultats_ok:    
        #    cpt_ok = 2
        #    cpt_ko= 10
        #    cpt_incomplet = 0
        #    cpt_nonrepondu = 1
        #    cpt = cpt_ok+cpt_ko+cpt_incomplet+cpt_nonrepondu
        cpt_ok = db((db.reponses_etudiants.idetudiant == request.args(0)) & (db.reponses_etudiants.correct == True)).count()
        cpt_incomplet = db((db.reponses_etudiants.idetudiant == request.args(0)) & (db.reponses_etudiants.incomplet == True)).count()
        cpt_nonrepondu = db((db.reponses_etudiants.idetudiant == request.args(0)) & (db.reponses_etudiants.nonrepondu == True)).count()   
        aux = cpt_ok + cpt_incomplet + cpt_nonrepondu
        cpt = db(db.reponses_etudiants.idetudiant == request.args(0)).count()
        cpt_ko = cpt - aux
        if cpt_ok != 0:
            p_ok = "{:.1%}".format(cpt_ok/cpt)
        else:
            p_ok = "0%"
        if cpt_ko != 0:
            p_ko = "{:.1%}".format(cpt_ko/cpt)
        else:
            p_ko = "0%"
        if cpt_incomplet != 0:
            p_incomplet = "{:.1%}".format(cpt_incomplet/cpt)
        else:
            p_incomplet = "0%"
        if cpt_nonrepondu != 0:
            p_nonrepondu = "{:.1%}".format(cpt_nonrepondu/cpt)
        else:
            p_nonrepondu = "0%"   
        resultat = cpt_ok/cpt 
        classeko=""
        mauvais_resultat = cpt_ko/cpt
        if resultat >= 0.5:
            classeok= "ok"
            if resultat >=0.75: 
                image = 'images/verygood.png'
            elif resultat >=0.6:
                image = 'images/good.png'
            else:
                image = 'images/middle.png'
        else:
            classeok = "ko"
            if mauvais_resultat >= 0.5:
                classeko = "ko"
            if resultat >= 0.3:
                image = 'images/bad.png'
            else:
                image = 'images/verybad.png'
    return locals()
