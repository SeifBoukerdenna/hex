### Semaine 4: Iterative Deepening et Optimisations

#### ✅ Tâches complétées

- [x] Alpha-beta pruning (fait en semaine 3)
- [x] Implémenter iterative deepening
- [x] Gestion du temps par coup
- [x] Tester v0.6 vs v0.5
- [x] Valider performances vs random et greedy

---

## Comparaison v0.5 vs v0.6

### Architecture v0.5 (Alpha-Beta fixe)

```python
self.max_depth = 2  # Toujours profondeur 2
# Explore jusqu'à profondeur 2, peu importe le temps
```

**Problèmes:**

- Profondeur fixe = temps variable (19s à 50s)
- Pas de contrôle du budget temps
- Risque de timeout en compétition

### Architecture v0.6 (Iterative Deepening)

```python
self.max_depth = 10  # Limite haute
self.time_per_move = 5.0  # Budget par coup

for depth in range(1, self.max_depth + 1):
    try:
        # Chercher à cette profondeur
        # Si timeout → break et retourner meilleur coup trouvé
    except TimeoutError:
        break
```

**Avantages:**

- Temps contrôlé (~5s par coup)
- Toujours un coup valide (profondeur 1 garantie)
- Utilise le temps disponible intelligemment
- Plus profond quand la position est simple

---

## Implémentation détaillée

### Iterative Deepening

```python
def compute_action(self, current_state, **kwargs):
    start_time = time.time()
    best_action = possible_actions[0]  # Fallback

    for depth in range(1, self.max_depth + 1):
        try:
            # Chercher à profondeur `depth`
            current_best = self.search_at_depth(depth, start_time)
            best_action = current_best  # Sauvegarder si réussi
        except TimeoutError:
            break  # Temps écoulé, retourner dernier best_action

    return best_action
```

### Vérification du temps dans alpha-beta

```python
def alphabeta(self, state, depth, alpha, beta, maximizing, start_time):
    if time.time() - start_time > self.time_per_move:
        raise TimeoutError()  # Interruption propre
    # ... reste de l'algorithme
```

### Paramètres clés

| Paramètre       | Valeur | Justification                        |
| --------------- | ------ | ------------------------------------ |
| `max_depth`     | 10     | Limite théorique (rarement atteinte) |
| `time_per_move` | 5.0s   | ~60 coups × 5s = 300s << 900s budget |

---

## 📊 Résultats des tests v0.6

### TEST 1: v0.6 vs Random (10 parties)

**Configuration Rouge (premier):**
| Partie | Résultat | Temps |
|--------|----------|-------|
| 1 | ✓ Victoire | 20.6s |
| 2 | ✓ Victoire | 23.1s |
| 3 | ✓ Victoire | 27.3s |
| 4 | ✓ Victoire | 26.7s |
| 5 | ✓ Victoire | 31.4s |
| **Total** | **5/5 (100%)** | **Moy: 25.8s** |

**Configuration Bleu (second):**
| Partie | Résultat | Temps |
|--------|----------|-------|
| 1 | ✓ Victoire | 30.1s |
| 2 | ✓ Victoire | 39.9s |
| 3 | ✓ Victoire | 20.4s |
| 4 | ✓ Victoire | 23.4s |
| 5 | ✓ Victoire | 23.0s |
| **Total** | **5/5 (100%)** | **Moy: 27.4s** |

**Résultat global vs Random: 10/10 (100%)**

### TEST 2: v0.6 vs Greedy (10 parties)

**Configuration Rouge (premier):**
| Partie | Résultat | Temps |
|--------|----------|-------|
| 1 | ✓ Victoire | 24.0s |
| 2 | ✓ Victoire | 29.9s |
| 3 | ✓ Victoire | 23.7s |
| 4 | ✓ Victoire | 26.8s |
| 5 | ✓ Victoire | 25.0s |
| **Total** | **5/5 (100%)** | **Moy: 25.9s** |

**Configuration Bleu (second):**
| Partie | Résultat | Temps |
|--------|----------|-------|
| 1 | ✓ Victoire | 34.2s |
| 2 | ✓ Victoire | 35.6s |
| 3 | ✓ Victoire | 36.7s |
| 4 | ✓ Victoire | 37.2s |
| 5 | ✓ Victoire | 36.8s |
| **Total** | **5/5 (100%)** | **Moy: 36.1s** |

**Résultat global vs Greedy: 10/10 (100%)**

### TEST 3: v0.6 vs v0.5 (10 parties)

| Configuration           | Gagnant        | Temps moy |
| ----------------------- | -------------- | --------- |
| v0.6 Rouge vs v0.5 Bleu | v0.6 (5/5)     | 153.9s    |
| v0.5 Rouge vs v0.6 Bleu | v0.5 (5/5)     | 154.9s    |
| **Total**               | **5/10 (50%)** | -         |

**Analyse:** 50% = force égale. Le premier joueur gagne toujours car les deux agents ont la même stratégie. Cela confirme que v0.6 n'est pas plus faible que v0.5.

---

