# 2026 - EPF MSMIN5IN43 - IA exploratoire et symbolique (Min2)

Dépôt de projets du cours **MSMIN5IN43 — Intelligence Artificielle II**, groupe **Min2**, EPF, année 2026-2027. Les projets explorent la recherche heuristique, la planification, la programmation par contraintes, les métaheuristiques, la logique SAT/SMT, le web sémantique, l'argumentation et l'IA hybride.

Le second projet du cours (IA probabiliste, théorie des jeux et machine learning) a son propre dépôt : [jsboigeEPF/2026-MSMIN5IN43-Probas-ML-Min2](https://github.com/jsboigeEPF/2026-MSMIN5IN43-Probas-ML-Min2).

## Calendrier

Le cours compte **8 séances** pour le groupe Min2, du **mercredi 28 octobre 2026** au **11 ou 12 janvier 2027** (dernière séance). Le calendrier précis des séances est annoncé sur Moodle.

| Étape | Date |
|---|---|
| Première séance | Mercredi 28 octobre 2026 |
| Dépôt de la Pull Request finale | **Date à fixer** *(emplacement réservé : JJ/MM/AAAA à HH:MM)* |
| Soutenance et démonstration | **Date à fixer** *(emplacement réservé : lors de la dernière séance, 11 ou 12 janvier 2027 — salle et horaire à préciser)* |

## Démarrage rapide

1. Constituez un groupe — **3 personnes est le format standard**.
2. Choisissez un sujet dans le [catalogue 2026-2027](docs/CATALOGUE.md), puis [réservez-le par une issue](https://github.com/jsboigeEPF/2026-MSMIN5IN43-Search-Symbolic-Min2/issues/new?template=inscription-groupe.yml). Un sujet ne peut être réservé que par un groupe. Reportez aussi votre groupe et votre sujet dans la feuille d'inscription indiquée sur Moodle.
3. Forkez ce dépôt sur le compte d'un membre du groupe.
4. Créez un dossier unique à la racine, nommé `groupe-<nom-court>`.
5. Copiez le contenu de [`template-groupe/`](template-groupe/) dans ce dossier.
6. Travaillez par commits réguliers sans modifier les fichiers des autres groupes.
7. Si le groupe est bloqué, ouvrez tôt une [demande d'accompagnement](https://github.com/jsboigeEPF/2026-MSMIN5IN43-Search-Symbolic-Min2/issues/new?template=demande-accompagnement.yml).
8. Ouvrez une Pull Request vers ce dépôt avant la date limite.

Les sujets libres sont possibles, mais doivent être proposés avec le [formulaire dédié](https://github.com/jsboigeEPF/2026-MSMIN5IN43-Search-Symbolic-Min2/issues/new?template=proposition-sujet.yml) et validés avant développement. Consultez [l'historique](docs/HISTORIQUE-SUJETS.md) avant de proposer : un sujet proche d'un thème déjà réalisé doit expliciter son verrou technique distinct.

## Documents de référence

- [Catalogue des sujets 2026-2027](docs/CATALOGUE.md)
- [Guide de réalisation et de soumission](docs/GUIDE-SOUMISSION.md)
- [Modalités d'évaluation](docs/EVALUATION.md)
- [Sujets réalisés lors des promotions précédentes](docs/HISTORIQUE-SUJETS.md)
- [Gabarit de dossier de groupe](template-groupe/README.md)
- [Charte pour les agents de code](AGENTS.md)

## Axes du catalogue

| Code | Axe |
|---|---|
| A | Recherche heuristique et planification |
| B | Programmation par contraintes et optimisation combinatoire |
| C | Métaheuristiques et calcul évolutionnaire |
| D | Logique, SAT/SMT et raisonnement |
| E | Web sémantique et graphes de connaissances |
| F | Argumentation et raisonnement délibératif |
| G | IA hybride : LLM et méthodes symboliques |

## Livrables attendus

Chaque groupe fournit au minimum :

- le code source et des instructions reproductibles ;
- un `README.md` complet ;
- un notebook explicatif avec analyses et visualisations **ou** une interface/démonstration fonctionnelle ;
- un vérificateur indépendant des solutions produites et des tests adaptés au projet ;
- les slides de soutenance ;
- un fichier `.env.example` sans valeur secrète si le projet utilise des services externes ;
- un historique Git montrant la participation des membres.

Les jeux de données téléchargés, environnements virtuels, fichiers `.env` et clés API ne doivent jamais être commités.

## Ressources du cours

- **Notebooks** : le dépôt public [CoursIA](https://github.com/jsboige/CoursIA), en particulier les séries [Search](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/Search) (recherche, CSP, métaheuristiques) et [SymbolicAI](https://github.com/jsboige/CoursIA/tree/main/MyIA.AI.Notebooks/SymbolicAI) (planification, SAT/SMT avec Z3, web sémantique, argumentation avec Tweety, apprentissage symbolique). Les fiches du catalogue y renvoient. Un projet ne se limite pas à recopier un notebook : il construit un démonstrateur, mesure ses résultats et documente ses choix.
- **Bibliographie** : la bibliothèque du cours (lien en lecture seule sur Moodle). Les ouvrages ne doivent pas être recopiés dans le dépôt ; citez-les.

## Licence

Le contenu pédagogique de ce dépôt est distribué sous [licence MIT](LICENSE). Chaque groupe reste responsable des licences des modèles, données, bibliothèques et médias qu'il utilise.
