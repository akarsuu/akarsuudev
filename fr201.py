from flask import Flask, Blueprint, jsonify, render_template, request, session
import random
from flask_cors import CORS

fr201_bp = Blueprint('fr201', __name__)
CORS(fr201_bp)


question_list = [
    (1, "Tu veux bien répondre aux questions suivantes ?", "Oui, je veux bien y répondre."),
    (2, "Stéphanie a voulu changer ... vie.", "Stéphanie a voulu changer de vie."),
    (3, "Max a ... révé ... devenir guitariste.", "Max a toujours révé de devenir guitariste."),
    (4, "François aime cuisiner pour ses amis, il aime ... faire découvrir ... nouvelles saveurs.", "François aime cuisiner pour ses amis, il aime leur faire découvrir de nouvelles saveurs."),
    (5, "Elle connait très bien la Thailande, elle ... a fait découvrir les spécialités du ....", "Elle connait très bien la Thailande, elle lui a fait découvrir les spécialités du pays."),
    (6, "Réponds sans répéter le complément : Elle a consulté l'association ?", "Oui, elle l'a consultée."),
    (7, "L'association ... a conseillé ... suivre une formation par alternance. (Stéphanie)", "L'association lui a conseillé de suivre une formation par alternance."),
    (8, "L'association ... a bien conseillé. (Stéphanie)", "L'association l'a bien conseillée."),
    (9, "Elle a pu changer de vie grâce ... association", "Elle a pu changer de vie grâce à l'association."),
    (10, "Trouve la question - Elle se protège du froid.", "Elle se protège de quoi ?"),
    (11, "François a ... bonnes ... en informatique.", "François a de bonnes compétences en informatique."),
    (12, "Elle ... gagné un séjour à la campagne.", "Elle a gagné un séjour à la campagne."),
    (13, "Compléte et corrige si nécessaire : Elle ... tombé amoureuse de la vie à la campagne.", "Elle est tombée amoureuse de la vie à la campagne."),
    (14, "Elle ... connaissance ... un éleveur de mouton.", "Elle a fait la connaissance d'un éleveur de mouton."),
    (15, "Stéphanie a ... souvenirs de la campagne.", "Stéphanie a d'excellents souvenirs de la campagne."),
    (16, "Max apprendre jouer guitare tout seul", "Max a appris à jouer de la guitare tout seul."),
    (17, "Les chiffres bloquent Catty ? Reponds sans répéter le complément", "Oui, les chiffres la bloquent."),
    (18, "Elle veut ouvrir son salon de thé ? Réponds sans répéter", "Oui, elle veut l'ouvrir."),
    (19, "On a prévenu Fiorenzo quand son emploi de temps a changé ? Non, sans répéter", "Non, on ne l'a pas prévenu quand son emploi de temps a changé."),


    
]


