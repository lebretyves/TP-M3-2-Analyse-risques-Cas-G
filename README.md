# TP M3-2 — Analyse des risques — Équipe 2

Analyse de la **souris ergonomique P4 avec une batterie unique de 1 500 mAh**, fondée sur la [branche cas-g-choisi](https://github.com/lebretyves/TP4-IoT-Autonomie/tree/cas-g-choisi).

## Livrables

- **[Excel complété : analyse_risques_eq02.xlsx](analyses/m3/analyse_risques_eq02.xlsx)** — fichier à déposer, conforme au chemin demandé dans le sujet.
- **[PDF explicatif du TP](analyses/m3/TP_M3_2_analyse_risques_cas_G.pdf)** — réponses aux six questions, chaînes des 22 risques et décision sur les risques résiduels.
- **[Analyse d’impact adaptée à la souris](analyses/m3/analyse_impact_souris_cas_G.pdf)** — document séparé sur les données, les droits, les accès et la conservation. Version préparatoire : mesures, essais et gouvernance à compléter.

Le classeur conserve les quatre onglets d'origine et les seuils du cours. Les formules, listes de cotation et couleurs couvrent les 22 lignes. Les dix premières lignes restent identiques. **Suivi et sources** documente les risques initiaux (sources S0 à S8) ; **Failles et preuves** décrit les faiblesses, preuves, essais et décisions de relecture des ajouts 11 à 22 (sources C0 à C11).

## Analyse de risques et analyse d’impact

L’analyse de risques du dispositif traite les pannes et erreurs pouvant causer un dommage : brûlure, douleur aggravée ou suivi inadapté, par exemple. L’AIPD examine la nécessité de la collecte, les droits et les effets sur la vie privée. Elle porte sur les signaux physiologiques et les mouvements recueillis par notre souris. Son caractère obligatoire dépend du contexte de déploiement ; le document examine la liste CNIL et les critères applicables.

**Conservation retenue :** historique sur le PC de l’utilisateur pendant la durée du suivi, avec suppression possible à tout moment et prévue à la fin du suivi, après possibilité d’export. Ce principe s’inspire des historiques de montres connectées ; ce n’est pas une durée légale universelle. La durée des signaux bruts et diagnostics doit être justifiée séparément. **La suppression et la clôture du suivi restent à développer et tester** : la passerelle actuelle ajoute les données au CSV sans purge automatique.

## Résultat de l'exercice

22 scénarios : 15 techniques, 5 d'utilisation et 2 de cybersécurité. Avant les mesures proposées : 6 élevés et 16 moyens. Après mesures, la **cible pédagogique** est de 5 moyens et 17 faibles. Plusieurs scénarios partagent des causes : ces comptes ne mesurent pas des événements indépendants.

Ces valeurs résiduelles supposent que les mesures sont réalisées et vérifiées. **Le prototype assemblé n'est pas validé.** Les risques 2, 3, 11, 12 et 20 restent moyens dans les cibles. Leur acceptation réelle reste différée ; le bénéfice clinique n'est pas démontré. Les probabilités sont des hypothèses argumentées, pas des fréquences mesurées.

L'usage médical envisagé reste celui du TP M3-1 : aider le professionnel à adapter la prise en charge de TMS. Le firmware R3 actuel acquiert des signaux ; il ne réalise pas cette fonction médicale. Les plans, pièces 3D et logiciels restent dans le dépôt de la souris.

## Sources et vérification

- Référence du projet examinée : [`b7625705741e973cda2934f0b328ea03531148f6`](https://github.com/lebretyves/TP4-IoT-Autonomie/tree/b7625705741e973cda2934f0b328ea03531148f6), branche `cas-g-choisi`, le 16 octobre 2026.
- Ajouts et AIPD : revue de la référence [`f76c7e4`](https://github.com/lebretyves/TP4-IoT-Autonomie/tree/f76c7e4bd4bdb517066562b716aee0732e4f6341/variantes/04_veille_R3), le 16 octobre 2026.
- [Sujet original](supports/TP_M3_2_Analyse_risques_etudiant.pdf) et [modèle Excel original](supports/TP_M3_2_Analyse_risques.xlsx), conservés sans modification.
- [Données, justifications et liens](sources/risques.json), utilisés par les deux générateurs.
- [Contrôles des livrables](analyses/m3/verification_livrables.json) : formules et plages étendues, résultats calculés, complétude, listes, couleurs, empreintes des supports et liens des PDF. Calculs et changements d’entrée vérifiés avec artifact-tool ; Excel natif non testé.

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
