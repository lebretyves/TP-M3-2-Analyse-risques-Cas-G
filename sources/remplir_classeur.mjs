import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {FileBlob, SpreadsheetFile} from '@oai/artifact-tool';
process.on('uncaughtException',err=>{console.error(err.message);console.error((err.stack||'').split('\n').filter(x=>x.includes('build.mjs')).join('\n'));process.exit(1);});
const root=new URL('../',import.meta.url);
const data=JSON.parse(await fs.readFile(new URL('sources/risques.json',root),'utf8'));
const reg=JSON.parse(await fs.readFile(new URL('sources/reglementation.json',root),'utf8'));
const initial={risques:data.risques.filter(r=>r.id<=10),sources:data.sources.filter(s=>s.id.startsWith('S'))};
const supplement={risques:data.risques.filter(r=>r.id>=11),sources:data.sources.filter(s=>s.id.startsWith('C'))};
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(fileURLToPath(new URL('supports/TP_M3_2_Analyse_risques.xlsx',root))));
const s=wb.worksheets.getItem('Analyse de risques');
const first=9,last=first+data.risques.length-1;
s.getRange('A19:R30').clear({applyTo:'all'});
for(let row=19;row<=last;row++)s.getRange(`A${row}:R${row}`).copyFrom(s.getRange('A18:R18'),'all');
s.getRange('A1').values=[['Analyse de risques — Cas G — 22 scénarios']];
s.getRange('C2').values=[['eq02 — Équipe 2']];
s.getRange('C3').dataValidation={rule:{type:'list',values:['G — Souris P4 — batterie unique 1 500 mAh']}};
s.getRange('C3').values=[['G — Souris P4 — batterie unique 1 500 mAh']];
s.getRange('C4').values=[['Usage envisagé : aide au professionnel pour la prise en charge des TMS. Fonction médicale non réalisée ni validée.']];
s.getRange('C4:F4').format.wrapText=true;s.getRange('A4:R4').format.rowHeight=40;

s.mergeCells('A5:R5');
s.getRange('A5').values=[['22 scénarios : risques initiaux 1 à 10 et ajouts 11 à 22. Cotations à relire. Résiduels = cibles après mesures vérifiées, pas sécurité démontrée du prototype.']];
s.getRange('A5:R5').format={wrapText:true,rowHeight:30,font:{bold:true,color:'#8A3E00',size:11}};
s.mergeCells('A6:R6');
s.getRange('A6').values=[['Analyse de risques du dispositif : pannes, erreurs et dommages. Analyse d’impact sur la vie privée (AIPD) : document PDF séparé, adapté aux données de la souris sur le PC utilisateur.']];
s.getRange('A6:R6').format={wrapText:true,rowHeight:30,font:{size:11,color:'#1F4E78'}};
s.getRange('N7').values=[['4. RÉSIDUEL CIBLE — APRÈS VÉRIFICATION']];
s.getRange('R8').values=[['Justification, lien avec le TP initial et limites']];
for(const [i,r] of data.risques.entries()){
 const n=first+i;
 s.getRange(`A${n}:H${n}`).values=[[r.id,r.type,r.danger,r.sequence,r.situation,r.dommage,r.g,r.p]];
 s.getRange(`K${n}:O${n}`).values=[[r.conception,r.protection,r.information,r.ga,r.pa]];
 s.getRange(`R${n}`).values=[[r.justification]];
 s.getRange(`I${n}`).formulas=[[`=IF(OR(G${n}="",H${n}=""),"",G${n}*H${n})`]];
 s.getRange(`J${n}`).formulas=[[`=IF(I${n}="","",IF(I${n}>='Échelles'!$C$15,"Élevé : inacceptable",IF(I${n}>='Échelles'!$C$14,"Moyen : à réduire","Faible : acceptable")))`]];
 s.getRange(`P${n}`).formulas=[[`=IF(OR(N${n}="",O${n}=""),"",N${n}*O${n})`]];
 s.getRange(`Q${n}`).formulas=[[`=IF(P${n}="","",IF(P${n}>='Échelles'!$C$15,"Élevé : inacceptable",IF(P${n}>='Échelles'!$C$14,"Moyen : à réduire","Faible : acceptable")))`]];
}
s.getRange(`A9:R${last}`).format.wrapText=true;
s.getRange(`A9:R${last}`).format.rowHeight=120;
s.getRange('A9:R18').format.rowHeight=140;
s.getRange(`A9:R${last}`).format.font.italic=false;
for(const cols of [['B','F'],['K','M'],['R','R']])s.getRange(`${cols[0]}9:${cols[1]}${last}`).format.verticalAlignment='top';
s.getRange(`B19:B${last}`).dataValidation={rule:{type:'list',values:['Technique','Utilisation','Cybersécurité']}};
for(const c of ['G','H','N','O'])s.getRange(`${c}19:${c}${last}`).dataValidation={rule:{type:'list',values:['1','2','3']}};
// Extend the template's reactive risk colours to every supplementary row.
for(const [start,end,valueCol] of [['I','J','I'],['P','Q','P']]){
 const rg=s.getRange(`${start}9:${end}${last}`);rg.conditionalFormats.clear();
 rg.conditionalFormats.addCustom(`AND(ISNUMBER($${valueCol}9),$${valueCol}9>=6)`,{fill:'#ED6A2C',font:{bold:true,color:'#FFFFFF'}});
 rg.conditionalFormats.addCustom(`AND(ISNUMBER($${valueCol}9),$${valueCol}9>=3,$${valueCol}9<6)`,{fill:'#FCE4D6',font:{color:'#000000'}});
 rg.conditionalFormats.addCustom(`AND(ISNUMBER($${valueCol}9),$${valueCol}9<3)`,{fill:'#E2F0D9',font:{color:'#000000'}});
}
s.mergeCells(`A${last+2}:R${last+2}`);
s.getRange(`A${last+2}`).values=[['Failles, preuves, essais et choix de relecture dans « Failles et preuves ». Des scénarios peuvent être fusionnés avec une ligne existante : ne pas additionner ces comptes comme des risques indépendants.']];
s.getRange(`A${last+2}:R${last+2}`).format={wrapText:true,rowHeight:30,font:{size:11,color:'#555555'}};

