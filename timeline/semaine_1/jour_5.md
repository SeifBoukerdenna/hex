### Jour 5: Analyse approfondie du greedy

- [x] Ouvrir `greedy_player_hex.py` et annoter chaque partie

**STRUCTURE GÉNÉRALE DU CODE:**
```python
# 1. INITIALISATION (lignes ~30-50)
# - Crée une matrice de distances (toutes à l'infini au début)
# - Crée une matrice de prédécesseurs (pour reconstruire le chemin)
# - Définit les objectifs (ligne d'arrivée)
# - Initialise la priority queue pour Dijkstra

# 2. DIJKSTRA (lignes ~52-70)
# - Explore le plateau case par case
# - Calcule le chemin le plus court vers l'objectif
# - Distance = 0 si case déjà occupée par moi
# - Distance = 1 si case vide (coût de jouer là)
# - Distance = ∞ si case occupée par adversaire (bloquée)

# 3. SÉLECTION DU COUP (lignes ~72-76)
# - Reconstruit le chemin optimal trouvé
# - Parmi les cases vides du chemin, choisit celle la plus proche du centre
# - Retourne l'action correspondante
```

**ANNOTATIONS DÉTAILLÉES:**
```python
# ÉTAPE 1: Créer structures de données
dist = np.full((14, 14), np.inf)  # Distance pour atteindre chaque case
preds = np.full((14, 14), None)   # Prédécesseur de chaque case (pour reconstruire chemin)
objectives = []                    # Liste des cases d'arrivée
pq = []                           # Priority queue pour Dijkstra

# ÉTAPE 2: Initialiser selon couleur du joueur
if self.piece_type == "R":  # Rouge doit aller de haut (ligne 0) en bas (ligne 13)
    for j in range(14):
        objectives.append((13, j))  # Toute la ligne du bas = objectifs
        if env.get((0,j)) is None:  # Si case vide en haut
            dist[0, j] = 1          # Coût = 1 (il faudra jouer là)
        elif env.get((0,j)).piece_type == "R":  # Si déjà ma pièce
            dist[0, j] = 0          # Coût = 0 (déjà occupé!)
        else:                       # Si pièce adverse
            continue                # Skip, ne pas ajouter à la queue
        heapq.heappush(pq, (dist[0, j], (0, j), None))  # Ajouter à la queue

# Même logique pour Bleu mais horizontal (colonne 0 → colonne 13)

# ÉTAPE 3: Dijkstra - trouver le plus court chemin
while len(pq) != 0:
    d, (i, j), pred = heapq.heappop(pq)  # Prendre case avec plus petite distance

    if d > dist[i, j]:  # Si déjà visité avec meilleure distance, skip
        continue

    preds[i,j] = pred  # Enregistrer d'où on vient

    if (i,j) in objectives:  # Si on a atteint une case d'arrivée
        path = retrace_path(preds, (i,j))  # Reconstruire le chemin
        break  # STOP, on a trouvé!

    # Explorer les voisins
    for n_type, (ni, nj) in current_state.rep.get_neighbours(i, j).values():
        if n_type == "EMPTY":           # Case vide
            new_dist = d + 1            # Coût = distance actuelle + 1
        elif n_type == self.piece_type: # Ma pièce
            new_dist = d                # Coût = distance actuelle + 0 (gratuit!)
        else:                           # Pièce adverse ou OUTSIDE
            continue                    # Ignorer, ne pas explorer

        if new_dist < dist[ni, nj]:     # Si meilleur chemin trouvé
            dist[ni, nj] = new_dist     # Mettre à jour distance
            heapq.heappush(pq, (new_dist, (ni, nj), (i, j)))  # Ajouter à explorer

# ÉTAPE 4: Choisir quelle case jouer sur le chemin
hq = []  # Nouvelle priority queue
for pos in path:  # Pour chaque case du chemin optimal
    if env.get(pos) == None:  # Si case vide (pas déjà jouée)
        # Calculer distance Manhattan au centre (6.5, 6.5)
        center_dist = abs(pos[0]-6.5) + abs(pos[1]-6.5)
        heapq.heappush(hq, (center_dist, pos))  # Ajouter avec priorité = distance au centre

_, pos = heapq.heappop(hq)  # Prendre la case la PLUS PROCHE du centre
return LightAction({"piece": self.piece_type, "position": pos})
```

- [x] Comprendre l'algo de Dijkstra utilisé

**ALGORITHME DE DIJKSTRA ADAPTÉ POUR HEX:**