"""

    (2, "J'ai beaucoup ... chance. ", "J'ai beaucoup de chance."),
    (3, "Elle est végétarienne, elle ne mange pas ... poisson.", "Elle est végétarienne, elle ne mange pas de poisson."),
    (4, "Au petit-déjeuner je prends ... tomates, ... oeuf et ... pain avec un peu ... fromage.", "Au petit-déjeuner je prends des tomates, un oeuf et du pain avec un peu de fromage."),
    (5, "Elle m'a fait gouter ... spécialités thailandaises.", "Elle m'a fait gouter les spécialités thailandaises."),
    (6, "En Turquie les repas sont composés ... entrée, ... plat principal et ... dessert.", "En Turquie les repas sont composés d'une entrée, d'un plat principal et d'un dessert."),
    (7, "Dans ce sandwich il y a ... champignons, ... thon, ... moutarde et un peu ... sel, il n'y a pas ... jambon.", "Dans ce sandwich il y a des champignons, du thon, de la moutarde et un peu de sel, il n'y a pas de jambon."),
    (8, "Je veux lui acheter ce sac mais je n'ai pas ... argent.", "Je veux lui acheter ce sac mais je n'ai pas d'argent."),
    (9, "Je veux lui acheter ce sac mais je n'ai pas assez ... argent.", "Je veux lui acheter ce sac mais je n'ai pas assez d'argent."),
    (10, "Je ne peux pas manger ce poisson, il y a trop ... sel !", "Je ne peux pas manger ce poisson, il y a trop de sel !"),
    (11, "Réponds sans répéter le complément : Tu te protèges le nez ? Oui, ...", "Oui, je me le protège."),
    (12, "Réponds sans répéter le complément : Tu t'es protégé du froid ? Oui, ...", "Oui, je m'en suis protégé."),
    (13, "Réponds à la négation sans répéter le complément : Vous vous êtes occupés des enfants ? Non, ...", "Non, nous ne nous en sommes pas occupés."),
    (14, "Réponds à la négation sans répéter le complément : Tu fais du tennis ? Non, ...", "Non, je n'en fais pas."),
    (15, "Fais une phrase au passé avec : grâce / initiatives / nouvelles / se calmer / politiques / inflation", "Grâce aux nouvelles initiatives politiques l'inflation s'est calmée."),
    (16, "Elle n'est pas assez de courage. Corrige la phrases", "Elle n'a pas assez de courage."),
    (17, "Elle n'a pas assez courageuse", "Elle n'est pas assez courageuse."),
    (18, "Fais une phrase au passé Jean Paul / s'inspirer / marinière", "Jean Paul s'est inspiré de la marinière."),
    (19, "Fais une phrase au passé Je mettre crème solaire protéger soleil", "Je me suis mis de la crème solaire pour me protéger du soleil."),
    (20, "Réponds négativement sans répéter le complément : Tu aimes les légumes ?", "Non, je n'aime pas ça."),
    (21, "Réponds affirmativement sans répéter le complément indirect : Elle est allée faire du shopping pour acheter une veste à son copain ?", "Oui, elle est allée faire du shopping pour lui acheter une veste."),
    (22, "Réponds négativement sans répéter le complément Tu as fait du shopping ?", "Non, je n'en ai pas fait."),
    (23, "Compléte les paroles de la chanson de Zaz : Je veux ... amour, ... joie et ... bonne humeur.", "Je veux de l'amour, de la joie et de la bonne humeur."),
    (24, "Tu as pris du poisson ? Réponds sans répéter le complément à la négation Non,", "Non, je n'en ai pas pris."),
    (25, "Compléte la question sans utiliser le verbe pouvoir : Pourquoi Emanuelle ... terminer les vétêments qu'elle commence à coudre ?", "Pourquoi Emanuelle n'arrive pas à terminer les vétêments qu'elle commence à coudre ?"),
    (26, "Compléte la question : Tu fais ... couture ?", "Tu fais de la couture ?"),
    (27, "Ne répéte pas le complément : Est-ce que les journalistes ont interviewé les étudiants de l'école ? Oui,", "Oui, ils les ont interviewés."),
    (28, "Constitue une question avec Qui / pouvoir / aider / Jean / pour / achats ?", "Qui peut aider Jean pour les achats ?"),
    (29, "Constitue une question avec Qui / pouvoir / demander / aide / Jean / pour / achats ?", "Qui peut demander de l'aide à Jean pour les achats ?"),
    (30, "Je ne peux pas bien dessiner parce que je n'ai pas ... geste précis.", "Je ne peux pas bien dessiner parce que je n'ai pas de geste précis."),
    (31, "Tu vas terminer les exercices ? Réponds à l'affirmative sans répéter le complément", "Oui, je vais les terminer."), 

    (2, "Fais une phrase au passé composé : s'inspirer / de / tradition / Arménie (adj.) / une / ils/", "Ils se sont inspirés d'une tradition arménienne."),
    (3, "Complète la phrase avec inventer : Un chimiste et un pharmacien …………", "Un chimiste et un pharmacien ont inventé le papier d'Arménie."),
    (4, "Complète la phrase (adjectif): Le papier ………… (naître) ………… un chimiste et un pharmacien.", "Le papier arménien est né grâce à un chimiste et un pharmacien."),
    (5, "Je fais des économies ………… ce type de cohabitation : Mets cette phrase au passé composé et complète la.", "J'ai fait des économies grâce à ce type de cohabitation."),
    (6, "Réponds sans répéter le complément à la négation : Elle a pris ses lunettes de soleil violettes ? Non,...", "Non, elle ne les a pas prises."),
    (7, "Réponds à la négation sans répéter le complément : Tu veux de la crème solaire ? Non, ...", "Non, je n'en veux pas."),
    (8, "Réponds au futur et à la négation sans répéter le complément « Lucie » : Elle demande à Lucie d'acheter le sac bleu. Non,...", "Non, elle ne va pas lui demander d'acheter le sac bleu."),
    (9, "Lucie peut s'occuper des achats ? Réponds sans répéter le complément. Non, ...", "Non, elle ne peut pas s'en occuper."),
    (10, "Le savon de Marseille est le ………… savon d'Alep.", "Le savon de Marseille est le petit frère du savon d'Alep."),
    (11, "Le savon de Marseille est ………… principalement ………….", "Le savon de Marseille est composé principalement d'huile d'olive."),
    (12, "Réponds au passé et à la négation : Tu me demandes un service ? Non, ...", "Non, je ne t'ai pas demandé de service."),
    (13, "Corrige la phrase : Nous avons tous ensemble sorti le soir pour aller manger.", "Nous sommes tous ensemble sortis le soir pour aller manger."),
    (14, "Réponds sans répéter le complément : Vous venez de Marseille ? Oui, ...", "Oui, nous en venons."),
    (15, "Corrige la phrase : Elle est mise sa jupe et son pull noir.", "Elle a mis sa jupe et son pull noir."),
    (16, "Le chocolat noir est ………… pour la santé que le chocolat blanc.", "Le chocolat noir est meilleur pour la santé que le chocolat blanc."),
    (17, "Fais une phrase : soldes / permettre / avoir / clients / prix / (le contraire d'élevés).", "Les soldes permettent aux clients d'avoir des prix réduits."),
    (18, "Fais une phrase : Grâce / soldes / commerçants / vendre / (+ bien)", "Grâce aux soldes les commerçants vendent mieux."),
    (19, "Sidonie n'a pas …………. faire les achats elle a donc demandé ………… Elise de ………… faire.", "Sidonie n'a pas le temps de faire les achats elle a donc demandé à Elise de les faire."),
    (20, "Réponds à la négation sans répéter le complément : Tu vas prendre des vacances ? Non, ...", "Non, je ne vais pas en prendre."),
    (21, "Améliore le registre : Il y a des jolies fleurs dans ce magasin.", "Il y a de jolies fleurs dans ce magasin."),
    (22, "Mets cette question au passé : Qu'est-ce que Maxime sent au magasin ?", "Qu'est-ce que Maxime a senti au magasin ?"),
    (23, "Fais une phrase vendeur / proposer / lui / moins / pour / article / cher / sac / sacs / que / Maxime / payer / parce que / ne pas vouloir / 200 euros /", "Le vendeur lui a proposé un article moins cher que les sacs parce que Maxime n'a pas voulu payer 200 euros pour un sac."),
    (24, "La marinière est aujourd'hui indissociable …………. grand couturier Jean Paul Gaultier.", "La marinière est aujourd'hui indissociable du grand couturier Jean Paul Gaultier."),
    (25, "Réponds sans répéter le complément à la négation : Tu apportes ton short jaune ? Non, ...", "Non, je ne l'apporte pas."),
    (26, "Transforme la question au passé sans répéter le complément : Elle va mettre sa robe noire ?", "Elle l'a mise ?"),
    (27, "Transforme la phrase au passé : Maxime (vouloir faire) un cadeau à sa copine alors il (aller) dans un magasin et (choisir) un portefeuille.", "Maxime a voulu faire un cadeau à sa copine alors il est allé dans un magasin et a choisi un portefeuille."),
    (28, "Réponds sans répéter le complement et le sujet : Est-ce que le magasin accepte les cartes bleues.", "Oui, il les accepte."),
    (29, "Réponds sans répéter le complément : Tu connais Maxime ?Oui, ...", "Oui, je le connais."),
    (30, "Réponds sans répéter le complément : Ils sont allés à l'école ?, Oui, ...", "Oui, ils y sont allés."),
    
    (2, "Réponds à la négation sans répéter le complément : Tu as ton bonnet ?", "Non, je ne l'ai pas."),
    (3, "Réponds à la négation sans répéter le complément : Tu as un bonnet ?", "Non, je n'en ai pas."),
    (4, "Réponds à la négation sans répéter le complément : Tu as répondu aux questions ?", "Non, je n'y ai pas répondu."),
    (5, "Réponds à la négation sans répéter le complément : Vous vous êtes inspirés d'une tradition thailandaise ?", "Non, nous ne nous en sommes pas inspirés."),
    (6, "Le sandwich est ...", "Le sandwich est composé de pain, de carottes et de mayonnaise."),
    (7, "Corrige la phrase : Maxime n'est pas pris le sac parce que il n'est pas voulu payer 200 euros.", "Maxime n'a pas pris le sac parce qu'il n'a pas voulu payer 200 euros."),
    (8, "Mets la phrase à l'impératif : Tu réponds et passes à la question suivante.", "Réponds et passe à la question suivante."),
    (9, "Fais une phrase à l'impératif, fais parler le vendeur : Le vendeur demande au client de le suivre et il lui fait sentir un parfum. ... , ...", "Suivez-moi, sentez ce parfum."),
    (10, "Fais un phrase au passé : Benjamin retirer appartement tous protuits étranger.", "Benjamin a retiré tous les produits fabriqués à l'étranger de son appartement."),
    (11, "Tu portes un bonnet pour te protéger quoi ?", "Je porte un bonnet pour me protéger la tête."),
    (12, "Pour te protéger quoi tu portes une veste ?", "Je porte une veste pour me protéger le corps."),
    (13, "On va à la plage s'il ...", "On va à la plage s'il fait beau."),
    (14, "Corrige : Elle porte une rouge robe petite.", "Elle porte une petite robe rouge."),
    (15, "Ella a des yeux bleu clair. Corrige", "Elle a des yeux bleus clairs."),
    (16, "Je veux de café. Corrige", "Je veux du café."),
    (17, "Ce matin je suis mangé une barre du chocolat. Corrige", "Ce matin j'ai mangé une barre de chocolat."),
    (18, "Corrige Ces sacs ne sont pas oranges ils sont rouges.", "Ces sacs ne sont pas orange ils sont rouges."),
    (19, "Tu as préparé ta valise ? Réponds sans répéter le complément. Oui,", "Oui, je l'ai préparée."),
    (20, "Corrige Quand nous avons entré dans le magasin le vendeuse a venu pour nous aider.", "Quand nous sommes entrés dans le magasin le vendeur est venu pour nous aider."),
    (21, "Réponds à la négation Tu peut aider ta petite soeur ?", "Non, je ne peux pas l'aider."),
    (22, "Fais une phrase Grâce soldes commerçants vendre +bien.", "Grâce aux soldes les commerçants vendent mieux."),
    (23, "S'il ... pas beau on ne va pas à la plage.", "S'il ne fait pas beau on ne va pas à la plage."),
    (24, "Fais une phrase ne pas faire tennis parce que je détéster tennis.", "Je ne fais pas du tennis parce que je détéste le tennis."),
    (25, "(nez, froid) Je porte une écharpe pour ... protéger ...... parce que je vais ... ... montagne et il ... fait froid.", "Je porte une écharpe pour me protéger le nez du froid parce que je vais à la montagne et il y fait froid."),
    (26, "Le coach me conseille ... ma pérformance.", "Le coach me conseille d'améliorer ma pérformance."), 
    (27, "Ce fromage sent ... .", "Ce fromage sent bon."),
    (28, "Je ne peux pas réviser parce que j'ai ... ... ... ... concentrer.", "Je ne peux pas réviser parce que j'ai du mal à me concentrer."),
    (29, "Dans le Banh mi il y a ... carottes, ... mayonnaise et un peu ... fromage.", "Dans le Banh mi il y a des carottes, de la mayonnaise et un peu de fromage."),
    (30, "Le client a acheté deux tablettes ... chocolat, un paquet .. riz, un pot ... confiture et 250 grammes ... olives.", "Le client a acheté deux tablettes de chocolat, un paquet de riz, un pot de confiture et 250 grammes d'olives."),
    (31, "Benjamin a enlevé sa télé d'où ? Réponds sans répéter le complément Il... ", "Il l'a enlevée de son appartement."), 
   """