## 📈 Tableau comparatif complet

| Version  | vs Random | vs Greedy | vs v0.5 | Temps/partie | Contrôle temps |
| -------- | --------- | --------- | ------- | ------------ | -------------- |
| v0.5     | 100%      | 100%      | -       | ~30s         | ❌ Non         |
| **v0.6** | **100%**  | **100%**  | **50%** | **~28s**     | **✅ Oui**     |

### Amélioration clé: Gestion du temps

**v0.5:**

- Temps imprévisible (19s à 50s)
- Risque de dépasser le budget de 15 min
- Pas d'adaptation à la complexité

**v0.6:**

- Temps contrôlé (~5s par coup max)
- Budget garanti: 60 coups × 5s = 300s << 900s
- Peut chercher plus profond sur positions simples

---

## 🤔 Analyse approfondie

### Pourquoi v0.6 = v0.5 en force?

Les deux versions utilisent:

1. Même heuristique (distance_adversaire - ma_distance)
2. Même alpha-beta pruning
3. Même tri des actions (centre d'abord)

La seule différence est la gestion du temps. Avec 5s/coup, v0.6 atteint généralement profondeur 2 comme v0.5, d'où les performances identiques.

### Pourquoi le temps varie (20s à 40s par partie)?

Facteurs:

1. **Nombre de coups:** Parties courtes = moins de temps total
2. **Complexité des positions:** Certaines nécessitent plus d'exploration
3. **Efficacité du pruning:** Variable selon l'ordre des coups

### Calcul du budget temps

```
Budget total: 15 min = 900 secondes
Coups typiques: 40-80 par partie
Temps par coup: 5s

Pire cas: 80 coups × 5s = 400s (44% du budget)
Cas moyen: 60 coups × 5s = 300s (33% du budget)

Marge de sécurité: >50% du budget inutilisé ✓
```

---

## 💡 Optimisations futures possibles

### 1. Augmenter time_per_move

```python
self.time_per_move = 10.0  # Doubler le temps
```

- Permettrait profondeur 3 plus souvent
- Toujours dans le budget (600s < 900s)

### 2. Temps adaptatif selon la phase

```python
def get_time_for_move(self, step):
    if step < 20:
        return 8.0   # Début: positions cruciales
    elif step < 60:
        return 5.0   # Milieu: temps standard
    else:
        return 2.0   # Fin: positions simples
```

### 3. Améliorer l'heuristique

```python
def evaluate(self, state):
    score = opponent_distance - my_distance

    # Bonus centre
    for pos in my_pieces:
        score += 0.1 * (7 - abs(pos[0]-6.5) - abs(pos[1]-6.5))

    # Bonus connectivité
    score += 0.5 * connected_groups_bonus

    return score
```

### 4. Transposition table

```python
self.transposition_table = {}

def alphabeta(self, state, ...):
    state_hash = self.hash_state(state)
    if state_hash in self.transposition_table:
        return self.transposition_table[state_hash]
    # ... calcul
    self.transposition_table[state_hash] = result
```

---

## 🎯 Prochaines étapes recommandées

### Priorité 1: Soumettre sur Abyss

- Tester contre de vrais adversaires
- Identifier faiblesses contre agents humains
- Obtenir classement Elo initial

### Priorité 2: Préparer agent concours (16 nov)

- Nettoyer le code
- Supprimer prints de debug
- Vérifier requirements.txt
- Tester sur environnement propre

### Priorité 3: Améliorations optionnelles

- Heuristique améliorée
- Temps adaptatif
- Plus de tests statistiques

---

## 📝 Structure du code v0.6

```
my_player.py (v0.6)
├── __init__
│   ├── piece_type, opponent_type
│   ├── max_depth = 10
│   └── time_per_move = 5.0
├── compute_action
│   ├── Tri des actions (centre first)
│   └── Iterative deepening avec timeout
├── alphabeta
│   ├── Vérification temps
│   ├── Alpha-beta pruning
│   └── Tri des actions
├── evaluate
│   └── distance_adversaire - ma_distance
└── calculate_shortest_path
    └── Dijkstra
```

---

## ⏱️ Temps passé Semaine 4

| Tâche                              | Temps   |
| ---------------------------------- | ------- |
| Implémentation iterative deepening | ~1h     |
| Debug et corrections               | ~30min  |
| Tests v0.6                         | ~1h     |
| Documentation                      | ~30min  |
| **Total**                          | **~3h** |

---

## 💭 Réflexions finales

### Ce que v0.6 apporte

- ✅ Gestion du temps robuste pour la compétition
- ✅ Même force que v0.5
- ✅ Code prêt pour soumission Abyss

### Ce qui reste identique

- Heuristique (shortest path difference)
- Force de jeu (100% vs random/greedy)
- Alpha-beta avec tri centre

### Décision pour la compétition

v0.6 est recommandé pour la soumission car:

1. Gestion du temps garantit pas de timeout
2. Force identique à v0.5
3. Architecture extensible pour futures améliorations

**Status:** Prêt pour soumission Abyss et concours du 16 novembre.
