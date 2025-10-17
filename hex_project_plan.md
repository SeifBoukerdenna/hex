# Plan de travail - Projet Hex INF8175

**Dates importantes:**
- Remise agent concours: 16 nov 2025
- Remise finale: 4 déc 2025

---

## Semaine 1: Setup et compréhension de base (5-8h)

### Jour 1-2: Installation et premiers tests
- [x] Cloner/télécharger les fichiers du projet
- [x] Créer environnement virtuel Python 3.11
- [x] Tester que tout marche
- [x] Jouer 3-4 parties complètes moi-même pour comprendre le jeu

- [x] Tester que tout marche:
  ```bash
  python main_hex.py -t human_vs_human
  ```

- [x] Notes sur stratégies observées:
  - Le plus important est de couper les points clés (empêcher les ponts)
  - Le centre du plateau est crucial - contrôler le centre donne plus d'options
  - Créer des "ponts" (deux cases adjacentes vides entre mes pièces) force l'adversaire à jouer 2 coups pour bloquer
  - Jouer trop près des bords limite mes options de connexion
  - Il faut penser en "chemins larges" pas juste une ligne droite
  - Bloquer l'adversaire est aussi important que construire mon propre chemin
  - Les cases en diagonale (qui se touchent par un coin) ne sont PAS connectées! Important pour Hex
  - Quand l'adversaire a un chemin presque complet, il faut absolument le couper
  - Le premier joueur (rouge) semble avoir un léger avantage
  - Une fois qu'un joueur contrôle bien le centre, c'est très dur de le rattraper
  - Difficile de voir tous les chemins possibles mentalement - besoin d'un algo pour ça

- [x] Stratégiques:
  - Former des groupes connectés plutôt que des pièces isolées
  - La distance la plus courte n'est pas toujours le meilleur chemin (peut être facilement bloqué)
  - Occuper les cases qui servent aux deux objectifs (mon chemin + bloquer adversaire) = coups efficaces
  - Les coins du plateau sont moins utiles que les cases centrales

- [x] Tactiques:
  - Certaines formes de placement sont naturellement plus fortes (triangles, losanges)
  - Quand deux chemins sont possibles pour l'adversaire, difficile de les bloquer tous les deux
  - Créer des menaces multiples oblige l'adversaire à choisir quoi défendre

- [x] Difficultés observées:

  - Dur de calculer mentalement si un chemin est vraiment bloqué ou non
  - Facile de rater un chemin alternatif de l'adversaire
  - Vers la fin de partie, le plateau devient complexe à analyser
  - Sans aide visuelle/algo, je rate des coups gagnants évidents


- [x] Questions qui émergent:
  - Comment calculer efficacement le chemin le plus court?
  - Comment évaluer quelle position est "meilleure" objectivement?
  - Est-ce qu'il vaut mieux attaquer ou défendre en début de partie?
  - Y a-t-il des "ouvertures" classiques comme aux échecs?


### Jour 3: Regarder les agents fournis
- [x] Lancer random vs greedy plusieurs fois
  ```bash
  python main_hex.py -t local random_player_hex.py greedy_player_hex.py
  ```
- [x] Observer qui gagne et pourquoi
- [ ] Jouer contre le greedy pour voir son comportement
  ```bash
  python main_hex.py -t human_vs_computer greedy_player_hex.py
  ```