const syn=wb.worksheets.getItem('Synthèse');
for(let row=1;row<=16;row++)for(let col=0;col<8;col++){
 const cell=syn.getCell(row-1,col);const f=cell.formulas[0]?.[0];
 if(f)cell.formulas=[[f.replaceAll('$18',`$${last}`)]];
}
syn.getRange('A1').values=[['Synthèse — 22 scénarios du cas G']];
syn.mergeCells('A2:H2');syn.getRange('A2').values=[['Risques 1 à 22. Après = cible conditionnelle, pas état réel de sécurité du prototype.']];
syn.getRange('A2:H2').format={wrapText:true,rowHeight:32,font:{size:11,color:'#8A3E00',bold:true}};
syn.getRange('E3').values=[['APRÈS mesures vérifiées : cible']];
syn.getRange('A4:H4').format.wrapText=true;syn.getRange('A4:H4').format.rowHeight=36;
syn.getRange('A11').values=[['Comptage des scénarios']];
syn.getRange('A12').values=[['Scénarios étudiés']];
syn.getRange('C12').formulas=[['=B12&" scénarios ; cotations à valider par les essais"']];
syn.getRange('A16').values=[['Élevés résiduels cibles']];
syn.getRange('B16').formulas=[[`=COUNTIFS('Analyse de risques'!$P$9:$P$${last},">="&'Échelles'!$C$15)`]];
syn.getRange('C16').formulas=[['=IF(B16=0,"Aucun élevé dans les cibles ; essais encore nécessaires","Cibles à revoir : risque élevé restant")']];
syn.getRange('A12:H16').format.wrapText=true;syn.getRange('A12:H16').format.rowHeight=34;
syn.mergeCells('A18:H19');syn.getRange('A18').values=[['N° 2, 3, 11, 12 et 20 : cibles moyennes, acceptation différée. Les autres cibles faibles supposent les mesures réalisées et vérifiées. Les probabilités proposées ne sont pas des fréquences mesurées.']];
syn.getRange('A18:H19').format={wrapText:true,rowHeight:27,font:{size:11,color:'#8A3E00'}};

