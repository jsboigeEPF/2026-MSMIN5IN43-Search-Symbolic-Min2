# Catalogue des sujets 2026-2027 — IA exploratoire et symbolique

Ce catalogue est propre à la promotion **MSMIN5IN43 2026-2027 (EPF, groupes Min1 et Min2)**. Il a été construit en trois temps : (1) compilation des sujets donnés aux promotions précédentes de ce cours et des cours voisins (EPF, ECE, EPITA) ; (2) retrait des sujets déjà traités par des groupes d'étudiants — voir [l'historique](HISTORIQUE-SUJETS.md) ; (3) complément par des sujets nouveaux. Aucun sujet du catalogue ne reprend le verrou technique d'un projet déjà rendu, et aucun ne figure au catalogue 2026-2027 du cours MSMIS5IN11 (majeure Ingénierie et santé), qui est un cours distinct.

Chaque fiche donne une difficulté indicative sur 5, des objectifs, les technologies clés et des liens **CoursIA** vers les notebooks du dépôt [jsboige/CoursIA](https://github.com/jsboige/CoursIA) qui servent de point de départ.

> **Exigence commune.** Toute solution produite par un solveur ou une heuristique doit être contrôlée par un **vérificateur indépendant** (une fonction qui recompte les contraintes violées). Comparez toujours votre méthode à une baseline simple (glouton, aléatoire, règle métier).
>
> **Données.** Instances publiques, open data ou générateurs synthétiques documentés uniquement.

## Index

| Code | Sujet | Difficulté |
|---|---|:---:|
| **A** | **Recherche heuristique et planification** | |
| A1 | Blocs glissants et Rush Hour : heuristiques admissibles et bases de motifs | 3/5 |
| A2 | Pathfinding hiérarchique pour mondes ouverts : HPA* et champs de flux | 3/5 |
| A3 | Self-play et MCTS : apprendre un jeu de plateau par auto-affrontement | 4/5 |
| A4 | Planification classique en PDDL : modéliser un domaine, comparer des planificateurs | 3/5 |
| **B** | **Programmation par contraintes et optimisation combinatoire** | |
| B1 | Allocation de fréquences radio : coloration avec preuve d'optimalité | 3/5 |
| B2 | Équilibrage de lignes de production et de flux : le problème du « balancer » | 3/5 |
| B3 | Générateur de grilles à solution unique : synthèse, preuve, calibration | 4/5 |
| B4 | Construire un mini-solveur CSP : propagation, cohérence d'arc, branchement | 4/5 |
| **C** | **Métaheuristiques et calcul évolutionnaire** | |
| C1 | Paysages d'optimisation : caractériser, visualiser, prédire la performance | 3/5 |
| C2 | Métaheuristiques composées et en îlots sur le voyageur de commerce | 4/5 |
| C3 | Neuroévolution : entraîner un réseau sans descente de gradient | 3/5 |
| **D** | **Logique, SAT/SMT et raisonnement** | |
| D1 | Au-delà de SAT : QBF et raisonnement à alternances | 4/5 |
| D2 | Synthèse de programmes par esquisses (program synthesis) | 4/5 |
| D3 | Tester des validateurs avec SMT strings et expressions régulières | 3/5 |
| D4 | Programmation par ensembles de réponses (ASP) avec Clingo | 3/5 |
| **E** | **Web sémantique et graphes de connaissances** | |
| E1 | Data journalism sémantique : vérifier des affirmations en croisant Wikidata | 3/5 |
| E2 | Traçabilité et provenance : RDF-star sur un graphe de connaissances | 3/5 |
| **F** | **Argumentation et raisonnement délibératif** | |
| F1 | Abstract Dialectical Frameworks : au-delà des attaques binaires | 4/5 |
| F2 | Reconstituer une controverse : de la lecture des sources à la base d'arguments interrogeable | 3/5 |
| **G** | **IA hybride : LLM et méthodes symboliques** | |
| G1 | Décodage contraint : forcer un LLM à produire des sorties valides | 3/5 |
| G2 | Apprentissage de règles par programmation logique inductive (ILP) | 4/5 |

---

## A — Recherche heuristique et planification

### A1 — Blocs glissants et Rush Hour : heuristiques admissibles et bases de motifs
**Difficulté : 3/5** · Mots-clés : `A*`, `heuristiques admissibles`, `pattern databases`, `anytime`

Rush Hour et les puzzles de blocs glissants (15-puzzle et variantes) sont des terrains classiques pour comparer des heuristiques : distance de Manhattan, conflits linéaires, bases de motifs, recherche à discrepancy limité. Le groupe implémente plusieurs heuristiques admissibles et mesure leur impact sur le nombre de nœuds explorés et le temps de résolution.
- **Objectifs** : générateur d'instances Rush Hour (grilles de taille paramétrable) ; A* avec au moins trois heuristiques admissibles dont une base de motifs ; courbes nœuds explorés / temps selon la difficulté ; borne inférieure prouvant l'admissibilité de chaque heuristique ; mode anytime (IDA*, LDS) sur les instances les plus dures.
- **Technologies clés** : Python (priorityqueues via `heapq`), `networkx` pour l'analyse, visualisation des fronts d'exploration.
- **CoursIA** : [Search-03-Informed](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-03-Informed.ipynb) · [Search-03b-PatternDatabases](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-03b-PatternDatabases.ipynb) · [Search-03c-LimitedDiscrepancySearch](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-03c-LimitedDiscrepancySearch.ipynb)
- **Références** : Culberson & Schaeffer, *Pattern Databases*, Computational Intelligence, 1998 · Korf, *Linear-space best-first search*, Artif. Intell., 1993 · Helmert, *Exact Heuristics for the Rush Hour Puzzle* (dans Journey Planning, 2003, adapté).

### A2 — Pathfinding hiérarchique pour mondes ouverts : HPA* et champs de flux
**Difficulté : 3/5** · Mots-clés : `A* hiérarchique`, `mondes ouverts`, `flow fields`, `qualité vs coût`

Sur une carte de jeu vidéo, un A* global est trop coûteux quand des centaines d'agents se déplacent. Le groupe compare A* pur, HPA* (décomposition en clusters, abstractions multi-niveaux) et champs de flux (champ de distance partagé par tous les agents vers une même cible), et quantifie le compromis longueur de chemin / temps de calcul.
- **Objectifs** : cartes procédurales ou extraites d'un jeu ouvert (binaire ou tuiles) ; implémentation d'HPA* à deux niveaux et d'un champ de flux ; mesure de la dégradation de qualité de chemin (ratio vs optimal) et du coût par requête ; étude de la mise à jour incrémentale quand un obstacle apparaît.
- **Technologies clés** : Python ou C# ; `networkx` ou implémentation propre ; visualisation animée des chemins.
- **CoursIA** : [Search-03-Informed](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-03-Informed.ipynb) · [Search-03d-WeightedAstar](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-03d-WeightedAstar.ipynb) · [Search-02b-NetworkX](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-02b-NetworkX.ipynb)
- **Références** : Botea, Müller & Schaeffer, *Near Optimal Hierarchical Path-Finding (HPA*)*, JGD, 2004 · Millington & Funge, *Artificial Intelligence for Games*, 3e éd. (bibliothèque du cours).

### A3 — Self-play et MCTS : apprendre un jeu de plateau par auto-affrontement
**Difficulté : 4/5** · Mots-clés : `MCTS`, `self-play`, `alpha-beta`, `évaluation`

Un agent apprend à jouer à un jeu de plateau combinatoire à information complète (Othello, Awalé, Hex ou connect-6 au choix — pas le Puissance 4, déjà traité) en jouant contre lui-même. Le groupe compare MCTS pur, MCTS avec politique apprise légère, et alpha-beta avec évaluation heuristique, puis mesure le niveau atteint (tournoi round-robin entre versions).
- **Objectifs** : moteur de jeu propre avec vérification des règles ; alpha-beta de référence ; MCTS (UCT) puis self-play avec table de transposition ou petite politique ; tournoi automatisé entre agents avec classement Elo ; analyse des coups surprenants et des échecs.
- **Technologies clés** : Python ; `numpy` ; éventuellement un petit réseau (pas de GPU requis).
- **CoursIA** : [Search-06-AdversarialSearch](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-06-AdversarialSearch.ipynb) · [Search-07-MCTS-And-Beyond](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-07-MCTS-And-Beyond.ipynb) · [App-14b-ConnectFour](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Search/App-14b-ConnectFour.ipynb)
- **Références** : Browne et al., *A Survey of Monte Carlo Tree Search Methods*, IEEE TCIAIG, 2012 · Silver et al., *Mastering the game of Go without human knowledge*, Nature, 2017 (lecture).

### A4 — Planification classique en PDDL : modéliser un domaine, comparer des planificateurs
**Difficulté : 3/5** · Mots-clés : `PDDL`, `planificateurs`, `heuristiques de domaine`, `validation de plans`

La planification automatique classique décrit un domaine (actions, préconditions, effets) en PDDL et laisse un planificateur générique trouver la séquence d'actions. Le groupe modélise un domaine réaliste de son choix (robot de service, logistique de colis, missions d'exploration) et compare plusieurs planificateurs.
- **Objectifs** : domaine et problèmes PDDL (au moins 15 actions, 3 problèmes de taille croissante) ; exécution via `unified-planning` d'au moins trois planificateurs (Fast Downward et variantes d'heuristiques) ; comparaison longueur de plan / temps / nœuds ; **validation indépendante des plans** avec un validateur externe (VAL) ou un vérificateur écrit par le groupe.
- **Technologies clés** : Python, `unified-planning`, Fast Downward ; VAL pour la validation.
- **CoursIA** : [Planners-2-PDDL-Basics](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Planners/01-Foundation/Planners-2-PDDL-Basics.ipynb) · [Planners-4-Fast-Downward](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Planners/02-Classical/Planners-4-Fast-Downward.ipynb) · [Planners-6-Domains](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Planners/02-Classical/Planners-6-Domains.ipynb)
- **Références** : Ghallab, Nau & Traverso, *Automated Planning and Acting*, 2016 (bibliothèque du cours) · Howey, Long & Fox, *VAL: Automatic plan verification*, 2004.