- [x] Notes sur ce qui rend greedy meilleur que random:
  - Greedy (bleu) a gagné en créant un chemin continu de gauche à droite
  - Les pièces bleues forment un groupe CONNECTÉ alors que les rouges sont éparpillées partout
  - Random (rouge) a joué des coups inutiles loin de ses objectifs (top et bottom)
  - Greedy semble suivre un chemin logique - ses pièces sont alignées avec son objectif (left→right)
  - Random a gaspillé des coups en haut du plateau alors qu'il devait connecter haut-bas
  - Greedy occupe une "bande" centrale efficace qui traverse le plateau
  - Les pièces rouges ne forment pas de chemin continu - plusieurs groupes isolés
  - Greedy a probablement calculé le chemin le plus court et joué dessus
  - Random n'a aucune stratégie = coups sans cohérence spatiale
  - La victoire de greedy semble rapide - random n'a même pas eu le temps de former un vrai chemin
  - Greedy joue concentré (toutes ses pièces travaillent ensemble) vs random dispersé
  - On voit clairement que PLANIFIER un chemin > jouer au hasard
  - Greedy ne semble pas bloquer random activement, juste construire son propre chemin
  - Ça suggère que dans Hex, l'offense (construire son chemin) > défense (bloquer)
  - Le greedy a probablement joué proche du centre du plateau (optimal pour shortest path)
  - Random a mis quelques pièces inutiles en périphérie (coins, bords éloignés)
- [x] Questions qui émergent:
  - Est-ce que greedy regarde 1 seul chemin ou adapte si bloqué?
  - Comment greedy calcule-t-il le "shortest path"? (Dijkstra probablement)
  - Est-ce que greedy aurait bloqué si random était plus menaçant?

  **Greedy ne défend PAS:**
  - Il calcule seulement SON chemin le plus court, ignore complètement mes menaces
  - J'ai pu créer un chemin vertical presque complet sans qu'il me bloque
  - Il continue à construire son propre chemin même quand je suis à 1 coup de gagner
  - Aucune notion de "bloquer l'adversaire" dans son algorithme
  - Stratégie purement offensive = grande vulnérabilité

  **Ce que ça révèle:**
  - Un bon agent DOIT évaluer les menaces adverses
  - Besoin de calculer AUSSI le chemin adverse (pas juste le mien)
  - Si adversaire est proche de gagner → jouer défensif devient prioritaire
  - Le greedy bat random car random ne crée pas de menaces cohérentes
  - Mais contre un humain/agent intelligent qui construit un vrai chemin = greedy perd

  **Implication pour mon agent:**
  - Mon heuristique doit considérer: MON chemin + LEUR chemin
  - Si leur chemin est plus court que le mien → BLOQUER en urgence
  - Équilibrer offense/défense selon situation
  - Peut-être chercher des coups qui font les DEUX (avancer + bloquer)

  **Test effectué:**
  - J'ai construit un chemin vertical évident
  - Greedy a continué horizontalement sans réagir
  - J'ai gagné facilement en complétant mon chemin
  - Victoire humain vs greedy confirmée grâce à sa faiblesse défensive

**Stratégie gagnante contre greedy découverte:**
1. Construire un chemin direct et rapide (vertical pour rouge)
2. Ignorer le greedy tant qu'il ne bloque pas ton chemin
3. Compléter ton chemin avant qu'il ne complète le sien
4. Victoire facile car il ne défendra jamais

**Pattern du greedy observé:**
- Greedy joue TOUJOURS une ligne diagonale quasi-droite à travers le centre
- Il semble calculer le chemin optimal au DÉBUT et le suit aveuglément
- Ne dévie JAMAIS de son plan même si des opportunités/menaces apparaissent
- Ses pièces forment une "échelle" connectée (chaque pièce touche la suivante)
- Joue très prévisible = facile à contrer une fois qu'on connaît sa stratégie

**Quand greedy est-il efficace?**
- Contre des adversaires désorganisés (random)
- En début de partie quand le plateau est vide
- Quand personne ne le bloque activement
- Sa vitesse de connexion est impressionnante si non contesté

**Quand greedy échoue-t-il?**
- Dès qu'on bloque son chemin principal, il ne sait pas adapter
- Il ne crée pas de plan B si son chemin est coupé
- Vulnérable à une stratégie "barrage" (bloquer sa diagonale)
- Ne profite pas des erreurs adverses

**Tactiques testées contre greedy:**
- Bloquer sa diagonale centrale = il ralentit beaucoup
- Jouer directement sur son chemin prévu = il doit contourner
- Créer mon propre chemin pendant qu'il hésite = victoire facile
- Le "zigzag" vertical bat sa ligne droite horizontale

