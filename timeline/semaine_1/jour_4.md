
### Jour 4: Lecture du code (important!)

- [x] Lire `board_hex.py` - comprendre la structure du plateau

  **Comment sont stockées les pièces?**
  - Les pièces sont dans un dictionnaire `env` avec clé = tuple (i,j) et valeur = objet Piece
  - Format: `env[(i,j)] = Piece(piece_type="R" ou "B", owner=player)`
  - Cases vides = pas dans le dictionnaire (pas de clé)
  - Dimensions du plateau stockées dans `self.dimensions` (ex: [14, 14])

  **Comment récupérer les voisins?**
  - Fonction `get_neighbours(i, j)` retourne un dict avec 6 voisins
  - Clés: "top_right", "top_left", "bot_left", "bot_right", "left", "right"
  - Valeurs: tuple (type, (i,j)) où type = "EMPTY", "OUTSIDE", "R", ou "B"
  - Exemple: `{"top_right": ("R", (5,7)), "left": ("EMPTY", (6,5)), ...}`
  - IMPORTANT: Hex a 6 voisins, pas 8 comme échecs!

- [x] Lire `player_hex.py` - voir ce que je dois hériter

  **Structure de PlayerHex:**
  - Hérite de la classe `Player` de seahorse
  - Attribut principal: `piece_type` ("R" ou "B")
  - Attribut secondaire: `name` (par défaut "bob")
  - Méthodes utiles:
    - `get_piece_type()` → retourne "R" ou "B"
    - `set_piece_type(piece_type)` → change la couleur (validation incluse)

  **Ce que je dois implémenter dans MY_PLAYER:**
  - Hériter de PlayerHex: `class MyPlayer(PlayerHex):`
  - Redéfinir `__init__()` pour initialiser mes attributs personnels
  - **OBLIGATOIRE:** implémenter `compute_action(self, current_state, **kwargs) -> Action`
  - C'est la SEULE fonction que je dois coder!

  **Structure minimale:**
```python
  class MyPlayer(PlayerHex):
      def __init__(self, piece_type: str, name: str = "MyAgent"):
          super().__init__(piece_type, name)
          # Mes attributs perso ici

      def compute_action(self, current_state: GameState, **kwargs):
          # Mon algorithme ici
          return une_action_valide
```

