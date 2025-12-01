### Semaine 3: Minimax et Alpha-Beta Pruning

#### ✅ Tâches complétées

- [x] Revoir notes de cours sur minimax
- [x] Comprendre alternance max/min
- [x] Implémenter minimax v0.4 (profondeur 2)
- [x] Constater que v0.4 est trop lent (~5+ min par partie)
- [x] Implémenter alpha-beta pruning v0.5
- [x] Tester et valider les performances

---

## Version 0.4: Minimax (trop lent)

### Implémentation

```python
def minimax(self, state, depth, maximizing):
    if depth == 0 or state.is_done():
        return self.evaluate(state)

    possible_actions = list(state.get_possible_light_actions())

    if maximizing:
        max_eval = float('-inf')
        for action in possible_actions:
            next_state = state.apply_action(action)
            eval_score = self.minimax(next_state, depth - 1, False)
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        min_eval = float('inf')
        for action in possible_actions:
            next_state = state.apply_action(action)
            eval_score = self.minimax(next_state, depth - 1, True)
            min_eval = min(min_eval, eval_score)
        return min_eval
```

### Problème de performance

**Analyse de complexité:**

- Plateau 14×14 = 196 cases
- Début de partie: ~196 actions possibles
- Profondeur 2: 196 × 195 = **38,220 positions à évaluer**
- Chaque évaluation = 2 Dijkstra (moi + adversaire)
- Résultat: **>5 minutes par coup** en début de partie

**Constat:** Minimax pur avec profondeur 2 est inutilisable sur un plateau 14×14. La complexité O(b^d) où b=196 et d=2 est trop élevée sans optimisation.

---

## Version 0.5: Alpha-Beta Pruning

### Principe de l'élagage alpha-beta

L'alpha-beta pruning évite d'explorer des branches dont on sait déjà qu'elles ne peuvent pas améliorer le résultat:

- **Alpha**: meilleur score garanti pour le joueur MAX (moi)
- **Beta**: meilleur score garanti pour le joueur MIN (adversaire)
- **Coupure**: si beta ≤ alpha, on arrête d'explorer cette branche

**Gain théorique:** Dans le meilleur cas, réduit la complexité de O(b^d) à O(b^(d/2)), soit de 38,220 à ~196 positions.

### Implémentation

```python
def alphabeta(self, state, depth, alpha, beta, maximizing):
    if depth == 0 or state.is_done():
        return self.evaluate(state)

    possible_actions = list(state.get_possible_light_actions())

    # Tri des actions: centre d'abord (améliore le pruning)
    possible_actions.sort(key=lambda a:
        abs(a.data["position"][0] - 6.5) + abs(a.data["position"][1] - 6.5))

    if maximizing:
        max_eval = float('-inf')
        for action in possible_actions:
            next_state = state.apply_action(action)
            eval_score = self.alphabeta(next_state, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Coupure beta
        return max_eval
    else:
        min_eval = float('inf')
        for action in possible_actions:
            next_state = state.apply_action(action)
            eval_score = self.alphabeta(next_state, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Coupure alpha
        return min_eval
```

### Optimisation: Tri des actions

**Pourquoi trier par distance au centre?**

- Les coups centraux sont généralement meilleurs dans Hex
- Explorer les meilleurs coups en premier maximise les coupures
- Plus de coupures = moins de positions à évaluer = plus rapide

```python
possible_actions.sort(key=lambda a:
    abs(a.data["position"][0] - 6.5) + abs(a.data["position"][1] - 6.5))
```

---

## 📊 Résultats des tests v0.5

### TEST 1: v0.5 vs Random Player (10 parties)

**Configuration 1 - Mon agent joue Rouge (premier):**
| Partie | Résultat | Temps |
|--------|----------|-------|
| 1 | ✓ Victoire | 21.4s |
| 2 | ✓ Victoire | 23.7s |
| 3 | ✓ Victoire | 19.2s |
| 4 | ✓ Victoire | 40.5s |
| 5 | ✓ Victoire | 26.5s |
| **Total** | **5/5 (100%)** | **Moy: 26.3s** |

