# TP M3-2 — Analyse des risques — Équipe 2

Analyse de la **souris ergonomique P4 avec une batterie unique de 1 500 mAh**, fondée sur la [branche cas-g-choisi](https://github.com/lebretyves/TP4-IoT-Autonomie/tree/cas-g-choisi).

## Livrables

- **[Excel complété : analyse_risques_eq02.xlsx](analyses/m3/analyse_risques_eq02.xlsx)** — fichier à déposer, conforme au chemin demandé dans le sujet.
- **[PDF explicatif du TP](analyses/m3/TP_M3_2_analyse_risques_cas_G.pdf)** — réponses aux six questions, chaînes des 22 risques et décision sur les risques résiduels.
- **[Analyse d’impact adaptée à la souris](analyses/m3/analyse_impact_souris_cas_G.pdf)** — document séparé sur les données, les droits, les accès et la conservation. Version préparatoire : mesures, essais et gouvernance à compléter.

Le classeur conserve les quatre onglets d'origine et les seuils du cours. Les formules, listes de cotation et couleurs couvrent les 22 lignes. Les 22 scénarios sont conservés ; les conséquences et cotations médicales sont réalignées le 19 octobre 2026. **Suivi et sources** documente les risques initiaux (sources S0 à S8) ; **Failles et preuves** décrit les faiblesses, preuves, essais et décisions de relecture des ajouts 11 à 22 (sources C0 à C11).

## Analyse de risques et analyse d’impact

L’analyse de risques du dispositif traite les pannes et erreurs pouvant causer un dommage : brûlure, fausse assurance cardiovasculaire ou retard de prise en charge, par exemple. L’AIPD examine la nécessité de la collecte, les droits et les effets sur la vie privée. Elle porte sur les signaux physiologiques et les mouvements recueillis par notre souris. Son caractère obligatoire dépend du contexte de déploiement ; le document examine la liste CNIL et les critères applicables.

**Conservation retenue :** historique sur le PC de l’utilisateur pendant la durée du suivi, avec suppression possible à tout moment et prévue à la fin du suivi, après possibilité d’export. Ce principe s’inspire des historiques de montres connectées ; ce n’est pas une durée légale universelle. La durée des signaux bruts et diagnostics doit être justifiée séparément. **La suppression et la clôture du suivi restent à développer et tester** : la passerelle actuelle ajoute les données au CSV sans purge automatique.

## Destination médicale et réglementation

Le dossier décrit un prototype pédagogique, sans mise sur le marché médicale ni certification démontrée. **Deux fonctions futures sont retenues** : suivi des indicateurs et de leurs tendances ET estimation personnalisée du risque de complications cardiovasculaires lié au stress et à la sédentarité. L’utilisateur choisit et paie sa souris dans l’hypothèse B2C, avec partage possible au médecin. Le score reste à développer et valider.

La **classe probable IIa est l’hypothèse du TP**, règle 11, pour un suivi physiologique de routine et un score informant la prévention sans piloter seul le diagnostic ou le traitement. Cette hypothèse doit être confrontée aux décisions réellement prises et à leurs conséquences : IIb pour une détérioration grave ou une intervention chirurgicale, III pour un décès ou une détérioration irréversible lorsque les critères s’appliquent. Les scénarios G3 ne sont pas écartés. Une mention de limites ou un usage non urgent ne suffisent pas à justifier IIa. Le rôle du matériel reste à préciser. Sous l’hypothèse IIa, un organisme notifié intervient dans l’évaluation de conformité.

Le nouvel onglet **Réglementation** relie chacun des 22 risques aux exigences à examiner, à son application au projet et à la vérification attendue. Deux pages du PDF reprennent la qualification et cette correspondance. Les références et associations sont dans [reglementation.json](sources/reglementation.json), commun aux générateurs. Ce rapprochement ne constitue pas une preuve de conformité ni un inventaire exhaustif de toutes les obligations de commercialisation.

**La classe réglementaire ne se calcule pas avec la matrice G × P du TP.** Quatorze scénarios médicaux passent à G3 conservatrice : un retard de prise en charge peut avoir des conséquences graves non exclues par le périmètre. Cette cotation n’est ni une incidence mesurée ni une décision de classification. L’AIPD demeure séparée : le RGPD concerne le traitement des données, indépendamment de la classe médicale. ISO 14971 est une norme de méthode, distincte du règlement.

## Résultat de l'exercice

22 scénarios : 15 techniques, 5 d'utilisation et 2 de cybersécurité. Avant les mesures proposées : 20 élevés et 2 moyens. Après mesures, la **cible pédagogique** est de 19 moyens et 3 faibles. Plusieurs scénarios partagent des causes : ces comptes ne mesurent pas des événements indépendants.

Ces valeurs résiduelles supposent que les mesures sont réalisées et vérifiées. **Le prototype assemblé n'est pas validé.** Les cinq scénarios physiques graves et les quatorze scénarios médicaux réévalués restent moyens dans les cibles ; seuls 6, 7 et 9 ont une cible faible. Leur acceptation réelle reste différée ; le bénéfice clinique n'est pas démontré. Les probabilités sont des hypothèses argumentées, pas des fréquences mesurées.

Le TP M3-1 a été réaligné sur le même objectif cardiovasculaire. Le suivi de tendances n’est pas une alerte d’urgence ; les indicateurs et leur valeur prédictive restent à valider. Le firmware R3 actuel acquiert des signaux ; il ne réalise pas cette fonction médicale. Les plans, pièces 3D et logiciels restent dans le dépôt de la souris.

## Sources et vérification

- Référence du projet examinée : [`b7625705741e973cda2934f0b328ea03531148f6`](https://github.com/lebretyves/TP4-IoT-Autonomie/tree/b7625705741e973cda2934f0b328ea03531148f6), branche `cas-g-choisi`, le 16 octobre 2026.
- Ajouts et AIPD : revue de la référence [`f76c7e4`](https://github.com/lebretyves/TP4-IoT-Autonomie/tree/f76c7e4bd4bdb517066562b716aee0732e4f6341/variantes/04_veille_R3), le 16 octobre 2026.
- [Sujet original](supports/TP_M3_2_Analyse_risques_etudiant.pdf) et [modèle Excel original](supports/TP_M3_2_Analyse_risques.xlsx), conservés sans modification.
- [Données, justifications et liens](sources/risques.json), utilisés par les deux générateurs.
- [Contrôles des livrables](analyses/m3/verification_livrables.json) : formules et plages étendues, résultats calculés, complétude, listes, couleurs, empreintes des supports et liens des PDF. Calculs et changements d’entrée vérifiés avec artifact-tool ; recalcul natif Microsoft Excel en lecture seule le 19 octobre : 22 risques, 20 élevés avant mesures et 19 moyens dans les cibles confirmés. Le rapport daté se trouve dans `analyses/m3/verification_excel_natif.json`.

La mise en commun avec la classe reste à faire. Aucune contribution d'autres équipes ni aucun essai matériel n'est présenté comme réalisé.

## Régénération

`sources/remplir_classeur.mjs` utilise Node.js et `@oai/artifact-tool` du runtime Codex. `sources/generer_pdf.py` utilise Python, ReportLab, PyMuPDF et les polices Arial de Windows. Ces deux scripts lisent `sources/risques.json`. `sources/generer_aipd.py` produit l’analyse d’impact avec ReportLab. Les livrables sont dans `analyses/m3/`, les aperçus dans `tmp/`, exclu du dépôt. Le vérificateur lit le classeur avec openpyxl.

```powershell
node sources/remplir_classeur.mjs
python sources/generer_pdf.py
python sources/generer_aipd.py
python sources/verifier_livrables.py
```

Les contrôles sont documentaires et numériques ; ils ne remplacent pas les essais électriques, ergonomiques, cutanés, cliniques et de sécurité des données décrits dans le classeur.