- [x] Lire `game_state_hex.py` - **LE PLUS IMPORTANT**

  **`get_possible_light_actions()` → actions possibles**
  - Retourne un générateur de toutes les actions légales
  - Format: `LightAction({"piece": "R", "position": (i,j)})`
  - Itère sur toutes les cases vides du plateau
  - Usage: `for action in current_state.get_possible_light_actions():`
  - Début de partie: 196 actions (14x14), diminue à chaque coup

  **`apply_action(action)` → simuler un coup**
  - Prend une LightAction en paramètre
  - Retourne un NOUVEAU GameStateHex (ne modifie pas l'actuel!)
  - Crée une copie du board avec la nouvelle pièce ajoutée
  - Incrémente le step de 1
  - Change le next_player (alterne entre joueurs)
  - Recalcule les scores via compute_scores()
  - **IMPORTANT:** Si position déjà occupée, retourne état inchangé (sécurité)

  **`compute_scores(play_info)` → vérifier victoire**
  - Appelée automatiquement par apply_action()
  - Utilise DFS (Depth-First Search) pour vérifier connectivité
  - Pour Rouge (player1): cherche chemin de ligne 0 à ligne 13
  - Pour Bleu (player2): cherche chemin de colonne 0 à colonne 13
  - Retourne `{player1_id: 1.0, player2_id: 0.0}` si Rouge gagne
  - Retourne `{player1_id: 0.0, player2_id: 1.0}` si Bleu gagne
  - Retourne `{player1_id: 0.0, player2_id: 0.0}` si partie continue
  - **Astuce:** Ajoute temporairement la pièce, teste, puis la retire (non destructif)

  **`get_neighbours(i, j)` → cases adjacentes**
  - Appelle directement `board.get_neighbours(i, j)`
  - Même fonctionnalité que dans BoardHex
  - Utile pour faire des DFS/BFS dans mon agent

  **Autres fonctions importantes:**
  - `get_step()` → numéro du tour actuel (0 à 196 max)
  - `is_done()` → True si quelqu'un a gagné
  - `in_board(index)` → vérifie si (i,j) est dans le plateau
  - `get_player_id(pid)` → récupère l'objet Player depuis son ID
  - `generate_possible_heavy_actions()` → comme light mais avec états complets (plus lourd)

- [x] Notes/questions sur le code:

  **Différence LightAction vs HeavyAction:**
  - LightAction = juste la position à jouer `{"piece": "R", "position": (5,7)}`
  - HeavyAction = état actuel + état futur complet (plus de mémoire)
  - Pour mon agent: toujours utiliser LightAction (plus efficace)
  - Le système convertit automatiquement si nécessaire

  **Comment fonctionne le DFS de victoire:**
```python
  # Pour Rouge (top→bottom):
  # 1. Pour chaque case de la ligne 0 qui contient une pièce rouge
  # 2. Lance un DFS récursif vers le bas
  # 3. Si atteint ligne 13 → victoire!
  # 4. Visite seulement les voisins de même couleur
```

  **Gestion du temps:**
  - `**kwargs` peut contenir `remaining_time`
  - Mon agent doit gérer son budget de 15 minutes total
  - Pas de limite par coup, juste total pour toute la partie
  - Suggestion: mesurer temps écoulé et adapter profondeur de recherche

  **Pourquoi copy.copy() et pas deepcopy():**
  - `copy.copy(dict)` copie le dict mais pas les objets à l'intérieur
  - Suffisant car on ne modifie jamais les Piece existantes
  - Plus rapide que deepcopy (important pour performance)
  - Attention: ne pas modifier les Piece, seulement ajouter/retirer du dict

  **Structure d'un état:**
```python
  GameStateHex:
    - scores: {player1_id: 0.0, player2_id: 0.0}
    - next_player: objet Player (celui qui doit jouer)
    - players: [player1, player2] (liste des 2 joueurs)
    - rep: BoardHex (le plateau)
    - step: 0 à 196 (numéro du tour)
    - max_step: 196 (14*14)
```

  **Questions importantes résolues:**

  Q: Est-ce que je peux modifier current_state directement?
  R: NON! Toujours utiliser apply_action() qui retourne un NOUVEAU state

  Q: Comment savoir si c'est mon tour?
  R: `current_state.next_player.get_piece_type() == self.piece_type`

  Q: Comment itérer sur toutes les actions possibles?
  R: `for action in current_state.get_possible_light_actions():`

  Q: Comment simuler un coup pour l'évaluer?
  R: `new_state = current_state.apply_action(action)`

  Q: Comment vérifier si j'ai gagné après un coup?
  R: `new_state.scores[self.id] == 1.0` ou `new_state.is_done()`

  Q: Combien d'actions possibles en moyenne?
  R: Début: 196, milieu: ~100, fin: ~20

  **Points critiques pour mon agent:**

  1. **Ne JAMAIS retourner une action invalide**
     - Toujours choisir depuis `get_possible_light_actions()`
     - Vérifier que la position n'est pas déjà occupée

  2. **Gérer le temps correctement**
     - Garder une marge de sécurité (ne pas utiliser les 15min complètes)
     - Si timeout → agent perd automatiquement

  3. **Utiliser apply_action() pour la recherche**
     - Simuler des coups futurs sans modifier le vrai état
     - Permet de faire minimax/alpha-beta

  4. **Structure typique de compute_action():**
```python
     def compute_action(self, current_state, **kwargs):
         # 1. Récupérer actions possibles
         actions = list(current_state.get_possible_light_actions())

         # 2. Évaluer chaque action
         best_action = None
         best_score = -float('inf')

         for action in actions:
             # 3. Simuler le coup
             new_state = current_state.apply_action(action)

             # 4. Évaluer la position résultante
             score = self.evaluate(new_state)

             # 5. Garder la meilleure
             if score > best_score:
                 best_score = score
                 best_action = action

         # 6. Retourner la meilleure action
         return best_action
```

  **Schéma du flux d'exécution:**
```
  GameMaster
      ↓
  appelle compute_action(current_state)
      ↓
  Mon agent analyse
      ↓
  retourne LightAction
      ↓
  GameMaster applique avec apply_action()
      ↓
  Nouveau state créé
      ↓
  compute_scores() vérifie victoire
      ↓
  Si pas fini: tour suivant (autre joueur)
  Si fini: partie terminée
```

  **Code test à faire:**
```python
  # Test 1: Vérifier get_possible_actions
  actions = list(current_state.get_possible_light_actions())
  print(f"Nombre d'actions: {len(actions)}")

  # Test 2: Simuler un coup
  first_action = actions[0]
  new_state = current_state.apply_action(first_action)
  print(f"Step avant: {current_state.get_step()}")
  print(f"Step après: {new_state.get_step()}")

  # Test 3: Vérifier voisins
  neighbors = current_state.get_neighbours(7, 7)  # Centre du plateau
  print(f"Voisins du centre: {neighbors}")

  # Test 4: Vérifier si partie finie
  print(f"Partie finie? {new_state.is_done()}")
  print(f"Scores: {new_state.scores}")
```


