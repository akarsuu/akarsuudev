from flask import Flask, Blueprint, jsonify, render_template, request, session
import random
from flask_cors import CORS

fr202_bp = Blueprint('fr202', __name__)
CORS(fr202_bp)


question_list = [
    (1, "Tu veux bien répondre aux questions suivantes ?", "Oui, je veux bien y répondre."),
    (2, "peur de / mourir / il / ne pas sauter / avion Fais une phrase au futur", "De peur de mourir il ne sautera pas de l'avion."),
    (3, "cercle / se former / et / Joseph / être / centre / cercle Fais une phrase au passé sans répéter 'cercle'", "Un cercle s'est formé et Joseph en a été le centre."),
    (4, "Compléte : Je ... la colère venir, doublée ... rage ... ne pas comprendre.", "Je sens la colère venir, doublée de la rage de ne pas comprendre."),
    (5, "Traduis : 70 years ago Jewish children could only go to school with a yellow star on their jacket.", "Il y a 70 ans les enfants juifs ne pouvaient aller à l'école qu'avec une étoile jaune sur leurs vestes."),
    (6, "Décathlon a aujourd'hui 20 marques. Remplace le verbe avoir par un autre verbe", "Décathlon possède aujourd'hui 20 marques."),
    (7, "Quand l'avion a attérri et s'est aussitôt décollé la jeune fille a eu ... coeur et ... sur les genoux de son voisin.", "Quand l'avion a attérri et s'est aussitôt décollé la jeune fille a eu mal au coeur et a vomi sur les genoux de son voisin."),
    (8, "Le succès de Décathlon ... par le grand choix de produits qu'il propose aux clients en libre-service.", "Le succès de Décathlon s'explique par le grand choix de produits qu'il propose aux clients en libre-service."),
    (9, "Constitue une prase au conditionnel au futur : si / entreprise / continuer / d'innover / elle / progresser / encore plus", "Si l'entreprise continue d'innover elle progressera encore plus."),
    (10, "Traduis : she did not take a shower, she smells bad.", "Elle n'a pas pris de douche, elle sent mauvais."),
    (11, "Traduis : Do not stare at your screen for a long time, take breaks to rest your eyes.", "Ne fixez pas votre écran longtemps, faites des pauses pour reposer vos yeux."),
    (12, "C'est un ... (synonyme pour travail et job) ... se mérite, ... qui ne peut pas l'... (synonyme avoir).", "C'est un poste qui se mérite, n'importe qui ne peut pas l'obtenir."),

]
"""
    (2, "Réponds sans répéter le complément et en utilisant le futur simple : L'association va pouvoir bien conseiller Stéphanie ? Oui, ...", "Oui, l'association pourra bien la conseiller."),
    (3, "Nishi avait il peur des femmes ? Réponds sans répéter le complément. Non, ...", "Non, il n'en avait pas peur."),
    (4, "Mets la question au passé en utilisant un autre temps : Est-ce qu'elle a vu la campagne avant de s'y installer ?", "Est-ce qu'elle avait vu la campagne avant de s'y installer ?"),
    (5, "Est-ce que Nishi avait peur de faire des gaffes quand il parlait aux français ? Réponds sans répéter les compléments. Oui, ...", "Oui, il avait peur d'en faire quand il leur parlait."),
    (6, "Réponds négativement. La comprend-t-elle quand elle lui raconte des salades ? Non, ...", "Non, elle ne la comprend pas quand elle lui raconte des salades."),
    (7, "Trouve la question; Il s'agit d'un pays : -Oui, elle l'a abolie en 1981.", "Est-ce que la France a aboli la peine de mort en 1981 ?"),
    (8, "Tu allais souvent chez tes grands-parents quand tu était petit(e) ? Réponds négativement et sans répéter le compément. Non, ...", "Non, je n'y allais pas souvent."),
    (9, "Marc, que n'a-t-il par remarqué appercevant Alice ? Réponds en utilisant (faire déborder la coupe d'Anne)", "Il n'a pas remarqué qu'il avait fait déborder la coupe d'Anne."),
    (10, "Qu'avait-il fait Armstrong pendant des années ?", "Il s'était dopé."),
    (25, "Réponds sans répéter les compléments. Que se passera lorsqu'on apprendra qu'Armstrong avait triché et qu'il ne méritait pas ses titres ? On ...", "On les lui retirera."),
    (12, "Que faisait Marc appercevant Alice ? (servir une coupe de champagne à Anne)", "Il servait une coupe de champagne à Anne."),
    (13, "Que fait notre visage quand nous avons honte ? Il ...", "Il rougit."),
    (14, "Fais une phrase négative avec nous / se rendre compte / déjà / coupe / être pleine avec un imparfait et un plus que parfait", "Nous ne nous étions pas rendus compte que la coupe était déjà pleine."),
    
    (16, "Jusqu'à la suppression des frontières européénnes + faites une phrase avec les éléments suivant : négation, elle, 4, de, de, en, en, moins, heures, pouvoir, jamais, aller, (destionation)Portugal, (provenance)Espagne", "Jusqu'à la suppression des frontières européénnes elle n'avait jamais pu aller de l'Espagne au Portugal en moins de 4 heures."),
    (17, "Complétez : Elle ......... heureuse de travailler à New York mais quand elle ................ son accident elle ............. rentrée en France.", "Elle était heureuse de travailler à New York mais quand elle a eu son accident elle est rentrée en France."),
    (18, "Complétez avec changer beaucoup / consommer : La révolution industrielle ......... les habitudes alimentaires des français, avant ils ......... de plats préparés.", "La révolution industrielle a beaucoup changé les habitudes alimentaires des français, avant ils ne consommaient pas de plats préparés."),
    (19, "Fais une phrase :  complément x 2 / chanteuse / téléphoner / pour / ils / annoncer / avoir / bébé", "La chanteuse lui a téléphoné pour lui annoncer qu'ils avaient eu un bébé."),
    (20, "Répondez sans répéter le complément: Avait-il apperçu Alice ? Non, ...", "Non, il ne l'avait pas apperçue."),
    (21, "Rougit on de peur ? Non, on ...", "Non, on rougit de honte."),
    (22, "Est-ce que Brigitte Bardot a trompé son mari ? Répondez sans répéter le complément. Non, ", "Non, elle ne l'a pas trompé."),
    (23, "Nous voyons s'il reste toujours des places quand nous arrivons au guichet. Mettez cette phrase au futur simple", "Nous verrons s'il reste toujours des places quand nous arriverons au guichet."),
    (24, "Pourquoi François-Xavier a eu des enfants ? Répondez sans répéter le complément. (avoir envie) Il ...", "Il en a eu parce qu'il avait eu envie de jouer au papa et à la maman."),
    
    (2, "Dis la même chose différemment. Il a voulu la draguer.", "Il a voulu la séduire."),
    (3, "Ilario a obtenu le … job … monde.", "Ilario a obtenu le meilleur job du monde."),
    (4, "Un soir ... elle en a eu … de la monotonie de sa vie elle a décidé de retrouver le numéro ... son petit ami de fac et de … téléhoner.", "Un soir où elle en a eu marre de la monotonie de sa vie elle a décidé de retrouver le numéro de son petit ami de fac et de lui téléphoner."),
    (5, "Il voulait ... son fils ... avec son grand-père.", "Il voulait voir son fils grandir avec son grand-père."),
    (6, "Contexte : la chanteuse allemande et Delon; Elle (téléphoner) plusieurs fois mais il (ne jamais répondre).", "Elle lui a téléphoné plusieurs fois mais il ne lui a jamais répondu."),
    (7, "Fais une phrase au passé composé et fait les changements nécessaires : Comme / il avoir la honte de sa vie / ne pas pouvoir sauter avion", "Comme il n'a pas pu sauter de l'avion il a eu la honte de sa vie."),
    (8, "Il lui a proposé un ... parachute parce qu'il voulait l'impressionner.", "Il lui a proposé un saut en parachute parce qu'il voulait l'impressionner."),
    (9, "Réponds à la négation sans répéter le complément: Il a impressionné sa copine ?", "Non, il ne l'a pas impressionnée."),
    (10, "Traduisez : Before the Industrial Revolution, almost no children went to school.", "Avant la révolution industrielle, presqu'aucun enfant n'allait à l'école."),
    (11, "Traduisez : He hadn't realized that what he was holding wasn't the bus's bar, but a passenger's.", "Il ne s'était pas rendu compte que ce qu'il tenait n'était pas la barre du bus, mais celle d'une passagère."),
    (12, "Avant la révolution industrielle les français ne consommaient pas de plats préparés, ils étaient donc en … santé comparé à aujourd'hui mais l'espérance de vie ... ... courte.", "Avant la révolution industrielle les français ne consommaient pas de plats préparés, ils étaient donc en meilleure santé comparé à aujourd'hui mais l'espérance de vie était plus courte."),
    (13, "Tu ne te souviens pas de la plage ou nous allions en été ? Refusez la proposition sans répéter le complément", "Si, je m'en souviens."),
    (14, "Corrige si nécessaire et fais une phrase au passé : ils s'approcher moi pour moi demander une addresse.", "Ils se sont approchés de moi pour me demander une addresse."),
    (15, "La femme … avait vécu dans une cité container pendant ses études avant … s'installer à la campagne, ... nous connaissons, … a vu la campagne et ... ... est tombée amoureuse s'appelle Stéphanie.", "La femme qui avait vécu dans une cité container pendant ses études avant de s'installer à la campagne, que nous connaissons, qui a vu la campagne et qui en est tombée amoureuse s'appelle Stéphanie."),
    (16, "Il a quitté son poste parce que c'était un travail qui ... convenait pas.", "Il a quitté son poste parce que c'était un travail qui ne lui convenait pas."),
    (17, "Il a quitté son job parce que c'était un travail qui ... plaisait pas.", "Il a quitté son job parce que c'était un travail qui ne lui plaisait pas."),
    (18, "Il a quitté son travail parce que c'était un travail ... n'était pas adaptée ses compétences.", "Il a quitté son travail parce que c'était un travail qui n'était pas adapté à ses compétences."),
    (19, "Elle est la meilleure dans ce qu'elle fait, elle ... son salaire.", "Elle est la meilleure dans ce qu'elle fait, elle mérite son salaire."),
    (20, "Réponds sans répéter le complément : Vous vous intéressiez à la politique quand vous étiez jeune ?", "Non, je ne m'y intéressais pas."),
    (21, "The emotion was so strong that he didn't realize the cup was already full.", "L'émotion était tellement forte qu'il ne s'est pas rendu compte que la coupe était déjà pleine."),
    (22, "I was so tired that I didn't realize that what I was holding was a curtain bar.", "J'étais si fatigué que je ne me suis pas rendu compte que ce que je tenais était une barre à rideaux."),
    (23, "Les enfants ... vous voyez ... se battent dans la ... de récréation sont ceux de Cécile.", "Les enfants que vous voyez qui se battent dans la cours de récréation sont ceux de Cécile."),
    (24, "Alice est fière ... ... car ... ce certificat n'était pas évident. En effet, c'est un certificat ... ... mérite.", "Alice est fière d'elle car obtenir ce certificat n'était pas évident. En effet, c'est un certificat qui se mérite."),
    (25, "... ... il a eu la honte de sa vie ne pouvant pas sauter, son premier rendez-vous avec Elodie a été un succès car ce geste ... a beaucoup plu, maintenant ils sont ensembles.", "Même s'il a eu la honte de sa vie ne pouvant pas sauter, son premier rendez-vous avec Elodie a été un succès car ce geste lui a beaucoup plu, maintenant ils sont ensembles."),
    (26, "Traduisez : 120 years ago, women could not vote in nearly any country", "Il y a 120 ans, les femmes ne pouvaient voter dans presqu'aucun pays."),
    (27, "Que se passera lorsqu'on apprendra qu'Armstrong avait triché et par conséquent il ne méritait pas ses titres ?", "On les lui retirera."),
    (28, "Est-ce que Bellegueule était le prénom d'Edouard ? Non, c'était le surnom que / personnes / certain / village / donner", "Non, c'était le surnom que certaines personnes du village lui avaient donné."),
    (29, "Corrige Stéphanie c'est quelqu'un d'intelligente.", "Stéphanie c'est quelqu'un d'intelligent."),

    
    (2, "Fais une phrase au passé composé avec : / partir / addresser / la / la / lui / de / de / peur / voir / il / ne / parole > Il ...", "Il ne lui a pas addressé la parole de peur de la voir partir."),
    (3, "Fais une phrase et ajoute les éléments manquants si nécessaire Mon...: pratique / permettre / rester / mon / frère / natation / qui / santé / bonne", "Mon frère pratique la natation qui lui permet de rester en bonne santé."),
    (4, "Fais une phrase au passé composé et ajoute les éLéMents manquants si nécessaire : je / impressionnant / visiter / utiliser / football / stade / locale / à domicile / équipe / pendant / matchs", "J'ai visité un stade de football impressionnant que l'équipe locale utilise pendant les matchs à domicile."),
    (5, "Corrige la phrase (pas de subjonctif): Je ne veux pas mes enfants grandir dans un pays que les droits démocratiques ne sont pas respecté.", "Je ne veux pas voir mes enfants grandir dans un pays où les droits démocratiques ne sont pas respectés."),
    (6, "Traduis : In almost no physical activity you can train your back as much as in rowing. Dans ... (vous)", "Dans presqu'aucune activité physique vous ne pouvez autant travailler votre dos que dans l'aviron."),
    (7, "Complète : Il y a 120 ans ... pays.", "Il y a 120 ans les femmes ne pouvaient voter dans presqu'aucun pays."),
    (8, "Fais une phrase au passé avec Decathlon / se développer énormément / permettre / innovant / choisir / son / grâce / produits / concept / qui / clients / les / libre-service", "Decathlon s'est énormément développé grâce à son concept innovant qui permettait aux clients de choisir les produits en libre-service."),
    (9, "Mets la phrase au passé : Nous ne pas savoir la marche faire travailler les muscles des jambes.", "Nous ne savions pas que la marche faisait travailler les muscles des jambes."),
    (10, "Fais une phrase au passé composé : Le / jour / aller / premier / école / jaune / son / étoile / Edouard agresser / se faire / ", "Le premier jour où Edouard est allé à l'école avec son étoile jaune il s'est fait aggressé."),
    (11, "Avant de changer de carrière Xavier ... longuement ... question.", "Avant de changer de carrière Xavier s'est longuement mis en question."),
    (12, "Je ne (savoir) pas la marche (muscler) les jambes.", "Je ne savais pas que la marche musclait les jambes."),
    (13, "Elle se ... souvent de douleurs musculaires mais ... qu'elle ... du sport régulièrement elle se ... beaucoup mieux.", "Elle se plaint souvent de douleurs musculaires mais depuis qu'elle fait régulièrement du sport elle se sent beaucoup mieux."),
    (14, "Réponds à la négation sans répéter le complément : Tu avait déjà fait de la natation ? Non,", "Non, je n'en avais jamais fait."),
"""

intro_question = question_list[0][1]
wrong_answer = ""
wrong_answer_number = 0
final_grade = 0

def initialize_session():
    
    session['question_list'] = question_list.copy()
    session['wrong_answer'] = ""
    session['wrong_answer_number'] = 0

@fr202_bp.route('/function202', methods=['GET', 'POST'])
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
        print("End of quiz session is cleared")
        final_wrong_answer_number = session.get('wrong_answer_number', 0)
        final_grade = 100 - session.get('wrong_answer_number', 0)
        session.clear()
        return jsonify({'error': 'No question available', 'wrong_answer_number': final_wrong_answer_number, 'final_grade': final_grade})
