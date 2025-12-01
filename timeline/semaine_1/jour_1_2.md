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