**Leçons pour mon agent:**
- Avoir UN plan c'est bien, mais savoir ADAPTER c'est mieux
- Calculer plusieurs chemins alternatifs (pas juste le plus court)
- Réévaluer la situation après CHAQUE coup adverse
- Implémenter une "alerte rouge" si l'adversaire est proche de gagner
- Penser aux coups "double fonction" (avancer ET bloquer simultanément)

**Idées d'amélioration vs greedy:**
- Ajouter un système de détection de menace (combien de coups pour adversaire gagner?)
- Si menace imminente (1-2 coups) → mode défensif prioritaire
- Sinon → construire efficacement comme greedy
- Bonus: identifier les cases "critiques" qui bloquent plusieurs chemins adverses


**Prochaine étape importante:**
Ton agent devra être **meilleur** que greedy en ajoutant la dimension défensive. Une heuristique simple pourrait être:

```python
score = (longueur_chemin_adverse - longueur_mon_chemin)
# Positif = je gagne, négatif = je perds
```

### Jour 4: Lecture du code (important!)
- [ ] Lire `board_hex.py` - comprendre la structure du plateau
  - Comment sont stockées les pièces?
  - Comment récupérer les voisins?
- [ ] Lire `player_hex.py` - voir ce que je dois hériter
- [ ] Lire `game_state_hex.py` - **LE PLUS IMPORTANT**
  - `get_possible_light_actions()` → actions possibles
  - `apply_action()` → simuler un coup
  - `compute_scores()` → vérifier victoire
  - `get_neighbours()` → cases adjacentes
- [ ] Notes/questions sur le code:
  -
  -
  -

### Jour 5: Analyse approfondie du greedy
- [ ] Ouvrir `greedy_player_hex.py` et annoter chaque partie
- [ ] Comprendre l'algo de Dijkstra utilisé
- [ ] Pourquoi il joue proche du centre?
- [ ] Schéma de l'algorithme sur papier:
  -
  -

---

## Semaine 2: Premier agent fonctionnel (8-12h)

### Jour 1-2: Agent version 0.1 - "juste qqch qui marche"
- [ ] Copier la structure de `random_player_hex.py`
- [ ] Créer `my_player.py` avec classe MyPlayer
- [ ] Implémenter compute_action() version simple:
  ```python
  def compute_action(self, current_state, **kwargs):
      actions = list(current_state.get_possible_light_actions())
      # TODO: choisir intelligemment au lieu d'aléatoire
      return random.choice(actions)
  ```
- [ ] Tester que ça compile et joue sans crash
- [ ] Résultats des tests:
  - vs random:
  - vs greedy:

### Jour 3-4: Première heuristique
- [ ] Brainstorm: qu'est-ce qui fait une bonne position?
  - Idée 1:
  - Idée 2:
  - Idée 3:
- [ ] Implémenter fonction `evaluate(state)` simple
  - Commencer par distance minimale pour connecter mes côtés
  - Utiliser Dijkstra comme dans greedy?
- [ ] Modifier compute_action pour tester toutes les actions et prendre la meilleure selon heuristique
- [ ] Tests:
  - vs random:
  - vs greedy:

### Jour 5: Debug et amélioration
- [ ] Identifier les coups stupides que mon agent fait
- [ ] Noter les bugs trouvés:
  -
  -
- [ ] Corriger et re-tester
- [ ] Résultats améliorés:
  -

---

## Semaine 3: Minimax et recherche (12-15h)

### Jour 1-2: Théorie minimax
- [ ] Revoir notes de cours sur minimax
- [ ] Dessiner arbre de jeu exemple sur papier (3 niveaux)
- [ ] Comprendre alternance max/min
- [ ] Pseudo-code minimax de base:
  ```



  ```

### Jour 3-4: Implémentation minimax v1
- [ ] Créer fonction `minimax(state, depth, maximizing)`
- [ ] Tester avec profondeur 1 d'abord (juste regarder 1 coup adversaire)
- [ ] Vérifier que ça bat mon agent heuristique simple
- [ ] Problèmes rencontrés:
  -
  -