---

## B — Programmation par contraintes et optimisation combinatoire

### B1 — Allocation de fréquences radio : coloration avec preuve d'optimalité
**Difficulté : 3/5** · Mots-clés : `coloration de graphes`, `CP-SAT`, `preuve d'optimalité`, `open data`

Des émetteurs proches ne peuvent pas partager une fréquence sans interférer : c'est une coloration de graphe. Le groupe résout des instances réalistes d'allocation de fréquences et va au-delà de « trouver une solution » en **prouvant** le nombre minimal de fréquences (le modèle pour k couleurs est infaisable).
- **Objectifs** : construction du graphe d'interférence à partir de données ouvertes ou d'un modèle de propagation simplifié ; modèle CP-SAT (ou Z3) ; recherche du minimum par dichotomie avec **preuve d'infaisabilité** pour k−1 couleurs ; comparaison avec une heuristique DSATUR et écart à l'optimum ; étude de la symétrie et de ses coupes.
- **Technologies clés** : Python, OR-Tools CP-SAT ou Z3 ; `networkx`.
- **CoursIA** : [App-2-GraphColoring](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-2-GraphColoring.ipynb) · [Z3-11-Graph-Coloring-Python](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SMT/Z3-API/Z3-11-Graph-Coloring-Python.ipynb)
- **Références** : Hale, *Frequency assignment: theory and applications*, Proc. IEEE, 1980 · DSATUR : Brélaz, *New methods to color the vertices of a graph*, CACM, 1979.