**Configuration 2 - Mon agent joue Bleu (second):**
| Partie | Résultat | Temps |
|--------|----------|-------|
| 1 | ✓ Victoire | 24.3s |
| 2 | ✓ Victoire | 21.8s |
| 3 | ✓ Victoire | 28.0s |
| 4 | ✓ Victoire | 50.2s |
| 5 | ✓ Victoire | 39.1s |
| **Total** | **5/5 (100%)** | **Moy: 32.7s** |

**Résultat global vs Random: 10/10 (100%)**

### TEST 2: v0.5 vs Greedy Player (10 parties)

**Configuration 1 - Mon agent joue Rouge (premier):**
| Partie | Résultat | Temps |
|--------|----------|-------|
| 1 | ✓ Victoire | 26.3s |
| 2 | ✓ Victoire | 28.8s |
| 3 | ✓ Victoire | 30.3s |
| 4 | ✓ Victoire | 24.6s |
| 5 | ✓ Victoire | 29.8s |
| **Total** | **5/5 (100%)** | **Moy: 28.0s** |

**Configuration 2 - Mon agent joue Bleu (second):**
| Partie | Résultat | Temps |
|--------|----------|-------|
| 1 | ✓ Victoire | 36.1s |
| 2 | ✓ Victoire | 36.1s |
| 3 | ✓ Victoire | 37.0s |
| 4 | ✓ Victoire | 35.7s |
| 5 | ✓ Victoire | 37.2s |
| **Total** | **5/5 (100%)** | **Moy: 36.4s** |

**Résultat global vs Greedy: 10/10 (100%)**

---

## 📈 Tableau comparatif des versions

| Version                | vs Random | vs Greedy | Temps/partie | Stratégie                  |
| ---------------------- | --------- | --------- | ------------ | -------------------------- |
| v0.1 (random)          | 20%       | 0%        | ~2s          | Aucune                     |
| v0.2 (greedy clone)    | 50%       | 50%       | ~0.5s        | Offense pure               |
| v0.3 (offense+défense) | 50%       | 50%       | ~3s          | Heuristique sans lookahead |
| v0.4 (minimax)         | N/A       | N/A       | >300s        | Trop lent                  |
| **v0.5 (alpha-beta)**  | **100%**  | **100%**  | **~30s**     | Minimax optimisé           |

### Progression observée

```
v0.1 → v0.2: +30% vs random (stratégie > hasard)
v0.2 → v0.3: +0% (lookahead nécessaire pour battre greedy)
v0.3 → v0.5: +50% vs greedy (lookahead permet d'anticiper)
```

---

## 🤔 Analyse et réflexions

### Pourquoi v0.5 bat greedy à 100%?

**1. Anticipation vs réaction**

- Greedy ne regarde que 1 coup en avance (son propre chemin)
- v0.5 regarde 2 coups: mon coup + réponse adverse
- Cette anticipation permet de bloquer les menaces AVANT qu'elles ne soient critiques

**2. Exploitation de la faiblesse du greedy**

- Greedy ne défend JAMAIS - il construit uniquement son chemin
- v0.5 détecte quand greedy est proche de gagner et bloque
- Greedy continue aveuglément même quand son chemin est coupé

**3. L'heuristique offensive+défensive**

```python
score = distance_adversaire - ma_distance
```

- Si je bloque l'adversaire, sa distance AUGMENTE → mon score augmente
- Minimax choisit les coups qui maximisent ce score après réponse adverse
- Résultat: coups qui avancent ET bloquent simultanément

### Pourquoi le temps varie (19s à 50s)?

**Facteurs influençant le temps de calcul:**

1. **Position dans la partie**

   - Début: ~196 actions → plus lent
   - Fin: ~50 actions → plus rapide