const read=wb.worksheets.getItem('Lisez-moi');
read.getRange('A1').values=[['TP M3-2 — Analyse de risques du cas G']];
read.getRange('A3').values=[['Proposition de relecture du 16 octobre 2026. Le modèle et ses seuils sont conservés. Les 22 scénarios ne constituent pas une analyse exhaustive ni une validation du prototype.']];
read.getRange('A16').values=[['Analyse de risques : dix risques initiaux conservés et douze scénarios ajoutés, numérotés 11 à 22. Colonnes et seuils du TP conservés.']];
read.getRange('A17').values=[['Synthèse : matrices et comptes des 22 scénarios. Des scénarios peuvent partager une cause ; les comptes ne mesurent pas des événements indépendants.']];
read.getRange('A19').values=[['Périmètre et relecture']];
read.getRange('A20').values=[['Failles et preuves : faiblesse possible, état des connaissances, essais à réaliser, sources et choix de relecture. Les cellules « Décision » et « Notes de relecture » sont à compléter.']];
read.getRange('A22').values=[['Usage médical envisagé : aide au professionnel pour la prise en charge des TMS chez un adulte utilisant un ordinateur, suivi non urgent. R3 mesure des signaux ; il ne produit pas de recommandation médicale validée.']];
read.getRange('A23').values=[['G et P proposés de 1 à 3. P2 = hypothèse qualitative de dommage possible, pas une fréquence observée. Résiduel cible : G inchangée et P1 seulement si les mesures et essais justifient cette réduction. Sinon conserver ou revoir la cotation initiale.']];
read.getRange('A24').values=[['Pour les dommages liés au suivi, G2 suppose des conséquences réversibles nécessitant des soins. Si une décision critique, une séquelle ou une surveillance d’hypoxémie devient possible, revoir le périmètre et la gravité.']];
read.getRange('A25').values=[['Les constats logiciels ne prouvent ni une fréquence de dommage ni un incident matériel. La mise à jour malveillante évoquée au n° 15 est conditionnelle ; aucune vulnérabilité du chargeur de démarrage n’a été établie.']];
read.getRange('A26').values=[['Suivi et sources documente les risques initiaux (sources S0 à S8). Failles et preuves documente les ajouts (sources C0 à C11). Les cotations résiduelles restent conditionnelles aux mesures et essais.']];
read.getRange('A28').values=[['Analyse de risques du dispositif : quelles pannes ou erreurs peuvent causer un dommage ? Exemple adapté : une mesure erronée peut-elle conduire à un conseil inadapté ?']];
read.getRange('A29').values=[['Analyse d’impact (AIPD) : comment la collecte de signaux physiologiques et de mouvements peut-elle affecter la vie privée et les droits de la personne ? Document séparé : analyse_impact_souris_cas_G.pdf.']];
read.getRange('A30').values=[['Les données restent prévues sur le PC de l’utilisateur. Historique conservé pendant le suivi, suppression possible à tout moment et prévue à la fin du suivi. Cette règle reste à implémenter. L’AIPD doit aussi évaluer nécessité, information, accès et sécurité.']];
read.getRange('A28:A30').format={wrapText:true,rowHeight:64,verticalAlignment:'top',font:{size:11}};
read.getRange('A1:A26').format.wrapText=true;
read.getRange('A3').format.rowHeight=52;
read.getRange('A16:A17').format.rowHeight=42;
read.getRange('A20').format.rowHeight=52;
read.getRange('A22:A26').format.rowHeight=64;
read.getRange('A22:A26').format.verticalAlignment='top';

const e=wb.worksheets.getItem('Échelles');
e.getRange('A25:D25').format.wrapText=true;e.getRange('A25:D25').format.rowHeight=42;
e.mergeCells('A30:D32');e.getRange('A30').values=[['Les repères EHPAD ci-dessus appartiennent au cours. Pour cette analyse, les probabilités sont des propositions qualitatives à relire, sans fréquence mesurée sur la souris. Les seuils du cours restent inchangés.']];
e.getRange('A30:D32').format={wrapText:true,rowHeight:24,font:{size:11}};