### B2 — Équilibrage de lignes de production et de flux : le problème du « balancer »
**Difficulté : 3/5** · Mots-clés : `flot`, `capacité`, `CP-SAT`, `jeu Factorio`

Dans une usine (ou le jeu Factorio), une ligne de production doit équilibrer les débits de ses machines pour qu'aucun poste ne devienne goulot. Le groupe modélise un réseau de production (recettes, vitesses, taux de perte en cas de déséquilibre) et calcule les ratios d'assemblage optimaux, avec variantes sous contraintes (nombre de machines limité, plusieurs produits).
- **Objectifs** : modèle formel (flot avec gains/pertes, éventuellement non linéaire par paliers — linéariser) ; solveur CP-SAT ou programmation linéaire ; générateur d'instances « arbre de production » ; vérificateur indépendant qui simule la ligne et confirme le débit de sortie ; visualisation de la ligne avec goulots annotés.
- **Technologies clés** : Python, OR-Tools (CP-SAT / GLOP), `networkx` ou `graphviz`.
- **CoursIA** : [Frontieres-02-Factorio-Balancer](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part5-Frontieres/Frontieres-02-Factorio-Balancer-Python.ipynb) · [CSP-5-Optimization](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-5-Optimization.ipynb)
- **Références** : Ahuja, Magnanti & Orlin, *Network Flows*, 1993 · documentation du jeu Factorio (ratios d'assemblage) comme source de données de recettes.

### B3 — Générateur de grilles à solution unique : synthèse, preuve, calibration
**Difficulté : 4/5** · Mots-clés : `génération sous contraintes`, `unicité`, `calibration de difficulté`, `SAT`

Résoudre un Sudoku a été traité de nombreuses fois ; le problème inverse — **construire** une grille intéressante — est différent : la grille doit avoir une solution unique, un niveau de difficulté visé et une symétrie éventuelle. Le groupe construit un générateur certifié, pour le Sudoku ou une variante au choix (Kakuro, binairo, Futoshiki).
- **Objectifs** : encodeur SAT/CP du puzzle et de la **contrainte d'unicité** (deux solutions interdites, via clause de blocage itérée) ; algorithme de génération (grille pleine puis retrait guidé) avec preuve d'unicité à chaque retrait ; calibration de difficulté mesurée par un solveur de référence (techniques humaines ou temps de résolution) ; banc d'essai sur 100 grilles générées.
- **Technologies clés** : Python, python-sat ou OR-Tools ; `matplotlib` pour la distribution de difficulté.
- **CoursIA** : [Z3-18-Sudoku-Modes](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SMT/Z3-API/Z3-18-Sudoku-Modes-Python.ipynb) · [App-20-SudokuBenchmark-Python](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/CSP/App-20-SudokuBenchmark-Python.ipynb)
- **Références** : Simonis, *Sudoku as a Constraint Problem*, CP, 2005 · Lin, *Sudoku generator using bitwise operations and fingering* (analyse de la génération), 2012.

### B4 — Construire un mini-solveur CSP : propagation, cohérence d'arc, branchement
**Difficulté : 4/5** · Mots-clés : `cohérence d'arc`, `propagation`, `heuristiques de branchement`, `AC-3`

Au lieu d'utiliser OR-Tools comme une boîte noire, le groupe écrit son propre solveur CSP : représentation des domaines, propagation AC-3, heuristiques de choix de variable et de valeur, backtracking avec apprentissage de conflits léger. Le but est de comprendre ce qui fait la puissance d'un solveur moderne — et de le mesurer.
- **Objectifs** : noyau générique (variables, domaines, contraintes binaires et globales `all_different` et `sum`) ; AC-3 puis propagation à chaque branchement ; heuristiques MRV/degré et valeur la moins contraignante ; comparaison systématique (avec/sans propagation, avec/sans heuristiques) sur N-queens, Sudoku et une instance de coloration ; comparaison finale avec OR-Tools sur les mêmes instances, avec analyse de l'écart.
- **Technologies clés** : Python pur (pas de dépendance solveur) ; banc d'essai reproductible.
- **CoursIA** : [CSP-1-Fundamentals](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb) · [CSP-2-Consistency](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-2-Consistency.ipynb) · [CSP-3-Advanced](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-3-Advanced.ipynb)
- **Références** : Mackworth, *Consistency in Networks of Relations*, Artif. Intell., 1977 · Rossi, van Beek & Walsh, *Handbook of Constraint Programming*, 2006.

---

## C — Métaheuristiques et calcul évolutionnaire

### C1 — Paysages d'optimisation : caractériser, visualiser, prédire la performance
**Difficulté : 3/5** · Mots-clés : `fitness landscape`, `rugosité`, `sélection d'algorithmes`, `benchmarks`

Pourquoi un algorithme génétique domine-t-il sur une instance et échoue-t-il sur la suivante ? Le groupe instrumente des fonctions et instances de benchmark, calcule des indicateurs de paysage (autocorrélation de marche aléatoire, dispersion, dénivelé) et vérifie s'ils prédisent la performance relative de plusieurs métaheuristiques.
- **Objectifs** : banc de fonctions (unimodal, multimodal, combinatoire via TSP et QAP) ; calcul d'au moins quatre indicateurs de paysage ; exécution de 4 à 6 métaheuristiques avec budgets égaux et répétitions ; corrélation indicateurs ↔ rang de performance ; rapport honnête sur les cas où la prédiction échoue.
- **Technologies clés** : Python, `numpy`, `scipy.stats` ; visualisation 3D et coupes de paysage.
- **CoursIA** : [MGS-15-LandscapeAnalysis](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part4-Metaheuristics/MGS-15-LandscapeAnalysis.ipynb) · [MGS-08-LandscapeExplorer](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part4-Metaheuristics/MGS-08-LandscapeExplorer.ipynb) · [Search-11c-Empirical-Algorithm-Selection](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-11c-Empirical-Algorithm-Selection.ipynb)
- **Références** : Pitzer & Affenzeller, *A Comprehensive Survey on Fitness Landscape Analysis* (Recent Advances in Intelligent Engineering Systems, 2012) · Muñoz, Kirley & Halgamuge, *A meta-learning prediction model of algorithm performance*, Inf. Sci., 2015.

### C2 — Métaheuristiques composées et en îlots sur le voyageur de commerce
**Difficulté : 4/5** · Mots-clés : `TSP`, `îlots`, `mémétique`, `composition`

Les métaheuristiques « pures » (recuit, génétique) sont souvent battues par des **compositions** : mémétiques (évolution + recherche locale), îlots avec migration, restarts adaptatifs. Le groupe construit un cadre de composition et l'évalue rigoureusement sur des instances TSP publiques. Le sujet n'est pas « résoudre un VRP » (traité) mais mesurer ce que la composition apporte.
- **Objectifs** : implémentation propre de recuit, génétique et recherche locale 2-opt/Or-opt ; composition en îlots (topologie et fréquence de migration paramétrables) ; étude d'abaque budget vs qualité (gap vers l'optimal connu des instances TSPLIB) ; analyse de diversité dans les îlots ; effet du restart.
- **Technologies clés** : Python, `numpy` ; instances TSPLIB ; exécutions multi-seeds.
- **CoursIA** : [MGS-04-Islands](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part4-Metaheuristics/MGS-04-Islands.ipynb) · [MGS-05-CompoundMetaheuristics](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part4-Metaheuristics/MGS-05-CompoundMetaheuristics.ipynb) · [App-13-TSP-Metaheuristics](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Applications/Hybrid/App-13-TSP-Metaheuristics.ipynb)
- **Références** : Reinelt, *TSPLIB — a traveling salesman problem library*, ORSA J. Comput., 1991 · Moscato, *On evolution, search, optimization, GAs and martial arts* (mémétiques), Caltech memo, 1989.

