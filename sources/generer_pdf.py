"""Complément lisible au classeur du TP M3-2 ; données communes dans risques.json."""
from pathlib import Path
import json
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'sources/risques.json').read_text(encoding='utf-8'))
REG=json.loads((ROOT/'sources/reglementation.json').read_text(encoding='utf-8'))
pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial',boldItalic='Arial-Bold')
ss=getSampleStyleSheet()
ss.add(ParagraphStyle(name='Body',fontName='Arial',fontSize=10,leading=14,spaceAfter=8,textColor=colors.HexColor('#253443')))
ss.add(ParagraphStyle(name='SmallText',parent=ss['Body'],fontSize=9,leading=12,spaceAfter=5))
ss.add(ParagraphStyle(name='TitleCustom',parent=ss['Body'],fontName='Arial-Bold',fontSize=22,leading=27,spaceAfter=15))
ss.add(ParagraphStyle(name='HeadingCustom',parent=ss['Body'],fontName='Arial-Bold',fontSize=12,leading=16,spaceBefore=9,spaceAfter=7,textColor=colors.HexColor('#204E72')))
story=[]
def p(t,style='Body'): return Paragraph(t,ss[style])
def add(t,style='Body'): story.append(p(t,style))
def title(t): add('TP M3-2 • CAS G • ÉQUIPE 2 • 19 OCTOBRE 2026','SmallText');add(t,'TitleCustom')
def tab(rows,widths):
 t=Table([[p(str(c),'SmallText') for c in r] for r in rows],colWidths=widths,hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E5EEF5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#204E72')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#DCE3E8'))]))
 story.append(t)
title('Analyse des risques de notre souris')
add('Souris ergonomique P4 avec une seule batterie de 1 500 mAh. Le tableau complet est <b>analyse_risques_eq02.xlsx</b> dans <b>analyses/m3/</b>. Il reprend les 22 scénarios et réévalue les conséquences médicales pour la destination cardiovasculaire, avec les colonnes et seuils du modèle. Une analyse d’impact sur les données personnelles est fournie séparément dans <b>analyse_impact_souris_cas_G.pdf</b>.')
add('Le projet analysé','HeadingCustom')
add(escape(D['finalite']))
add(escape(D['perimetre']))
add('La branche prévoit le kit souris MH002, une XIAO nRF52840 Sense avec IMU, le PPG SEN-15219, le GSR Grove avec deux contacts dans la coque et le DS18B20. Le pack final, l’alimentation dans la coque et l’autonomie restent à vérifier. R3 fait de l’acquisition ; il ne fournit pas de recommandation médicale validée. [S1–S4]')
add('1. Pourquoi « batterie vide » n’est pas un dommage ?','HeadingCustom')
add('C’est une cause de perte du suivi. Dans l’exemple du cours : batterie vide → aucune alerte lors de la chute → résidente au sol sans aide → déshydratation ou escarres. Pour notre souris : batterie vide → acquisition interrompue → suivi incomplet interprété comme continu → fausse assurance et retard de prise en charge cardiovasculaire. Le dommage est l’atteinte à la santé, pas la panne.')
add('3. Quels risques sont les plus élevés ?','HeadingCustom')
add('Le score maximal retenu est <b>6</b>, pour 20 scénarios. Les 14 scénarios d’information médicale fausse ou manquante passent à G3 conservatrice : des conséquences graves ne sont pas exclues. Les dangers physiques restent examinés. Les scénarios de gravité 3 demandent une attention prioritaire. Certains partagent des causes ; les comptes ne représentent pas des événements indépendants.')
tab([['Niveau','Avant mesures','Après mesures : cible'],['Élevé','20','0'],['Moyen','2','19'],['Faible','0','3']],[170,150,190])
add('G et P : 1 à 3 ; risque = G × P. Faible : 1–2 ; moyen : 3–4 ; élevé : 6–9. Les probabilités sont des hypothèses pédagogiques. <b>Les scores après mesures sont conditionnels aux essais : ils ne décrivent pas la sécurité actuelle du prototype.</b>','SmallText')
story.append(PageBreak());title('Destination médicale et hypothèse IIa')
for q in REG['qualification']:
 add(q['titre'],'HeadingCustom');add(escape(q['texte']))
add('Références réglementaires et guides','HeadingCustom')
for source in REG['sources']:
 add(f"<b>[{source['id']}]</b> <link href='{escape(source['url'])}' color='#205E8A'>{escape(source['titre'])}</link>",'SmallText')
add('Les guides MDCG accompagnent l’interprétation du règlement ; ils ne constituent pas une certification du projet. Références consultées le 16 octobre 2026.','SmallText')
story.append(PageBreak());title('Relier les 22 risques aux exigences')
add(escape(REG['cadre']),'SmallText')
tab([['Risques / thème','Références à examiner','Exigence concernée']]+[[', '.join(map(str,g['ids']))+' - '+g['theme'],g['references'],g['exigence']] for g in REG['groupes']],[145,215,150])
add('L’onglet <b>Réglementation</b> détaille chaque risque, l’application au projet et la preuve attendue. Les essais sont repris des lignes du TP pour conserver le lien entre exigence, mesure et vérification. Les cotations des scénarios médicaux ont été revues pour la destination cardiovasculaire.','SmallText')
add(escape(REG['limites']),'SmallText')
for start in range(0,len(D['risques']),5):
 end=min(start+5,len(D['risques']))
 story.append(PageBreak());title(f'2. Les chaînes de risque — {start+1} à {end}')
 add('Chaque chaîne relie la panne ou le danger à une personne exposée, puis à un dommage. Les mesures et leurs justifications détaillées sont dans les colonnes K à R du classeur.','SmallText')
 for r in D['risques'][start:end]:
  block=[p(f"{r['id']}. {escape(r['danger'])}",'HeadingCustom'),p(f"<b>{r['type']}</b> — Avant : {r['g']} × {r['p']} = {r['g']*r['p']} ; résiduel cible : {r['ga']} × {r['pa']} = {r['ga']*r['pa']}.",'SmallText'),p('<b>Séquence :</b> '+escape(r['sequence'].rstrip('.'))+'.','SmallText'),p('<b>Situation :</b> '+escape(r['situation']),'SmallText'),p('<b>Dommage :</b> '+escape(r['dommage']),'SmallText')]
  story.append(KeepTogether(block))
story.append(PageBreak());title('4–6. Maîtriser les risques')
add('4. Trois mesures pour l’échauffement de la batterie','HeadingCustom')
for k,label in [('conception','1 — Conception'),('protection','2 — Protection'),('information','3 — Information')]: add(f"<b>{label}.</b> {escape(D['risques'][1][k])}")
add('La notice vient en dernier parce qu’elle dépend de la lecture et du comportement de l’utilisateur. Elle n’empêche pas, à elle seule, un court-circuit interne. Il faut d’abord éviter le défaut par le montage et limiter ses effets par les protections.')
add('5. Quels risques restent moyens ? Peut-on les accepter ?','HeadingCustom')
add('Dix-neuf scénarios restent à <b>3 × 1 = 3</b> dans les cibles : les cinq dangers physiques graves et les quatorze scénarios médicaux réévalués. Les risques 6, 7 et 9 ont une cible faible. G reste inchangée après mesures ; P1 est seulement une hypothèse à justifier par les essais. Le bénéfice cardiovasculaire reste à démontrer.')
add('<b>Notre décision : acceptation réelle différée.</b> La classe « moyen » du TP n’autorise pas la mise en service. Il faut qualifier le pack, le montage et les protections, vérifier la thermique et les erreurs de branchement, puis confronter le risque restant au bénéfice clinique. Si la maîtrise reste insuffisante, nous revoyons le circuit ou la coque. Le simple fait de choisir 1 500 mAh ne justifie pas le risque.')
add('6. Quelles règles du module 2 sont des mesures de maîtrise ?','HeadingCustom')
add('<b>Qualité :</b> rejeter les données anciennes ou invalides et afficher « mesure indisponible » (risques 1, 4 et 8). <b>Autonomie :</b> dimensionner puis mesurer toute la chaîne d’alimentation ; ne pas promettre les anciens chiffres théoriques (1 et 2). <b>Sécurité :</b> authentifier le BLE, protéger les fichiers, séparer les comptes ; si MQTT devient distant, utiliser TLS, habituellement sur 8883, avec validation des certificats et identité par objet (9 et 10). Le numéro de port seul ne prouve aucun chiffrement.')
add('Dans R3, l’option MQTT vise <b>127.0.0.1:1883</b> et la découverte BLE repose sur le nom de la souris. Nous les avons traitées comme des fonctions de prototype à sécuriser, pas comme des protections déjà réalisées. [S4]')
add('Une mesure peut créer un nouveau risque','HeadingCustom')
add('Un filtrage trop strict peut supprimer beaucoup de mesures et rendre le suivi inutilisable. Il faut afficher les périodes manquantes, jamais un état rassurant par défaut. De même, un appairage trop contraignant peut empêcher la reconnexion : vérifier aussi le retour à un suivi valide.')
story.append(PageBreak());title('Vérifications et traçabilité')
add('Ce qui est terminé pour le TP','HeadingCustom')
add('Vingt-deux risques renseignés, les trois familles présentes, les quatre éléments de chaque chaîne, les cotations, les trois mesures dans l’ordre et les justifications. Les contrôles de Synthèse sont à OK pour les cibles saisies. La mise en commun avec la classe reste à faire ; aucun retour d’autres équipes n’est inventé.')
add('Ce qui reste à réaliser sur le projet','HeadingCustom')
tab([['Essais','Objet de la vérification'],['T1–T3','Coupures et autonomie ; pack, charge et thermique ; rails, branchements et ports USB.'],['T4–T5','Qualité des mesures puis validité des indicateurs de stress et de leur utilité cardiovasculaire.'],['T6–T8','Confort avec pack final, contacts cutanés/nettoyage et compréhension de l’interface.'],['T9–T10','Confidentialité, contrôle des accès, authentification de l’objet et rejet des données rejouées.'],['11–22','Liquides, chute, vieillissement, sessions, mises à jour, perturbations, valeurs extrêmes, volume CSV, MQTT, maintenance, démarrage et diversité des utilisateurs.']],[70,440])
add('Le détail et l’état actuel de chaque vérification se trouvent dans les onglets <b>Suivi et sources</b> (1 à 10) et <b>Failles et preuves</b> (11 à 22). Aucun de ces essais n’est déclaré réussi sur une souris assemblée. Avant tout contact humain, la sécurité électrique et mécanique doit être vérifiée.','SmallText')
story.append(PageBreak());title('Sources et portée de l’analyse')
for s in D['sources']:
 url=s['url'] if s['url'].startswith('https:') else '../../'+s['url']
 add(f"<b>[{s['id']}]</b> <link href={escape(url, {'chr(34)':'&quot;'})!r} color='#205E8A'>{escape(s['titre'])}</link>",'SmallText')
add('Branche étudiée : cas-g-choisi. Risques initiaux : référence b762570 ; ajouts : revue f76c7e4. Les liens figés des sources précisent chaque version. Sources Web consultées le 16 octobre 2026. Le sujet et le classeur d’origine sont conservés dans supports/. Les échelles du cours sont utilisées pour cet exercice, sans déclaration de conformité à ISO 14971.','SmallText')
def footer(c,doc):
 c.setFont('Arial',8);c.setFillColor(colors.HexColor('#5E6B75'));c.drawString(42,25,'Équipe 2 • TP M3-2 • Souris ergo 1 500 mAh');c.drawRightString(A4[0]-42,25,str(doc.page))
out=ROOT/'analyses/m3/TP_M3_2_analyse_risques_cas_G.pdf'
SimpleDocTemplate(str(out),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=35,bottomMargin=43,title='TP M3-2 — Analyse des risques — Cas G — Équipe 2',author='Équipe 2').build(story,onFirstPage=footer,onLaterPages=footer)
import pymupdf
(ROOT/'tmp').mkdir(exist_ok=True)
pdf=pymupdf.open(out)
assert len(pdf)==(len(D['risques'])+4)//5+6,len(pdf)
for i,page in enumerate(pdf):page.get_pixmap(matrix=pymupdf.Matrix(1.3,1.3)).save(ROOT/f'tmp/tp_risques_{i+1}.png')
print(f'PDF : {len(pdf)} pages ; {sum(len(p.get_links()) for p in pdf)} liens.')