- [ ] Résultats profondeur 1:
  - vs greedy:
  - temps par coup:

### Jour 5: Augmenter profondeur
- [ ] Essayer profondeur 2
- [ ] Mesurer temps de calcul - probablement trop lent!
- [ ] Notes sur performance:
  - Profondeur 2 → X secondes par coup
  - Trop lent? Besoin d'optimiser

---

## Semaine 4: Optimisations (12-15h)

### Jour 1-2: Alpha-beta pruning
- [ ] Comprendre le principe (couper branches inutiles)
- [ ] Implémenter version alpha-beta
- [ ] Comparer vitesse vs minimax normal:
  - Minimax prof 2: X sec
  - Alpha-beta prof 2: Y sec
  - Gain:
- [ ] Tester profondeur 3 maintenant possible?

### Jour 3: Améliorer l'heuristique
- [ ] Brainstorm nouvelles idées:
  - Contrôle du centre?
  - Bloquer chemins adverses?
  - Groupes connectés?
- [ ] Implémenter 2-3 heuristiques différentes
- [ ] Tester chacune séparément
- [ ] Résultats comparatifs:
  | Heuristique | vs greedy | vs minimax v1 |
  |-------------|-----------|---------------|
  | Distance    |           |               |
  | Centre      |           |               |
  | Connecté    |           |               |
  | Combinée    |           |               |

### Jour 4-5: Optimisations diverses
- [ ] Trier les actions (essayer meilleures en premier pour alpha-beta)
- [ ] Cache/memoization?
- [ ] Gérer le temps (iterative deepening?)
- [ ] Idées d'optimisation:
  -
  -
  -
- [ ] Impact mesuré:
  - Avant:
  - Après:

---

## Semaine 5: Tests et tuning (10-12h)

### Jour 1-2: Batterie de tests
- [ ] Faire jouer 20 parties vs greedy
  - Résultat: X/20 victoires
- [ ] Faire jouer 10 parties vs random
  - Résultat: X/10 victoires
- [ ] Identifier patterns de défaite
- [ ] Situations problématiques observées:
  -
  -
  -

### Jour 3: Ajustements finaux
- [ ] Tweaker poids de l'heuristique
- [ ] Ajuster profondeur selon temps restant
- [ ] Stratégie d'allocation du temps:
  - Premiers coups: X secondes
  - Milieu partie: Y secondes
  - Fin partie: Z secondes
- [ ] Tests après ajustements:
  -

### Jour 4: Soumission Abyss (optionnel mais recommandé)
- [ ] Créer compte Abyss si pas déjà fait
- [ ] Préparer ZIP avec:
  - my_player.py
  - requirements.txt
  - dossier src_mat1_mat2/ si fichiers supplémentaires
- [ ] Upload sur Abyss
- [ ] Attendre validation
- [ ] Observer premières parties
- [ ] Notes sur classement:
  -

### Jour 5: Itérations basées sur Abyss
- [ ] Analyser parties perdues (télécharger JSON)
- [ ] Identifier faiblesses
- [ ] Corrections à faire:
  -
  -
- [ ] Re-soumettre version améliorée

---

## Semaine 6: Finalisation agent (8-10h)

### Jour 1-2: Polissage du code
- [ ] Nettoyer commentaires
- [ ] Supprimer prints de debug
- [ ] Vérifier qu'il n'y a pas d'imports inutiles
- [ ] Ajouter docstrings aux fonctions importantes
- [ ] Tests finaux sans crash

### Jour 3: Gestion robuste des erreurs
- [ ] Que faire si timeout proche?
- [ ] Gérer cas limites (début/fin de partie)
- [ ] Fallback si algo plante
- [ ] Tests de robustesse:
  - [ ] 50 parties sans crash
  - [ ] Respecte limite 15min
  - [ ] Pas d'action invalide

### Jour 4: Version finale agent concours
- [ ] Derniers tests approfondis
- [ ] Statistiques finales:
  - vs random:
  - vs greedy:
  - Temps moyen:
  - RAM utilisée:
- [ ] **REMISE AGENT CONCOURS - 16 NOV**
- [ ] Backup du code quelque part!

---

## Semaine 7: Rapport (12-15h)

### Jour 1: Structure et intro
- [ ] Créer document LaTeX/Word
- [ ] Page de titre avec:
  - Nom équipe Challonge
  - Noms + matricules
- [ ] Introduction (1/2 page):
  - Contexte du projet
  - Objectifs
  - Structure du rapport

### Jour 2: Section Méthodologie (2 pages)
- [ ] Expliquer l'algorithme choisi (minimax? alphabeta? MCTS?)
- [ ] Décrire l'heuristique en détail
  - Quels critères?
  - Pourquoi ces choix?
  - Formule mathématique si applicable
- [ ] Gestion du temps de calcul
- [ ] Schémas/pseudo-code pour clarifier
- [ ] Contenu écrit:
  -
  -

### Jour 3: Section Résultats (1.5 page)
- [ ] Créer tableaux de résultats:
  | Version | vs random | vs greedy | Profondeur | Temps/coup |
  |---------|-----------|-----------|------------|------------|
  | v0.1    |           |           |            |            |
  | v0.2    |           |           |            |            |
  | finale  |           |           |            |            |
- [ ] Graphiques d'évolution (taux victoire, temps calcul)
- [ ] Utiliser données Abyss si dispo
- [ ] Analyser 2-3 parties intéressantes
- [ ] Screenshots de parties?

### Jour 4: Discussion et conclusion (1 page)
- [ ] Avantages de mon approche:
  -
  -
- [ ] Limites identifiées:
  -
  -
- [ ] Pistes d'amélioration:
  - Si j'avais plus de temps...
  - Approches alternatives possibles
  -
- [ ] Conclusion (ce que j'ai appris)

### Jour 5: Finitions rapport
- [ ] Relecture orthographe/grammaire
- [ ] Vérifier que toutes les figures sont référencées
- [ ] Ajouter références si j'ai utilisé des ressources externes
- [ ] Vérifier limite 5 pages (+ annexes OK)
- [ ] Exporter en PDF
- [ ] Faire relire par binôme/ami

---

## Semaine 8: Remise finale (2-3h)

### Jour 1: Préparation ZIP final
- [ ] Vérifier structure:
  ```
  mat1_mat2_Projet.zip
  ├── my_player.py
  ├── requirements.txt
  └── src_mat1_mat2/  (si fichiers supplémentaires)
      └── ...
  ```
- [ ] Tester dans environnement PROPRE:
  ```bash
  python -m venv test_env
  source test_env/bin/activate
  pip install -r requirements.txt
  python main_hex.py -t local my_player.py greedy_player_hex.py
  ```
- [ ] Checklist finale:
  - [ ] Code compile sans erreur
  - [ ] Gagne vs greedy au moins 1x/3
  - [ ] Pas de print() de debug
  - [ ] requirements.txt à jour
  - [ ] Matricules en commentaire en haut du fichier

### Jour 2: Soumission Moodle
- [ ] Nommer fichiers correctement:
  - Code: `mat1_mat2_Projet.zip`
  - Rapport: `mat1_mat2_Projet.pdf`
- [ ] Upload sur Moodle AVANT MINUIT 4 DÉC
- [ ] Vérifier confirmation upload
- [ ] Garder copie locale de backup
- [ ] **PROJET TERMINÉ!!!** 🎉

---

## Notes / Idées en vrac

### Idées d'heuristique à explorer:
-
-
-

### Bugs rencontrés:
-
-
-

### Ressources utiles:
-
-
-

### Questions pour le chargé de labo:
-
-
-

### Optimisations possibles:
-
-
-

### Résultats parties importantes:
-
-
-

---

## Rétrospective (à remplir à la fin)

**Ce qui a bien marché:**
-
-

**Ce qui était difficile:**
-
-

**Ce que j'ai appris:**
-
-

**Si c'était à refaire:**
-
-