### C3 — Neuroévolution : entraîner un réseau sans descente de gradient
**Difficulté : 3/5** · Mots-clés : `stratégies d'évolution`, `CMA-ES`, `cart-pole`, `sans gradient`

Entraîner les poids d'un petit réseau de neurones par évolution (stratégies d'évolution, CMA-ES sur les poids) au lieu de la rétropropagation : le groupe compare les deux régimes sur des tâches de contrôle simple (cart-pole, luni-lander) et discute quand l'approche sans gradient reste compétitive (réseaux petits, récompenses éparses, non-différenciable).
- **Objectifs** : environnement `gymnasium` au choix ; réseau fixe (1-2 couches) ; optimisation des poids par (a) algorithme génétique simple, (b) CMA-ES, (c) rétropropagation (PPO de Stable-Baselines3) ; courbes d'apprentissage multi-seeds ; test de robustesse en récompense éparse ; limites quand la taille du réseau croît.
- **Technologies clés** : Python, `gymnasium`, `cma`, Stable-Baselines3 pour la baseline.
- **CoursIA** : [Search-05-GeneticAlgorithms](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part1-Foundations/Search-05-GeneticAlgorithms.ipynb) · [RL-01-Premiers-Pas-Stable-Baselines3](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/RL/RL-01-Premiers-Pas-Stable-Baselines3-Python.ipynb)
- **Références** : Salimans et al., *Evolution Strategies as a Scalable Alternative to RL*, arXiv:1703.03864 · Such et al., *Deep Neuroevolution: Genetic Algorithms Are a Competitive Alternative*, arXiv:1712.06567.