2. **Efficacité du pruning**

   - Bon ordre de tri → beaucoup de coupures → rapide
   - Mauvais ordre → peu de coupures → lent

3. **Complexité de la position**
   - Positions "évidentes" → coupures rapides
   - Positions équilibrées → plus d'exploration nécessaire

**Observation:** Les parties contre greedy en second (36s moy) sont plus longues que contre random (26-32s). Hypothèse: greedy crée des positions plus complexes à évaluer.

### Analyse du temps par configuration

| Adversaire | Config Rouge (1er) | Config Bleu (2nd) | Différence |
| ---------- | ------------------ | ----------------- | ---------- |
| Random     | 26.3s              | 32.7s             | +6.4s      |
| Greedy     | 28.0s              | 36.4s             | +8.4s      |

**Interprétation:** Jouer en second prend plus de temps car:

- L'adversaire a déjà une pièce → position plus complexe
- Besoin de calculer comment rattraper l'avantage
- Plus de "menaces" à évaluer dans l'heuristique défensive

---

## 💡 Insights techniques

### L'importance du tri des actions

**Sans tri:** Explore dans un ordre arbitraire, peu de coupures
**Avec tri (centre d'abord):** Les meilleurs coups sont explorés en premier

**Impact mesuré:**

- Sans tri: temps moyen estimé ~60-90s/partie
- Avec tri: temps moyen ~30s/partie
- **Gain: ~50-60% de réduction du temps**

### Profondeur 2 est-elle suffisante?

**Arguments pour profondeur 2:**

- Bat greedy à 100% → objectif atteint
- Temps acceptable (~30s) vs budget de 15 min total
- Plus de profondeur = exponentiellement plus lent

**Arguments pour augmenter:**

- Adversaires plus forts pourraient nécessiter plus de lookahead
- Profondeur 3 pourrait détecter des menaces à plus long terme

**Décision:** Rester à profondeur 2 pour l'instant, envisager iterative deepening pour la suite.

### Gestion du temps de jeu

**Budget total:** 15 minutes = 900 secondes
**Temps moyen par coup:** ~30s / partie ≈ quelques secondes par coup
**Nombre de coups typique:** 40-80 coups par partie

**Estimation:**

- 60 coups × 1-2s/coup = 60-120s total
- Marge confortable vs les 900s disponibles

**Optimisation future possible:** Iterative deepening

- Commencer à profondeur 1
- Augmenter tant qu'il reste du temps
- Retourner le meilleur coup trouvé quand le temps est écoulé

---

## 🐛 Problèmes rencontrés et solutions

### Problème 1: Minimax trop lent

**Symptôme:** Une seule partie prenait >5 minutes
**Cause:** 196² = 38,000 positions à évaluer sans pruning
**Solution:** Implémenter alpha-beta pruning + tri des actions
**Leçon:** Toujours considérer la complexité algorithmique avant d'implémenter

### Problème 2: Déterminer qui maximise/minimise

**Symptôme:** Confusion sur quand utiliser max vs min
**Cause:** Le joueur qui appelle minimax veut maximiser SON score
**Solution:**

- Premier appel après mon coup → adversaire joue → `maximizing=False`
- Puis alterner à chaque profondeur
  **Leçon:** Dessiner l'arbre de jeu sur papier aide énormément

### Problème 3: Ordre des actions affecte le pruning

**Symptôme:** Temps de calcul très variable (19s à 50s)
**Cause:** Mauvais ordre = peu de coupures alpha-beta
**Solution:** Trier les actions par distance au centre
**Leçon:** L'ordre d'exploration est crucial pour alpha-beta

---

## 📝 Code final v0.5

**Structure:**

```
my_player.py (v0.5)
├── __init__: initialise piece_type, opponent_type, max_depth=2
├── compute_action: point d'entrée, lance alpha-beta sur chaque action
├── alphabeta: minimax avec élagage alpha-beta
├── evaluate: heuristique (distance_adversaire - ma_distance)
└── calculate_shortest_path: Dijkstra pour calculer distances
```

**Paramètres configurables:**

- `max_depth = 2`: profondeur de recherche
- Tri par centre: optimise le pruning

**Dépendances:**

```python
import numpy as np   # Pour matrices de distance
import heapq        # Pour Dijkstra (priority queue)
```

---

## 🎯 Objectifs atteints vs planifiés

| Objectif Semaine 3    | Statut | Résultat                          |
| --------------------- | ------ | --------------------------------- |
| Implémenter minimax   | ✅     | v0.4 fonctionnel mais trop lent   |
| Tester profondeur 1-2 | ✅     | Profondeur 2 nécessite alpha-beta |
| Battre greedy         | ✅     | 100% victoires                    |
| Temps <60s/partie     | ✅     | ~30s/partie en moyenne            |

**Objectifs dépassés:**

- 100% vs greedy (objectif était >50%)
- 100% vs random (objectif était >90%)
- Alpha-beta implémenté (prévu semaine 4)

---

## 🚀 Prochaines étapes (Semaine 4+)

### Optimisations envisageables

1. **Iterative deepening**

   - Augmenter profondeur tant qu'il reste du temps
   - Permet d'utiliser tout le budget de 15 min intelligemment

2. **Transposition table**

   - Cache les positions déjà évaluées
   - Évite de recalculer les mêmes sous-arbres

3. **Meilleur tri des actions**

   - Utiliser l'heuristique pour trier (pas juste distance au centre)
   - "Killer move heuristic": mémoriser les bons coups

4. **Améliorer l'heuristique**
   - Bonus pour contrôle du centre
   - Bonus pour groupes connectés
   - Pénalité pour pièces isolées

### Tests à faire

- [ ] Tester contre d'autres agents sur Abyss
- [ ] Mesurer précisément le nombre de nœuds explorés
- [ ] Comparer profondeur 2 vs 3 (avec iterative deepening)
- [ ] Identifier les types de positions où v0.5 pourrait perdre

---

## 💭 Réflexions finales

### Ce que j'ai appris

**Sur l'algorithme minimax:**

- Conceptuellement simple mais exponentiellement coûteux
- L'élagage alpha-beta est ESSENTIEL, pas optionnel
- L'ordre d'exploration impacte drastiquement la performance

**Sur le jeu Hex:**

- Profondeur 2 suffit pour battre un agent greedy
- L'anticipation (lookahead) est la clé pour gagner
- Un bon agent doit équilibrer offense et défense

**Sur le développement:**

- Tester tôt révèle les problèmes de performance
- La progression itérative (v0.1 → v0.5) permet de diagnostiquer
- Chaque optimisation doit être mesurée, pas assumée

### Comparaison avec les objectifs du projet

Selon le PDF du projet, l'approche "minimax avec bonne heuristique" est recommandée au niveau standard et a gagné le concours en 2021, 2022 et 2023. Ma v0.5 suit exactement cette approche:

- ✅ Minimax avec alpha-beta
- ✅ Heuristique basée sur shortest path (comme greedy mais bidirectionnelle)
- ✅ Gestion du temps acceptable

**Prochaine priorité:** Tester sur Abyss pour voir comment v0.5 se comporte contre de vrais adversaires.

---

## ⏱️ Temps passé

| Tâche                              | Temps     |
| ---------------------------------- | --------- |
| Théorie minimax (révision cours)   | ~1h       |
| Implémentation v0.4 (minimax)      | ~1h       |
| Diagnostic problème de performance | ~30min    |
| Implémentation v0.5 (alpha-beta)   | ~1h       |
| Tests et validation                | ~1h       |
| Documentation                      | ~1h       |
| **Total Semaine 3**                | **~5.5h** |

**Comparaison avec planning:** Prévu 12-15h, réalisé en ~5.5h grâce à la bonne préparation des semaines précédentes et l'aide de l'IA pour le debugging.