**Dijkstra classique:**
- Trouve le plus court chemin dans un graphe pondéré
- Utilise une priority queue pour explorer les nœuds par ordre de distance croissante
- Garantit de trouver le chemin optimal

**Adaptation pour Hex:**

1. **Graphe = plateau hexagonal**
   - Nœuds = cases du plateau
   - Arêtes = voisins (6 directions)
   - Poids des arêtes = coût pour traverser

2. **Pondération intelligente:**
   - Case VIDE → coût = 1 (il faudra jouer un coup là)
   - Case avec MA pièce → coût = 0 (déjà occupée, passage gratuit!)
   - Case ADVERSE → coût = ∞ (bloquée, ne pas considérer)

3. **Point de départ:**
   - Rouge: toute la ligne du HAUT (ligne 0)
   - Bleu: toute la colonne de GAUCHE (colonne 0)
   - Plusieurs points de départ possibles!

4. **Point d'arrivée:**
   - Rouge: toute la ligne du BAS (ligne 13)
   - Bleu: toute la colonne de DROITE (colonne 13)
   - Plusieurs objectifs possibles!

5. **Résultat:**
   - Chemin avec la PLUS PETITE distance
   - Distance = nombre de coups nécessaires pour compléter le chemin
   - Exemple: distance = 5 → il reste 5 cases vides à jouer sur ce chemin

**POURQUOI C'EST MALIN:**
- Calcule le chemin qui nécessite le MOINS de coups pour gagner
- Profite des pièces déjà jouées (coût = 0)
- Évite automatiquement les pièces adverses
- Trouve le chemin optimal mathématiquement

**EXEMPLE CONCRET:**
```
Situation:
R = mes pièces rouges
B = pièces bleues adverses
. = vide

Ligne 0:  . . R . .
Ligne 1:  . R . B .
Ligne 2:  R . . . .
Ligne 3:  . . B . .
...

Dijkstra calcule:
Chemin 1: ligne0[2] → ligne1[1] → ligne2[0] → ... (distance = 3)
          (car 3 cases vides à jouer)
Chemin 2: ligne0[0] → ligne1[0] → ... (distance = 5)
          (car 5 cases vides à jouer)

→ Choisit Chemin 1 (distance minimale)
```

- [x] Pourquoi il joue proche du centre?

**RAISONS DE JOUER AU CENTRE:**

1. **Flexibilité maximale**
   - Centre = plus d'options de connexion
   - Peut bifurquer dans plusieurs directions
   - Moins facile à bloquer

2. **Équidistance**
   - Distance égale vers les bords
   - Peut adapter stratégie selon adversaire
   - Symétrie avantageuse

3. **Éviter les extrémités**
   - Jouer trop à gauche/droite = se limiter
   - Coins = moins de voisins disponibles
   - Centre = 6 voisins disponibles toujours

4. **Logique du code:**
```python
   center_dist = abs(pos[0]-6.5) + abs(pos[1]-6.5)
```
   - Calcule distance Manhattan au centre (6.5, 6.5)
   - Sur plateau 14×14, centre = (7, 7) environ
   - Minimise cette distance = privilégie centre

5. **Stratégie géométrique**
   - Plus court chemin géométriquement = passer par le centre
   - Diagonale traverse le centre
   - Centre (7,7) est sur la diagonale optimale

**ILLUSTRATION:**
```
Plateau 14×14:

(0,0)  ─────────────────── (0,13)
  │                            │
  │         CENTRE             │
  │          (7,7)             │
  │          ★                 │
  │                            │
(13,0) ─────────────────── (13,13)

Chemin passant par centre = plus court
Chemin passant par bords = plus long
```

- [x] Schéma de l'algorithme sur papier:

**SCHÉMA COMPLET DE L'ALGORITHME GREEDY:**
```
┌─────────────────────────────────────────────┐
│ DÉBUT: compute_action(current_state)        │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ INITIALISATION                              │
│ - Créer matrice dist[14][14] = ∞           │
│ - Créer matrice preds[14][14] = None       │
│ - Définir objectives (ligne/colonne fin)   │
│ - Créer priority_queue = []                │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ SELON MA COULEUR                            │
│ Rouge (R): départ = ligne 0, fin = ligne 13│
│ Bleu (B): départ = col 0, fin = col 13     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ INITIALISER DÉPARTS                         │
│ Pour chaque case de départ:                │
│   - Si VIDE: dist = 1, ajouter à PQ        │
│   - Si MA PIÈCE: dist = 0, ajouter à PQ    │
│   - Si ADVERSE: ignorer                    │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ BOUCLE DIJKSTRA                             │
│ Tant que priority_queue non vide:          │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
┌──────────────┐   ┌──────────────────┐
│ Pop case     │   │ Case déjà        │
│ (d, pos)     │   │ visitée?         │
│ plus petite  │   │ → continue       │
│ distance     │   └──────────────────┘
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│ Enregistrer preds[pos] = pred               │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
         ┌────────┴────────┐
         │ pos dans        │
         │ objectives?     │
         └────────┬────────┘
              NON │   OUI
                  │   │
                  │   ▼
                  │  ┌─────────────────┐
                  │  │ CHEMIN TROUVÉ!  │
                  │  │ Reconstruire    │
                  │  │ avec preds      │
                  │  │ → SORTIE BOUCLE │
                  │  └─────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ EXPLORER LES 6 VOISINS                      │
│ Pour chaque voisin (ni, nj):               │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
         ┌────────┴────────┐
         │ Type voisin?    │
         └────────┬────────┘
         │        │        │
    EMPTY│   MA PIÈCE│  ADVERSE
         │        │        │
         ▼        ▼        ▼
    new_dist  new_dist  continue
      = d+1     = d+0   (ignorer)
         │        │
         └────┬───┘
              │
              ▼
    ┌──────────────────────┐
    │ new_dist < dist[ni,nj]?│
    └──────────┬─────────────┘
            OUI│   NON
               │   (ignorer)
               ▼
    ┌──────────────────────┐
    │ Mettre à jour:       │
    │ dist[ni,nj] = new_dist│
    │ Ajouter à PQ         │
    └──────────────────────┘
               │
               │ (retour boucle)
               │
               ▼
┌─────────────────────────────────────────────┐
│ FIN BOUCLE: path contient le chemin optimal│
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ SÉLECTION DU COUP                           │
│ Pour chaque case du path:                  │
│   - Si VIDE: calculer distance au centre   │
│   - Ajouter à heap_queue                   │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ Pop case avec distance minimale au centre  │
│ = Case la plus proche du centre (7,7)      │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ RETOUR: LightAction(piece, position)       │
└─────────────────────────────────────────────┘
```

**EXEMPLE PAS-À-PAS SUR MINI-PLATEAU 5×5:**
```
Initial (Rouge joue):
    0 1 2 3 4
0   . . R . .
1   . . . . .
2   . . . B .
3   . . . . .
4   . . . . .

Étape 1: Init
dist[0][2] = 0 (ma pièce)
dist[0][0] = 1, dist[0][1] = 1, dist[0][3] = 1, dist[0][4] = 1

Étape 2: Dijkstra explore
Depuis (0,2) avec dist=0:
  → (1,1): EMPTY, dist = 0+1 = 1
  → (1,2): EMPTY, dist = 0+1 = 1
  → (1,3): EMPTY, dist = 0+1 = 1

Depuis (0,0) avec dist=1:
  → (1,0): EMPTY, dist = 1+1 = 2
  → (1,1): déjà dist=1, skip

... continue jusqu'à atteindre ligne 4

Étape 3: Chemin trouvé
path = [(4,2), (3,2), (2,2), (1,2), (0,2)]
Cases vides: [(4,2), (3,2), (2,2), (1,2)]

Étape 4: Sélection
Centre = (2, 2)
Distances au centre:
  (4,2): |4-2| + |2-2| = 2
  (3,2): |3-2| + |2-2| = 1  ← MINIMUM!
  (2,2): |2-2| + |2-2| = 0  ← mais occupé par B
  (1,2): |1-2| + |2-2| = 1

Résultat: Joue (3,2) ou (1,2)
```

**POINTS CLÉS À RETENIR:**

1. **Dijkstra modifié** avec pondération intelligente (0 pour mes pièces, 1 pour vide)
2. **Multi-source, multi-destination** (toute une ligne/colonne)
3. **Sélection au centre** parmi les cases du chemin optimal
4. **Aucune défense** - calcule seulement SON chemin, pas celui de l'adversaire
5. **Déterministe** - même situation = même coup
6. **Complexité** - O(n² log n) où n = taille plateau (acceptable pour 14×14)

**FAIBLESSE PRINCIPALE:**
- Ne calcule JAMAIS le chemin adverse
- Ne bloque JAMAIS activement
- Vulnérable à un adversaire qui construit un chemin plus rapide