---

## D — Logique, SAT/SMT et raisonnement

### D1 — Au-delà de SAT : QBF et raisonnement à alternances
**Difficulté : 4/5** · Mots-clés : `QBF`, `PSPACE`, `alternances`, `jeux à deux`

La logique booléenne quantifiée (QBF) étend SAT avec des quantificateurs existentiels et universels : elle capture des problèmes PSPACE comme les jeux à deux tours (« existe-t-il un coup tel que pour toute riposte, existe-t-il... »). Le groupe encode des problèmes réels en QBF (planification adversariale, vérification interactive, jeux) et explore les solveurs QBF.
- **Objectifs** : comprendre les prénexes QBF et les preuves Q-resolution ; encoder au moins deux problèmes (ex. : jeu de tic-tac-toe généralisé, éviter un obstacle avec adversaire, model checking borné d'un système réactif) ; exécution avec un solveur QBF (DepQBF, CAQE, Qute) ; comparaison avec un encodage SAT équivalent quand il existe ; limites de passage à l'échelle selon le nombre d'alternances.
- **Technologies clés** : Python, solveur QBF via DIMACS ou bindings ; génération de QDIMACS.
- **CoursIA** : [Tweety-03-QBF-CSharp](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-03-QBF-CSharp.ipynb) · [Z3-01-Introduction-Python](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SMT/Z3-API/Z3-01-Introduction-Python.ipynb)
- **Références** : Kleine Büning & Bubeck, *Theory of Quantified Boolean Formulas*, Handbook of Satisfiability, 2009 · Shukla, Biere, Seidl, *A Survey of Applications of QBF*, 2019.

### D2 — Synthèse de programmes par esquisses (program synthesis)
**Difficulté : 4/5** · Mots-clés : `synthèse`, `CEGIS`, `esquisses`, `Rosette`

Au lieu d'écrire un programme, on écrit une **esquisse** (squelette avec trous) et une spécification (exemples entrée/sortie ou assertion), et le solveur complète les trous. Le groupe explore la synthèse counterexample-guided (CEGIS) sur des tâches concrètes : complétion de fonctions simples, optimisation d'expressions, puzzles de transformation de listes.
- **Objectifs** : comprendre CEGIS (boucle synthèse/contre-exemple) ; résoudre au moins trois tâches de synthèse avec Rosette (Racket) ou CrossHair/Sygus côté Python ; mesurer le coût selon la taille des trous ; une tâche « utile » au choix (génération de mutations de code pour tests, complétion d'expressions de requêtes) ; comparaison avec ce qu'un LLM produit sur les mêmes trous (le LLM propose, le vérificateur tranche).
- **Technologies clés** : Racket + Rosette (recommandé) ou Python + Z3 ; tests de propriétés.
- **CoursIA** : [Z3-05-Quantifiers-Proofs-Python](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SMT/Z3-API/Z3-05-Quantifiers-Proofs-Python.ipynb) · [SL-14-AIFeynman-Discover-Equations](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SymbolicLearning/SL-14-AIFeynman-Discover-Equations.ipynb)
- **Références** : Solar-Lezama, *Program Synthesis by Sketching*, MIT Press, 2008 · Alur et al., *Syntax-Guided Synthesis (SyGuS)*, 2015.

### D3 — Tester des validateurs avec SMT strings et expressions régulières
**Difficulté : 3/5** · Mots-clés : `SMT strings`, `regex`, `génération de tests`, `sécurité`

Les validateurs (emails, identifiants, plaque d'immatriculation, numéro de sécurité sociale, format de protocole) se spécifient naturellement en logique avec théorie des chaînes. Le groupe écrit des spécifications déclaratives et génère automatiquement des entrées valides et **invalides** pour tester de vraies implémentations (regex en production, parseurs).
- **Objectifs** : au moins quatre spécifications en Z3 strings (avec longueur, contient, regex) ; génération d'entrées satisfaisant / violant la spécification ; harness de test qui confronte une regex ou un parseur réel aux entrées générées ; rapport des divergences trouvées (bugs de validation) ; discussion des limites de la théorie strings (décidabilité, complexité).
- **Technologies clés** : Python, Z3 (théorie strings), module `re` comme cible.
- **CoursIA** : [Z3-04-Strings-Regex-Python](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SMT/Z3-API/Z3-04-Strings-Regex-Python.ipynb) · [Z3-03-Tactics-Python](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SMT/Z3-API/Z3-03-Tactics-Python.ipynb)
- **Références** : Czerwinski et al., *Strings in SMT* (théorie des chaînes), 2021 · documentation Z3 strings.

### D4 — Programmation par ensembles de réponses (ASP) avec Clingo
**Difficulté : 3/5** · Mots-clés : `ASP`, `Clingo`, `ensembles stables`, `déclaratif`

L'ASP (Answer Set Programming) est un paradigme déclaratif différent de SAT et de CP : on décrit le problème par des règles logiques et le solveur énumère les « ensembles de réponses » (solutions). Le groupe apprend l'ASP sur des problèmes concrets (planification d'horaires légers, configuration, raisonnement sur ontologies simples) et le compare au CP.
- **Objectifs** : maîtriser la syntaxe Clingo (règles, contraintes, optimisation `#minimize`) ; modéliser au moins deux problèmes (ex. : emploi du temps d'un tournoi interne, sélection de projets sous budget, raisonnement d'exceptions) ; comparaison de modélisation et de performance avec CP-SAT sur les mêmes instances ; rapport sur ce que chaque paradigme exprime facilement.
- **Technologies clés** : Clingo (Python bindings), OR-Tools pour la comparaison.
- **CoursIA** : [Tweety-02-Basic-Logics-Python](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-02-Basic-Logics-Python.ipynb) (logiques par défaut, cousin conceptuel) · [CSP-1-Fundamentals](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/Search/Part2-CSP/CSP-1-Fundamentals.ipynb)
- **Références** : Gelfond & Kahl, *Knowledge Representation, Reasoning, and the Design of Intelligent Agents*, 2014 · Potassco : [https://potassco.org](https://potassco.org).

---

## E — Web sémantique et graphes de connaissances

### E1 — Data journalism sémantique : vérifier des affirmations en croisant Wikidata
**Difficulté : 3/5** · Mots-clés : `SPARQL`, `Wikidata`, `open data`, `fact-checking de données`

Les affirmations chiffrées des médias (« la moitié des villes de plus de X habitants sont... ») se vérifient en croisant des sources ouvertes. Le groupe construit un pipeline qui interroge Wikidata (et éventuellement DBpedia ou data.gouv) en SPARQL pour confirmer ou infirmer une liste d'affirmations factuelles, et documente la **fiabilité des données** elles-mêmes.
- **Objectifs** : requêtes SPARQL fédérées ou multi-étapes sur au moins 8 affirmations chiffrées réelles (sources citées) ; gestion des données manquantes et des qualifications Wikidata (dates, périmètres) ; pour chaque affirmation : verdict, requête, incertitudes ; étude d'un cas où Wikidata se contredit (historique de révisions) ; notebook reproductible (cache des requêtes).
- **Technologies clés** : Python, `SPARQLWrapper` ou service WDQS direct, `pandas`.
- **CoursIA** : [SW-4b-Python-SPARQL](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SemanticWeb/SW-4b-Python-SPARQL.ipynb) · [SW-5b-Python-LinkedData](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SemanticWeb/SW-5b-Python-LinkedData.ipynb)
- **Références** : Wikidata Query Service ([https://query.wikidata.org](https://query.wikidata.org)) · Erxleben et al., *Introducing Wikidata to the Linked Data Web*, ISWC, 2014.

### E2 — Traçabilité et provenance : RDF-star sur un graphe de connaissances
**Difficulté : 3/5** · Mots-clés : `RDF-star`, `provenance`, `confiance`, `annotation`

Dans un graphe de connaissances, savoir **d'où vient** un triplet (quelle source, quelle date, quel niveau de confiance) est aussi important que le triplet lui-même. RDF-star permet d'annoter les triplets. Le groupe construit un petit graphe multi-sources (ex. : films et récompenses depuis Wikipédia et une API) et raisonne sur la provenance.
- **Objectifs** : moissonnage de 2 à 3 sources publiques sur un même sujet ; graphe RDF-star où chaque triplet porte source, date et confiance ; requêtes SPARQL-star (« quelles affirmations ne sont soutenues que par une source ? », « quels triplets ont changé ? ») ; détection de contradictions inter-sources et résolution par règle de confiance documentée ; visualisation du graphe annoté.
- **Technologies clés** : Python, `rdflib` (support RDF-star), SPARQL-star.
- **CoursIA** : [SW-10-Python-RDFStar](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SemanticWeb/SW-10-Python-RDFStar.ipynb) · [SW-11-Python-KnowledgeGraphs](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SemanticWeb/SW-11-Python-KnowledgeGraphs.ipynb)
- **Références** : Hartig & Thompson, *Foundations of SPARQL Update* (RDF-star), W3C Community Report, 2021 · Moreau & Groth, *Provenance: An Introduction to PROV*, Morgan & Claypool, 2013.

---

## F — Argumentation et raisonnement délibératif

### F1 — Abstract Dialectical Frameworks : au-delà des attaques binaires
**Difficulté : 4/5** · Mots-clés : `ADF`, `conditions d'acceptation`, `sémantiques`, `Tweety`

Les frameworks de Dung (déjà étudiés dans ce cours et traités en projet) ne connaissent que l'attaque binaire. Les ADF généralisent : chaque argument porte une **condition d'acceptation** (formule propositionnelle), ce qui permet de représenter le support, l'attaque conjointe et les dépendances complexes. Le groupe implémente les sémantiques ADF et les compare aux sémantiques de Dung.
- **Objectifs** : définition et lecture d'ADF (format ADF syntax de la compétition) ; calcul des sémantiques admises, complètes et préférées par itération d'opérateurs à trois valeurs ; vérification croisée avec l'implémentation de référence (solveur de la compétition ICCMA'23 ou module `arg.adf` de Tweety) ; étude de cas où ADF ≠ AF (support, attaque conjointe) ; passage à l'échelle (arbres de preuve SAT).
- **Technologies clés** : Python (implémentation propre) ; JPype + Tweety ou solveur ADF externe pour la vérification ; SAT solver.
- **CoursIA** : [Tweety-07a-Extended-Frameworks-Python](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Tweety/Tweety-07a-Extended-Frameworks-Python.ipynb) · [Argumentation-03-Dung-AF-Semantics](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Argument_Analysis/Argumentation-03-Dung-AF-Semantics-Python.ipynb)
- **Références** : Brewka, Ellmauthaler, Strass, Thielscher, *Abstract Dialectical Frameworks Revisited*, IJCAI, 2013 · Linsbichler et al., *A Higher-Order Semantics for Abstract Dialectical Frameworks*, 2016.

### F2 — Reconstituer une controverse : de la lecture des sources à la base d'arguments interrogeable
**Difficulté : 3/5** · Mots-clés : `base d'arguments`, `controverse`, `sémantiques de Dung`, `dynamique`

Les moteurs d'argumentation traitent des graphes déjà construits ; le travail difficile est en amont — transformer un corpus documentaire réel en base de propositions, d'arguments et de conflits **fidèle aux sources**. Le groupe reconstitue une controverse scientifique historique (par ex. dérive des continents, miasmes contre germes, origine bactérienne de l'ulcère) et l'analyse formellement.
- **Objectifs** : choix d'une controverse historique documentée (sources ouvertes) ; protocole d'extraction écrit : propositions, arguments pour/contre, relations d'attaque et de soutien, avec grille de décision et double lecture des passages clés (accord entre membres rapporté) ; base formalisée au format propositions/arguments/conflits du carnet 04b ; analyse **calculée** : extensions sous les sémantiques de Dung — quels arguments survivent, la carte confirme-t-elle l'issue historique ? ; dynamique : courbe d'acceptation au fil de l'ajout chronologique des arguments ; limites analysées honnêtement : sous-détermination des sources, angles morts, biais de reconstruction.
- **Technologies clés** : Python, moteur de sémantiques (implémentation propre ou Tweety), visualisation de graphes.
- **CoursIA** : [Argumentation-04b-Knowledge-Base](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Argument_Analysis/Argumentation-04b-Knowledge-Base-Python.ipynb) · [Argumentation-03-Dung-AF-Semantics](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/Argument_Analysis/Argumentation-03-Dung-AF-Semantics-Python.ipynb)
- **Références** : Dung, *On the Acceptability of Arguments*, Artif. Intell., 1995 · Besnard & Hunter, *Elements of Argumentation*, MIT Press, 2008 · Latour, *Science in Action*, 1987 (méthode de suivi des controverses).

À distinguer des traitements 2025 (moteurs de sémantiques, schémas de Walton, détection de sophismes, indexation sémantique d'arguments) : ici le verrou est la **construction fidèle** de la base depuis des sources réelles et son analyse formelle.

---

## G — IA hybride : LLM et méthodes symboliques

### G1 — Décodage contraint : forcer un LLM à produire des sorties valides
**Difficulté : 3/5** · Mots-clés : `grammaires`, `JSON schema`, `décodage guidé`, `validation`

Un LLM qui doit produire du JSON valide, une requête SPARQL correcte ou une ligne de calendrier sans collision échoue une fraction du temps. Le groupe compare les approches pour l'y forcer : prompts simples, sorties structurées, décodage guidé par grammaire (outlines, llama.cpp GBNF, XGrammar), post-validation par parseur ou solveur.
- **Objectifs** : trois tâches à format contraignant (JSON d'un schéma donné, expression d'une requête mini-DSL, configuration respectant des contraintes) ; pipeline de génération avec quatre niveaux de contrainte ; mesure du taux de validité, du coût (tokens, latence) et de la qualité sémantique ; analyse fine : le décodage contraint dégrade-t-il le contenu ? recommandations d'ingénierie.
- **Technologies clés** : Python, `outlines` ou llama.cpp, jsonschema, Z3 pour la tâche contrainte.
- **CoursIA** : [GenAI/Texte/03c_Constrained_Decoding](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/03c_Constrained_Decoding_Python.ipynb) · [GenAI/Texte/03_Structured_Outputs](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/GenAI/Texte/03_Structured_Outputs.ipynb)
- **Références** : Willard & Louf, *Efficient Guided Generation for LLMs* (outlines), arXiv:2307.09702 · documentation XGrammar / GBNF.

### G2 — Apprentissage de règles par programmation logique inductive (ILP)
**Difficulté : 4/5** · Mots-clés : `ILP`, `Popper`, `règles`, `explicabilité`

La programmation logique inductive apprend des **règles symboliques** (clauses) à partir d'exemples positifs et négatifs — un mode d'apprentissage lisible et vérifiable, opposé aux boîtes noires. Le groupe applique un système ILP moderne à des tâches de prédiction de relations et compare aux méthodes numériques.
- **Objectifs** : compréhension du cadre (modes, biais de langage, examples pos/neg) ; exécution de Popper (ou Aleph) sur au moins deux jeux (ex. : family relations, adaptation de données tabulaires discrétisées, arcs de connaissances simples) ; mesure : précision/rappel des règles apprises, taille et lisibilité ; comparaison avec arbre de décision et forêt sur les mêmes données ; discussion : que gagne-t-on en explicabilité, que perd-on en performance.
- **Technologies clés** : Python, Popper (dockerisé ou local), `scikit-learn` pour la baseline.
- **CoursIA** : [SL-4-InductiveLogicProgramming](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SymbolicLearning/SL-4-InductiveLogicProgramming.ipynb) · [SL-6-ModernILP](https://github.com/jsboige/CoursIA/blob/main/MyIA.AI.Notebooks/SymbolicAI/SymbolicLearning/SL-6-ModernILP.ipynb)
- **Références** : Cropper & Dumančić, *Inductive Logic Programming at 30: A New Introduction*, JAR, 2022 · Muggleton, *Inductive Logic Programming*, New Gen. Comput., 1991.
