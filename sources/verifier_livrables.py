"""Vérifie les livrables sans modifier le classeur ; openpyxl est utilisé en lecture."""
from pathlib import Path
import hashlib, json
from collections import Counter
import openpyxl, pymupdf
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'sources/risques.json').read_text(encoding='utf-8'))
src=openpyxl.load_workbook(ROOT/'supports/TP_M3_2_Analyse_risques.xlsx')
dst=openpyxl.load_workbook(ROOT/'analyses/m3/analyse_risques_eq02.xlsx')
val=openpyxl.load_workbook(ROOT/'analyses/m3/analyse_risques_eq02.xlsx',data_only=True)
count=0
for name in src.sheetnames:
 for row in src[name]:
  for c in row:
   if c.data_type=='f':
    expected=c.value.replace('$18','$30') if name=='Synthèse' else c.value
    if name=='Synthèse' and c.coordinate in ['B16','C12','C16']:continue
    assert dst[name][c.coordinate].value==expected,(name,c.coordinate,'formule incorrecte')
    count+=1
for i,r in enumerate(data['risques'],9):
 sh=val['Analyse de risques']
 assert all(sh.cell(i,c).value is not None for c in range(1,19))
 assert sh.cell(i,9).value==r['g']*r['p']
 assert sh.cell(i,16).value==r['ga']*r['pa']
 assert sh.cell(i,18).value==r['justification']
checks=[val['Synthèse'].cell(i,2).value for i in range(12,17)]
assert checks==[22,15,5,2,0],checks
for sheet in val:
 for row in sheet:
  for c in row:assert c.data_type!='e',(sheet.title,c.coordinate,c.value)
assert dst['Analyse de risques'].freeze_panes=='D9'
for address in ['B30','G30','H30','N30','O30']:
 assert any(address in v.sqref for v in dst['Analyse de risques'].data_validations.dataValidation),address
assert {str(k.sqref) for k in dst['Analyse de risques'].conditional_formatting}=={'I9:J30','P9:Q30'}
assert [val['Analyse de risques'].cell(i,1).value for i in range(9,31)]==list(range(1,23))
assert [val['Failles et preuves'].cell(i,1).value for i in range(4,16)]==list(range(11,23))
pdf=pymupdf.open(ROOT/'analyses/m3/TP_M3_2_analyse_risques_cas_G.pdf')
assert len(pdf)==9
links=[a for page in pdf for a in page.get_links()]
assert len(links)==21
aipd=pymupdf.open(ROOT/'analyses/m3/analyse_impact_souris_cas_G.pdf')
assert len(aipd)==5
assert sum(len(p.get_links()) for p in aipd)==10
at='\n'.join(p.get_text() for p in aipd).replace('\n',' ')
for phrase in ['A1.','A2.','A3.','A4.','A5.','A6.','durée du suivi','suppression à tout moment','Apple','Google','CNIL']:assert phrase in at,phrase
def level(x):return 'élevé' if x>=6 else 'moyen' if x>=3 else 'faible'
report={'date':'2026-10-16','equipe':2,'risques':22,'formules_modele_verifiees_et_plages_etendues':count,'controles_synthese':checks,'avant':dict(Counter(level(r['g']*r['p']) for r in data['risques'])),'residuels_cibles':dict(Counter(level(r['ga']*r['pa']) for r in data['risques'])),'pages_pdf_risques':len(pdf),'liens_pdf_risques':len(links),'pages_pdf_aipd':len(aipd),'liens_pdf_aipd':10,'moteur_calcul':'artifact-tool ; dernière ligne et entrée vide testées dans le générateur','excel_natif_teste':False,'aipd_statut':'préparatoire ; mesures et gouvernance à compléter','gestion_conservation_implementee':False,'essais_materiels_realises':False,'supports_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'supports').iterdir() if p.is_file()}}
(ROOT/'analyses/m3/verification_livrables.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
