from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analyses/m3/analyse_impact_souris_cas_G.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
for name,file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyFR',fontName='Arial',fontSize=10.5,leading=14,spaceAfter=7,textColor=colors.HexColor('#243442')))
styles.add(ParagraphStyle(name='TitleFR',fontName='Arial-Bold',fontSize=22,leading=26,spaceAfter=13,textColor=colors.HexColor('#173F5F')))
styles.add(ParagraphStyle(name='HFR',fontName='Arial-Bold',fontSize=13,leading=17,spaceBefore=9,spaceAfter=7,textColor=colors.HexColor('#173F5F')))
styles.add(ParagraphStyle(name='SmallFR',fontName='Arial',fontSize=9,leading=12,spaceAfter=5,textColor=colors.HexColor('#384B5A')))
styles.add(ParagraphStyle(name='CellFR',fontName='Arial',fontSize=9.4,leading=12))
story=[]
def p(text,style='BodyFR'): story.append(Paragraph(text,styles[style]))
def h(text): p(text,'HFR')
def page(title):
    if story:story.append(PageBreak())
    p(title,'TitleFR')
def table(headers,rows,widths):
    values=[[Paragraph('<b>'+escape(v)+'</b>',styles['CellFR']) for v in headers]]
    values += [[Paragraph(escape(str(v)),styles['CellFR']) for v in row] for row in rows]
    t=Table(values,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DFEAF1')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),1,colors.HexColor('#173F5F')),('LINEBELOW',(0,1),(-1,-1),.4,colors.HexColor('#CCD7DF'))]))
    story.append(t);story.append(Spacer(1,8))
def risk(title,scenario,impact,assessment,measures,test):
    h(title)
    p('<b>Scénario et faiblesse.</b> '+scenario)
    p('<b>Impact pour la personne.</b> '+impact)
    p('<b>Estimation initiale.</b> '+assessment)
    p('<b>Mesures proposées.</b> '+measures)
    p('<b>Vérification attendue.</b> '+test)

page('Analyse d’impact sur la protection des données')
p('<b>Cas G - Souris ergonomique connectée</b><br/>Équipe 2 | Version préparatoire réalignée le 19 octobre 2026')
p('Périmètre retenu : données conservées sur l’ordinateur de la personne qui utilise la souris. Historique disponible pendant le suivi, avec suppression à tout moment.')
h('La question adaptée à notre projet')
p('La souris collecte des signaux physiologiques et des mouvements pendant son utilisation. Leur rapprochement avec les horaires et les sessions peut révéler des habitudes ou des informations de santé. Qui peut lire les fichiers sur le PC ? Quelles mesures sont réellement nécessaires au suivi ? Comment l’utilisateur consulte-t-il, exporte-t-il et supprime-t-il son historique ?')
h('Traitement et personnes concernées')
p('Le prototype R3 acquiert et affiche des mesures expérimentales. La finalité future est le repérage des risques de complications cardiovasculaires liés au stress et à la sédentarité, chez un adulte utilisant un ordinateur. Population, événements et décisions restent à définir. Le logiciel actuel ne fournit pas de recommandation médicale validée ni de décision thérapeutique automatique. [P1]')
table(['Données présentes dans R3','Utilité et limites'],[
('Pouls calculé, SpO2 expérimentale, signaux optiques IR/rouge, qualité PPG','Mesures au contact de la main. Leur valeur pour évaluer un risque cardiovasculaire reste à démontrer.'),
('GSR, accélérations de la souris, température de contact','Pas de diagnostic de stress, immobilité non équivalente à sédentarité, pas de température centrale.'),
('Horodatages, session et connexion, états et erreurs techniques','Relier les mesures et diagnostiquer une acquisition. Les identifiants de session ne rendent pas les données anonymes.')],[205,300])
h('Circulation des données')
p('Capteurs de la souris → liaison Bluetooth LE → passerelle sur le PC → fichier CSV local → tableau de bord local. Le code comporte une option MQTT vers 127.0.0.1:1883. Aucun serveur distant n’est retenu dans le périmètre. Les sauvegardes du PC et l’exposition réseau du tableau de bord restent à vérifier. [P1]')
p('L’analyse de risques du dispositif (tableau n° 1 à 22) traite les défaillances, erreurs et dommages. Cette analyse d’impact examine aussi la nécessité de la collecte, les droits et les effets sur la vie privée. Une même faiblesse peut contribuer aux deux analyses.','SmallFR')

page('Nécessité, accès et conservation')
h('Minimiser la collecte')
p('Pour chaque capteur, préciser l’indicateur recherché et la décision de suivi qu’il permet. Si aucune utilité n’est démontrée, désactiver la collecte correspondante ou la limiter aux essais techniques. Une souris utilisable sans enregistrement doit rester possible. Ne pas déduire un état de santé, un stress ou une productivité à partir d’un signal non validé.')
p('Ne demander ni nom, ni adresse, ni identité de patient pour le simple affichage local. Séparer les utilisateurs et les sessions. L’absence de nom dans un CSV ne garantit pas l’anonymat : le PC, les horaires et le contexte peuvent identifier la personne. Les mesures physiologiques peuvent relever des données de santé selon leur nature, leur croisement et leur finalité. [P1, P2]')
h('Règle de conservation retenue')
p('<b>L’historique de suivi reste sur le PC pendant la durée du suivi. L’utilisateur peut supprimer une période ou l’ensemble des données à tout moment. À la fin du suivi, prévoir la suppression après possibilité d’export.</b> Une désinstallation doit proposer explicitement de conserver ou de supprimer les données locales.')
p('Ce choix s’inspire du fonctionnement de Santé d’Apple et de Fitbit/Google Health : l’historique peut durer plusieurs années et sa suppression est contrôlée par l’utilisateur. Il ne s’agit pas d’une durée légale commune aux objets connectés. Pour le projet, la conservation doit rester justifiée par la finalité du suivi. [P3-P5]')
table(['Catégorie','Règle à mettre en place'],[
('Historique utile au suivi','Durée du suivi, suppression possible à tout moment et prévue à sa clôture. Ne pas conserver par défaut des données sans utilité pour cet historique.'),
('Signaux bruts et diagnostics','Définir une durée technique distincte et courte avant les essais. Cette durée doit répondre au besoin de validation ; elle ne limite pas l’historique de suivi.'),
('Exports et sauvegardes','Identifier les copies. Informer que supprimer l’historique principal ne supprime pas un export réalisé ailleurs. Prévoir la purge des sauvegardes gérées par le projet.')],[155,350])
p('<b>Écart actuel :</b> la passerelle ajoute les enregistrements au CSV. Le code examiné ne fournit ni purge par ancienneté, ni interface de suppression de l’historique, ni clôture du suivi. Les règles ci-dessus sont des exigences à développer et tester. [P1]')
h('Accès, information et droits')
p('Accès prévu : utilisateur du PC. Aucun accès automatique de l’équipe, d’un employeur ou d’un professionnel. Un éventuel partage médical doit être choisi et limité par l’utilisateur. Prévoir une notice indiquant les données, les finalités, les destinataires, la conservation et le moyen d’exercer ses droits. Permettre consultation, export et suppression ; signaler une mesure incorrecte sans falsifier la mesure d’origine. [P6]')

page('Risques pour les droits et libertés')
p('Estimations qualitatives préparatoires : « importante » signifie une atteinte pouvant avoir des conséquences personnelles ou professionnelles durables ; « modérée », une gêne réversible dans le suivi. « Possible » décrit un scénario plausible sans fréquence mesurée. Aucune cotation résiduelle n’est validée avant les essais. Ce repérage ne reprend pas la matrice de sécurité du TP.','SmallFR')
risk('A1. Lecture non autorisée du fichier local',
     'Un proche, un autre compte du PC, un administrateur ou un logiciel malveillant lit le CSV. Les droits du dossier, le chiffrement du disque et les sauvegardes n’ont pas été vérifiés. [P1]',
     'Divulgation d’habitudes et d’informations de santé, gêne, détresse ou utilisation défavorable de ces informations.',
     'Gravité importante ; vraisemblance possible, dépendante de la configuration du PC.',
     'Dossier privé au compte utilisateur, verrouillage de session, chiffrement du disque, protection des sauvegardes, limitation des exports. Aucun fichier de mesures réelles dans Git.',
     'Essayer l’accès depuis un autre compte standard ; vérifier les permissions, le chiffrement et les destinations de sauvegarde. Lien : risque 9 du TP.')
risk('A2. Transmission ou service local exposé',
     'Une configuration Bluetooth insuffisante ou un tableau de bord/broker exposé sur le réseau permet à un tiers de consulter les mesures. La sélection BLE par nom ne démontre pas l’authentification. L’option MQTT vise actuellement localhost ; son existence ne prouve pas une fuite distante. [P1]',
     'Interception de données intimes et surveillance à l’insu de la personne.',
     'Gravité importante ; vraisemblance possible, protections réelles à tester.',
     'Vérifier appairage et chiffrement BLE. Limiter le tableau de bord et le broker à l’interface locale. Désactiver MQTT si inutile. Réévaluer toute ouverture distante.',
     'Contrôler les interfaces d’écoute et tester depuis une autre machine ; vérifier qu’un client BLE non autorisé ne peut lire les mesures. Lien : risque 9.')
risk('A3. Données attribuées à la mauvaise personne',
     'Plusieurs acquisitions s’ajoutent au même CSV ; les courbes ne filtrent pas les sessions. Une personne voit ou exploite l’historique d’une autre. Une usurpation d’objet constitue aussi un scénario distinct. [P1]',
     'Divulgation croisée, profil inexact et perte de maîtrise du suivi ; conséquences possibles sur une future prise en charge.',
     'Gravité importante ; vraisemblance possible si le PC ou la souris est partagé.',
     'Séparer les profils/fichiers, filtrer par session, afficher l’utilisateur actif et authentifier l’objet. Ne pas assimiler un UUID de session à une identité vérifiée.',
     'Enchaîner deux profils et deux sessions ; vérifier l’absence de mélange et le refus d’une source étrangère. Liens : risques 10 et 14.')

page('Conservation, détournement et perte')
risk('A4. Historique oublié ou suppression incomplète',
     'Le fichier continue à grossir après la fin du suivi, ou réapparaît depuis une sauvegarde. La purge n’existe pas dans la passerelle examinée. [P1]',
     'Exposition prolongée de données intimes et impossibilité pratique de maîtriser leur devenir.',
     'Gravité importante ; vraisemblance forte si l’usage se prolonge sans règle de clôture ni action manuelle.',
     'Ajouter suppression par période/totale, clôture du suivi et règles pour les copies gérées. Réexaminer périodiquement le besoin de garder l’historique. Ne pas recopier des bruts inutiles dans les synthèses.',
     'Supprimer un jeu fictif, relancer l’application puis restaurer une sauvegarde de test : vérifier que les données supprimées ne sont pas réintroduites sans contrôle. Lien : risque 9.')
risk('A5. Réutilisation pour surveiller ou évaluer',
     'Des horaires et signaux initialement collectés pour le suivi sont interprétés comme des indicateurs de présence, de stress ou de performance puis transmis à un tiers. Ce scénario est hypothétique : cette fonction n’est pas fournie par le prototype. [P1]',
     'Pression, perte d’autonomie, discrimination ou conséquences professionnelles sur la base d’un profil non fiable.',
     'Gravité importante ; vraisemblance possible uniquement en cas de partage ou de changement de finalité.',
     'Limiter la finalité au suivi défini. Exclure les tableaux de productivité et le partage automatique. Expliquer les limites des inférences et réévaluer tout nouveau destinataire.',
     'Examiner les écrans et exports ; vérifier qu’ils ne produisent pas de score de stress, de diagnostic ou de rendement. Faire relire la notice par un utilisateur.')
risk('A6. Perte ou altération de l’historique',
     'Panne du PC, corruption du CSV, modification manuelle ou données incohérentes rendent l’historique incomplet ou trompeur. Le stockage local ne fournit pas à lui seul une sauvegarde ni une preuve d’intégrité. [P1]',
     'Perte de données utiles au suivi, impossibilité de les consulter ou de les transmettre correctement ; décisions ultérieures fondées sur des informations fausses.',
     'Gravité modérée dans le suivi expérimental non urgent ; à réévaluer si l’historique devient déterminant pour une prise en charge. Vraisemblance possible.',
     'Sauvegarde locale chiffrée choisie par l’utilisateur, contrôle de cohérence, séparation des sessions, indication des lacunes et traçabilité des corrections.',
     'Simuler corruption et restauration avec données fictives ; vérifier absence de faux état rassurant et restitution du bon historique. Liens : risques 1, 4, 14, 17 et 18.')
p('<b>Résiduel A1 à A6 :</b> non validé. Les mesures sont proposées ; leur présence dans ce document ne démontre pas leur mise en œuvre. Les résultats des contrôles doivent être consignés avant l’acceptation des risques.','SmallFR')

page('Décision et références')
h('Une AIPD est-elle obligatoire ici ?')
p('Le seul fait de garder les données sur un PC personnel ne répond pas à cette question. Un usage strictement personnel ou domestique peut relever de l’exception de l’article 2 du RGPD. Une collecte organisée par l’équipe, un établissement ou un professionnel doit être évaluée dans son propre cadre. [P7]')
p('La liste CNIL vise notamment certains traitements de santé en établissement et la surveillance constante des employés. Ces situations ne sont pas établies pour ce prototype individuel. En revanche, les données sensibles et un suivi systématique rendent l’examen des critères AIPD nécessaire avant un déploiement organisé. Le contexte des patients, l’échelle et les destinataires restent à préciser. [P8, P9]')
p('<b>Conclusion du dossier :</b> conserver cette analyse préparatoire et compléter l’examen d’obligation. Ne pas déclarer une AIPD réglementaire validée. Si un risque élevé subsiste malgré les mesures, le responsable doit examiner la consultation préalable de la CNIL. [P9]')
h('Actions restant à attribuer et vérifier')
p('1. Identifier le responsable du traitement et le contact pour les droits. Pour une collecte encadrée, documenter la base de l’article 6 et la condition de l’article 9 applicable ; ne pas présumer qu’un accord informel suffit. [P10]<br/>2. Justifier chaque mesure conservée, arrêter la durée des bruts et publier la notice.<br/>3. Mettre en œuvre les accès, la séparation des sessions et la suppression de l’historique.<br/>4. Réaliser les essais A1 à A6 sur données fictives ; compléter les niveaux résiduels et recueillir l’avis des utilisateurs. Associer le DPO s’il est désigné.<br/>5. Faire dater la décision par le responsable et réviser le dossier si serveur, nouveaux destinataires ou usage clinique sont ajoutés.')
h('Sources consultées le 16 octobre 2026')
sources=[
('P1','Projet : code R3, gateway.py et dashboard.py (révision f76c7e4)','https://github.com/lebretyves/TP4-IoT-Autonomie/tree/f76c7e4bd4bdb517066562b716aee0732e4f6341/variantes/04_veille_R3'),
('P2','CNIL : définition des données de santé','https://www.cnil.fr/fr/quest-ce-ce-quune-donnee-de-sante'),
('P3','Apple : Health App & Privacy, rubrique Retention','https://www.apple.com/legal/privacy/data/en/health-app/'),
('P4','Google : confidentialité Google Health, durée des données','https://support.google.com/product-documentation/answer/13532616?hl=fr'),
('P5','CNIL : durées de conservation','https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees'),
('P6','CNIL : droits des personnes','https://www.cnil.fr/fr/passer-laction/les-droits-des-personnes-sur-leurs-donnees'),
('P7','RGPD : article 2, champ d’application','https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre1'),
('P8','CNIL : liste des traitements exigeant une AIPD','https://www.cnil.fr/sites/default/files/atoms/files/liste-traitements-aipd-requise.pdf'),
('P9','CNIL : principes et réalisation d’une AIPD','https://www.cnil.fr/fr/ce-quil-faut-savoir-sur-lanalyse-dimpact-relative-la-protection-des-donnees-aipd'),
('P10','CNIL : formalités pour les données de santé','https://www.cnil.fr/fr/quelles-formalites-pour-les-traitements-de-donnees-de-sante')]
for key,label,url in sources:p(f'{key}. <link href="{escape(url)}" color="#174F79">{escape(label)}</link>','SmallFR')
p('Éléments projet : choix de stockage et d’historique confirmés par l’utilisateur ; lecture du code et du dossier technique. Aucun résultat de test de sécurité du PC, aucun avis DPO et aucune acceptation réglementaire ne sont présumés.','SmallFR')

def footer(c,doc):
    c.saveState();c.setStrokeColor(colors.HexColor('#CFD9E0'));c.line(45,39,A4[0]-45,39)
    c.setFont('Arial',8);c.setFillColor(colors.HexColor('#51636F'))
    c.drawString(45,26,'Cas G - AIPD préparatoire - 19 octobre 2026')
    c.drawRightString(A4[0]-45,26,str(doc.page));c.restoreState()
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=45,leftMargin=45,topMargin=38,bottomMargin=51,title='Analyse d’impact - Souris connectée Cas G',author='Équipe 2')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