intro_question = question_list[0][1]
wrong_answer = ""
wrong_answer_number = 0
final_grade = 0

def initialize_session():
    
    session['question_list'] = question_list.copy()
    session['wrong_answer'] = ""
    session['wrong_answer_number'] = 0
    

@fr201_bp.route('/function201', methods=['GET', 'POST'])
def function202():
    
    data = request.get_json()
    submitted_answer = data.get('answer')

    if 'question_list' not in session:
        initialize_session()

        if submitted_answer == session['question_list'][0][2]:
            session['question_list'].pop(0)
            if len(session['question_list']) == 0:
                final_wrong_answer_number = session.get('wrong_answer_number', 0)
                session.clear()
                return jsonify({
                    'completed': True,
                    'wrong_answer_number': final_wrong_answer_number
                
                })
            else:
                current_question = session['question_list'][0]
                session.pop('wrong_answer', None)  # Clear wrong answers for new question
                return jsonify({
                    'question': current_question[1],
                    'wrong_answer': '',
                })
        else:
            session['wrong_answer'] = submitted_answer
            session['wrong_answer_number'] += 1  # Increment wrong answer count in session
            print(session['wrong_answer_number'])
            return jsonify({
                'question': session['question_list'][0][1],  # Display the introductory question again
                'wrong_answer': session['wrong_answer'],
                'wrong_answer_number': session['wrong_answer_number'],
            })
    elif 'question_list' in session and len(session['question_list']) > 0:
        if submitted_answer == session['question_list'][0][2] or submitted_answer == "passer":
            session['question_list'].pop(0)
            if len(session['question_list']) == 0:
                final_wrong_answer_number = session.get('wrong_answer_number', 0)
                final_grade = 100 - session.get('wrong_answer_number', 0)
                session.clear()
                return jsonify({
                    'completed': True,
                    'wrong_answer_number': final_wrong_answer_number,
                    'final_grade': final_grade,
                     })
            else:
                random.shuffle(session['question_list'])
                current_question = session['question_list'][0]  # Update current question after shuffling
                session.pop('wrong_answer', None)  # Clear wrong answers for new question
                return jsonify({
                    'question': current_question[1],
                    'wrong_answer': '',
                    'wrong_answer_number': session['wrong_answer_number'],
                })
        else:
            current_question = session['question_list'][0]
            # Store the wrong answer for the current question
            session['wrong_answer_number'] += 1
            print(session['wrong_answer_number'])
            if 'wrong_answer' not in session:
                session['wrong_answer'] = submitted_answer
            else:
                session['wrong_answer'] += ' ' + '/ ' + submitted_answer
            return jsonify({
                'question': current_question[1],
                'wrong_answer': session['wrong_answer'],
                'wrong_answer_number': session['wrong_answer_number'],
            })
    else:
        print("LAST ELSE BLOCK")
        print("End of quiz session is cleared")
        final_wrong_answer_number = session.get('wrong_answer_number', 0)
        final_grade = 100 - session.get('wrong_answer_number', 0)
        print(final_grade, "is the final grade")
        session.clear()
        return jsonify({'error': 'No question available', 'wrong_answer_number': final_wrong_answer_number, 'final_grade': final_grade})