{
const n=wb.worksheets.add('Suivi et sources');
n.showGridLines=false;
n.getRange('A1:D1').merge();n.getRange('A1').values=[['Équipe 2 — Mesures à vérifier et sources']];
n.getRange('A1:D1').format.font={name:'Arial',size:14,bold:true};
n.getRange('A3:D3').values=[['Risque','État actuel vérifié dans la branche','Vérification à réaliser','Statut']];
n.getRange('A4:D13').values=initial.risques.map(r=>[r.id,r.etat,r.test,'À réaliser — aucune validation matérielle ou clinique fournie']);
n.getRange('A15:D15').values=[['Source','Document','Lien / chemin','Portée']];
n.getRange('A16:D24').values=initial.sources.map(x=>[x.id,x.titre,x.url,x.detail]);
n.getRange('A3:D24').format.font={name:'Arial',size:11};
n.getRange('A3:D24').format.wrapText=true;
n.getRange('A3:D24').format.verticalAlignment='top';
for(const col of ['B','C','D'])n.getRange(`${col}3:${col}24`).format.columnWidth=60;
n.getRange('A3:A24').format.columnWidth=10;
n.getRange('A4:D13').format.rowHeight=130;
n.getRange('A16:D24').format.rowHeight=110;
for (const r of [3,15]) n.getRange(`A${r}:D${r}`).format={fill:'#1F4E78',font:{color:'#FFFFFF',bold:true},rowHeight:30};
n.freezePanes.freezeRows(3);
}
const n=wb.worksheets.add('Failles et preuves');n.showGridLines=false;
n.getRange('A1:H1').merge();n.getRange('A1').values=[['Risques supplémentaires — Failles, preuves et relecture']];
n.getRange('A1:H1').format={font:{name:'Arial',size:14,bold:true},rowHeight:28};
n.getRange('A2:H2').merge();n.getRange('A2').values=[['Constat vérifié ≠ dommage constaté. Choisir « À ajouter », « À fusionner », « À écarter » ou « À approfondir » après lecture.']];
n.getRange('A2:H2').format={font:{name:'Arial',size:11,color:'#555555'},wrapText:true,rowHeight:32};
n.getRange('A3:H3').values=[['N°','Faille / faiblesse possible','Constat et niveau de preuve','Vérification à réaliser','Lien avec les risques initiaux','Sources','Décision','Notes de relecture']];
n.getRange('A4:H15').values=supplement.risques.map(r=>[r.id,r.faille,r.statut+'\n'+r.preuve,r.test,r.lien,r.sources,'À relire',null]);
n.getRange('A3:H15').format.font={name:'Arial',size:11};
n.getRange('A3:H15').format.wrapText=true;n.getRange('A3:H15').format.verticalAlignment='top';
const widths={A:7,B:42,C:54,D:52,E:38,F:14,G:19,H:38};
for(const [c,w] of Object.entries(widths))n.getRange(`${c}1:${c}35`).format.columnWidth=w;
n.getRange('A4:H15').format.rowHeight=110;
n.getRange('G4:H15').format.fill='#EAF2F8';n.getRange('G4:H15').format.font.color='#0000FF';
n.getRange('G4:G15').dataValidation={rule:{type:'list',values:['À relire','À ajouter','À fusionner','À écarter','À approfondir']}};
n.getRange('A3:H3').format={fill:'#1F4E78',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true};
n.getRange('A17:H18').merge();n.getRange('A17').values=[['R1–R10 désignent les risques initiaux, présents dans le même tableau. Sources C0–C11 propres aux ajouts ; S0–S8 dans « Suivi et sources ». Une ligne du complément peut être fusionnée avec eux. N° 15 : les régressions sont techniques ; une mise à jour non authentifiée serait un scénario cyber distinct, conditionnel et non démontré ici.']];
n.getRange('A17:H18').format={font:{name:'Arial',size:11},wrapText:true,rowHeight:24};
n.getRange('A21:H21').merge();n.getRange('A21').values=[['Sources et portée — consultation du 16 octobre 2026']];
n.getRange('A21:H21').format={font:{name:'Arial',size:12,bold:true},rowHeight:28};
n.getRange('C22:F22').merge();n.getRange('G22:H22').merge();
n.getRange('A22').values=[['ID']];n.getRange('B22').values=[['Document']];n.getRange('C22').values=[['Lien / référence']];n.getRange('G22').values=[['Portée de la source']];
n.getRange('A22:H22').format={fill:'#1F4E78',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:30};
for(const [i,src] of supplement.sources.entries()){
 const row=23+i;n.getRange(`C${row}:F${row}`).merge();n.getRange(`G${row}:H${row}`).merge();
 n.getRange(`A${row}`).values=[[src.id]];n.getRange(`B${row}`).values=[[src.titre]];n.getRange(`C${row}`).values=[[src.url]];n.getRange(`G${row}`).values=[[src.detail]];
 n.getRange(`A${row}:H${row}`).format={font:{name:'Arial',size:11},wrapText:true,verticalAlignment:'top',rowHeight:95};
}
n.freezePanes.freezeRows(3);n.freezePanes.freezeColumns(1);

