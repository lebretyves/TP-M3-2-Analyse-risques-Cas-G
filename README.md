# TP M3-2 — Analyse des risques — Équipe 2

Analyse de la **souris ergonomique P4 avec une batterie unique de 1 500 mAh**, fondée sur la [branche cas-g-choisi](https://github.com/lebretyves/TP4-IoT-Autonomie/tree/cas-g-choisi).

## Livrables

- **[Excel complété : analyse_risques_eq02.xlsx](analyses/m3/analyse_risques_eq02.xlsx)** — fichier à déposer, conforme au chemin demandé dans le sujet.
- **[PDF explicatif du TP](analyses/m3/TP_M3_2_analyse_risques_cas_G.pdf)** — réponses aux six questions, chaînes des dix risques et décision sur les risques résiduels.

Le classeur conserve les quatre onglets d'origine, les formules, les listes de cotation et les seuils du cours. Le cas G est ajouté à la liste des cas. L'onglet **Suivi et sources** distingue les fonctions présentes dans le dépôt des mesures et essais encore à réaliser.

## Résultat de l'exercice

10 risques : 5 techniques, 3 d'utilisation et 2 de cybersécurité. Avant les mesures proposées : 3 élevés et 7 moyens. Après mesures, la **cible pédagogique** est de 2 moyens et 8 faibles.

Ces valeurs résiduelles supposent que les mesures sont réalisées et vérifiées. **Le prototype assemblé n'est pas validé.** Les deux risques moyens concernent la batterie et les erreurs d'alimentation. Leur acceptation réelle reste différée ; le bénéfice clinique n'est pas démontré. Les probabilités sont des hypothèses argumentées, pas des fréquences mesurées.

L'usage médical envisagé reste celui du TP M3-1 : aider le professionnel à adapter la prise en charge de TMS. Le firmware R3 actuel acquiert des signaux ; il ne réalise pas cette fonction médicale. Les plans, pièces 3D et logiciels restent dans le dépôt de la souris.

## Sources et vérification

- Référence du projet examinée : [`b7625705741e973cda2934f0b328ea03531148f6`](https://github.com/lebretyves/TP4-IoT-Autonomie/tree/b7625705741e973cda2934f0b328ea03531148f6), branche `cas-g-choisi`, le 16 octobre 2026.
- [Sujet original](supports/TP_M3_2_Analyse_risques_etudiant.pdf) et [modèle Excel original](supports/TP_M3_2_Analyse_risques.xlsx), conservés sans modification.
- [Données, justifications et liens](sources/risques.json), utilisés par les deux générateurs.
- [Contrôles des livrables](analyses/m3/verification_livrables.json) : formules conservées, résultats calculés, complétude, empreintes des supports et liens du PDF.

La mise en commun avec la classe reste à faire. Aucune contribution d'autres équipes ni aucun essai matériel n'est présenté comme réalisé.

## Régénération

`sources/remplir_classeur.mjs` utilise Node.js et `@oai/artifact-tool` du runtime Codex. `sources/generer_pdf.py` utilise Python, ReportLab, PyMuPDF et les polices Arial de Windows. Les deux scripts lisent `sources/risques.json` et écrivent dans `analyses/m3/`. Les aperçus sont placés dans `tmp/`, exclu du dépôt.

```powershell
node sources/remplir_classeur.mjs
python sources/generer_pdf.py
python sources/verifier_livrables.py
```

Les contrôles sont documentaires et numériques ; ils ne remplacent pas les essais électriques, ergonomiques, cutanés, cliniques et de sécurité des données décrits dans le classeur.