const legal=wb.worksheets.add('Réglementation');legal.showGridLines=false;
const legalWidths={A:7,B:40,C:39,D:34,E:57,F:62,G:21};
for(const [col,width] of Object.entries(legalWidths))legal.getRange(`${col}1:${col}40`).format.columnWidth=width;
legal.getRange('A1:G1').merge();legal.getRange('A1').values=[['Destination médicale, classification et traçabilité des risques']];
legal.getRange('A1:G1').format={font:{name:'Arial',size:14,bold:true},rowHeight:30};
for(const [i,q] of reg.qualification.entries()){
 const row=i+3;legal.getRange(`A${row}:G${row}`).merge();
 legal.getRange(`A${row}`).values=[[q.titre+' : '+q.texte]];
 legal.getRange(`A${row}:G${row}`).format={font:{name:'Arial',size:11},wrapText:true,rowHeight:43,verticalAlignment:'top'};
}
legal.getRange('A8:G8').merge();legal.getRange('A8').values=[[reg.cadre]];
legal.getRange('A8:G8').format={font:{name:'Arial',size:11,color:'#8A3E00'},wrapText:true,rowHeight:43};
legal.getRange('A10:G10').values=[['Risque','Danger du TP','Références à examiner','Exigence concernée','Application au projet','Preuve / vérification à produire','État']];
legal.getRange('A10:G10').format={fill:'#1F4E78',font:{name:'Arial',size:11,color:'#FFFFFF',bold:true},wrapText:true,rowHeight:35};
legal.getRange('A11:G32').values=data.risques.map(r=>{
 const group=reg.groupes.filter(g=>g.ids.includes(r.id));
 if(group.length!==1)throw new Error('Rapprochement réglementaire manquant ou ambigu : '+r.id);
 const g=group[0];return [r.id,r.danger,g.references,g.exigence,g.application,r.test,'À vérifier ; conformité non démontrée'];
});
legal.getRange('A11:G32').format={font:{name:'Arial',size:11},wrapText:true,verticalAlignment:'top',rowHeight:115};
legal.getRange('A34:G34').merge();legal.getRange('A34').values=[[reg.limites]];
legal.getRange('A34:G34').format={font:{name:'Arial',size:11},wrapText:true,rowHeight:46};
for(const [i,source] of reg.sources.entries()){
 const row=36+i;legal.getRange(`B${row}:C${row}`).merge();legal.getRange(`D${row}:G${row}`).merge();
 legal.getRange(`A${row}`).values=[[source.id]];legal.getRange(`B${row}`).values=[[source.titre]];legal.getRange(`D${row}`).values=[[source.url]];
 legal.getRange(`A${row}:G${row}`).format={font:{name:'Arial',size:11},wrapText:true,rowHeight:42,verticalAlignment:'top'};
}
legal.freezePanes.freezeRows(10);legal.freezePanes.freezeColumns(2);
read.getRange('A32').values=[['Réglementation : destination médicale future, classe IIa proposée pour le logiciel (règle 11), statut matériel à préciser et correspondance entre chacun des 22 risques et les exigences à vérifier. La cotation du TP ne détermine pas la classe réglementaire.']];
read.getRange('A32').format={wrapText:true,rowHeight:64,font:{size:11},verticalAlignment:'top'};

wb.recalculate();
// Independent arithmetic and summary checks, including the two rows beyond the original template.
for(const [i,r] of data.risques.entries()){
 const row=first+i;
 if(s.getRange(`I${row}`).values[0][0]!==r.g*r.p||s.getRange(`P${row}`).values[0][0]!==r.ga*r.pa)throw new Error(`Bad risk calculation ${r.id}`);
}
const counts=syn.getRange('B12:B16').values.map(x=>x[0]);
if(JSON.stringify(counts)!==JSON.stringify([22,15,5,2,0]))throw new Error('Summary '+JSON.stringify(counts));
// Exercise the newly extended final row, then restore the proposed inputs.
s.getRange(`O${last}`).values=[[3]];wb.recalculate();
if(s.getRange(`P${last}`).values[0][0]!==6||syn.getRange('B16').values[0][0]!==1)throw new Error('New row not included in formulas '+JSON.stringify({risk:s.getRange(`P${last}`).values,level:s.getRange(`Q${last}`).values,count:syn.getRange('B16').values,formula:syn.getRange('B16').formulas}));
s.getRange(`O${last}`).values=[[null]];wb.recalculate();
if(s.getRange(`P${last}`).values[0][0]!==''||s.getRange(`Q${last}`).values[0][0]!=='')throw new Error('Blank input is not blank output');
s.getRange(`O${last}`).values=[[1]];wb.recalculate();
for(let i=0;i<7;i++)for(const row of wb.worksheets.getItemAt(i).getUsedRange().values)for(const v of row)if(typeof v==='string'&&/^#(REF!|DIV\/0!|VALUE!|NAME\?|N\/A|NUM!|SPILL!|CALC!)/.test(v))throw new Error(v);
await fs.mkdir(new URL('tmp/previews_22/',root),{recursive:true});
const previews=[['Lisez-moi','A22:A30','lisez_moi'],['Échelles','A24:D32','echelles'],['Synthèse','A1:H19','synthese'],['Failles et preuves','A1:H6','preuves_debut'],['Failles et preuves','A12:H15','preuves_fin'],['Failles et preuves','A21:H26','sources_debut'],['Failles et preuves','A31:H34','sources_fin'],['Suivi et sources','A1:D6','suivi'],['Analyse de risques','A1:R8','entete']];
previews.push(['Réglementation','A1:G10','reg_cadre'],['Réglementation','A34:G39','reg_sources'],['Lisez-moi','A28:A32','reg_lisez_moi']);
for(let lo=11;lo<=32;lo+=4)previews.push(['Réglementation',`A${lo}:G${Math.min(lo+3,32)}`,`reg_${lo}`]);
for(const [lo,hi] of [[19,21],[22,24],[25,27],[28,30]]){
 previews.push(['Analyse de risques',`A${lo}:J${hi}`,`avant_${lo}`]);previews.push(['Analyse de risques',`K${lo}:R${hi}`,`apres_${lo}`]);
}
for(const [sheetName,range,file] of previews){
 const img=await wb.render({sheetName,range,scale:1,format:'png'});await fs.writeFile(new URL(`tmp/previews_22/${file}.png`,root),new Uint8Array(await img.arrayBuffer()));
}
const out=await SpreadsheetFile.exportXlsx(wb);
const staged=fileURLToPath(new URL('tmp/analyse_risques_eq02_prepare.xlsx',root));
await out.save(staged);
await fs.copyFile(staged,fileURLToPath(new URL('analyses/m3/analyse_risques_eq02.xlsx',root)));
await fs.writeFile(new URL('tmp/verification_22.json',root),JSON.stringify({scenarios:22,ids:data.risques.map(r=>r.id),counts,initial:{eleves:6,moyens:16,faibles:0},cible:{eleves:0,moyens:5,faibles:17},checks:['22 products before and after','summary includes all 22 risks','last-row change updates summary','blank input stays blank','no formula errors'],engine:'artifact-tool; native Excel recalculation not tested'},null,2));
console.log('Export terminé : 22 scénarios ; 15 techniques, 5 utilisation, 2 cyber ; 5 cibles moyennes et 17 faibles.');
