### Jour 1-2: Agent version 0.1 - "juste qqch qui marche"

#### ✅ Tâches complétées
- [x] Copier la structure de `random_player_hex.py`
- [x] Créer `my_player.py` avec classe MyPlayer
- [x] Implémenter compute_action() version simple (aléatoire)
- [x] Tester que ça compile et joue sans crash
- [x] Créer script de test automatique `test_agent.py`
- [x] Lancer batterie de tests complète

---

#### 📊 Résultats détaillés des tests

**TEST 1: My Player vs Random Player (10 parties)**

Configuration 1 - Mon agent joue Rouge (commence en premier):
- Résultat: 4 victoires / 5 parties (80%)
- Temps moyen: ~2.3s par partie
- Observation: Quand je commence, je gagne la grande majorité du temps même en jouant aléatoirement!

Configuration 2 - Mon agent joue Bleu (joue en second):
- Résultat: 0 victoires / 5 parties (0%)
- Temps moyen: ~2.3s par partie
- Observation: Quand l'adversaire commence, je perds systématiquement même contre un agent aléatoire

**Résultat global: 4/10 victoires (40%)**

**TEST 2: My Player vs Greedy Player (10 parties)**

Configuration 1 - Mon agent joue Rouge (commence en premier):
- Résultat: 0 victoires / 5 parties (0%)
- Temps moyen: ~0.5s par partie
- Observation: Greedy me massacre ultra rapidement, même avec l'avantage du premier joueur

Configuration 2 - Mon agent joue Bleu (joue en second):
- Résultat: 0 victoires / 5 parties (0%)
- Temps moyen: ~0.6s par partie
- Observation: Aucune différence, greedy domine complètement

**Résultat global: 0/10 victoires (0%)**

---

#### 🤔 Analyse et réflexions

**1. L'avantage du premier joueur est MASSIF**

Ce qui m'a le plus surpris, c'est l'écart gigantesque entre jouer Rouge vs Bleu:
- Rouge (premier): 80% de victoires contre random
- Bleu (second): 0% de victoires contre random

Ça veut dire que dans Hex, commencer en premier donne un avantage énorme, même avec deux agents totalement aléatoires. C'est un peu comme si aux échecs, les blancs gagnaient 80% du temps contre un adversaire de même niveau.

**Pourquoi cet avantage existe?**
- Le premier joueur peut immédiatement prendre des positions centrales stratégiques
- Le second joueur est toujours en mode "réaction" et doit défendre
- Dans Hex, il ne peut pas y avoir d'égalité, donc quelqu'un DOIT gagner
- Statistiquement, celui qui pose la première pièce a plus de chances de construire son chemin en premier

**Implication pour mon agent:**
- Je ne peux PAS me fier uniquement aux résultats où je joue en premier
- Un bon agent doit pouvoir gagner même en jouant Bleu (second)
- Dans mes futurs tests, je DOIS toujours tester les deux configurations
- Le vrai test de qualité = performance quand je joue en SECOND

**2. Greedy est dans une autre ligue**

Contre greedy, même l'avantage du premier joueur ne sert à rien:
- 0/10 victoires, que je commence ou pas
- Les parties sont ultra-rapides (~0.5s vs ~2.3s contre random)
- Ça montre qu'avoir une STRATÉGIE (même basique) >> jouer au hasard

**Pourquoi greedy domine autant?**
- Il a un plan: calculer le plus court chemin et le suivre
- Chaque coup a un sens et contribue à son objectif
- Même sans défense, juste avoir une direction cohérente suffit à écraser le random
- Mes coups aléatoires ne créent jamais de menace réelle

**Vitesse des parties:**
- Greedy gagne tellement vite que les parties durent 0.5s
- Contre random, les parties durent 2.3s (plus de coups joués)
- Ça suggère que greedy gagne rapidement sans laisser traîner

**3. Mon agent aléatoire comme baseline**

Résultat 40% contre random peut sembler "pas si mal", mais c'est trompeur:
- 80% vient uniquement de l'avantage du premier joueur
- 0% en jouant second montre qu'il n'y a AUCUNE stratégie
- Un agent "neutre" devrait faire 50-50 contre random
- Mon 40% est en fait 40% à cause de l'asymétrie Rouge/Bleu

**Ce que je peux en tirer:**
- Baseline établie: je sais maintenant ce que représente "aucune stratégie"
- Objectif clair: ma prochaine version DOIT faire mieux que 40% vs random
- Benchmark: greedy fait 100% vs random (mon objectif ultime)
- Première étape réaliste: viser 70-80% vs random (dans les deux configs)

---

#### 💡 Insights et apprentissages

**Sur l'importance de la méthodologie de test:**

Au début, j'avais un script de test qui disait que mon agent random battait greedy 100% du temps - IMPOSSIBLE! Ça m'a forcé à:
1. Débugger mon script de test
2. Comprendre comment détecter le gagnant correctement
3. Réaliser l'importance de tester les deux configurations (Rouge/Bleu)
4. Créer un script robuste qui affiche les vrais résultats

**Leçon:** Avant de faire confiance aux résultats, il faut vérifier manuellement que le système de test fonctionne bien.

**Sur la différence entre "marcher" et "bien jouer":**

Version 0.1 "marche" techniquement:
- Pas de crash ✓
- Joue des coups légaux ✓
- Finit les parties ✓

Mais elle ne "joue" pas vraiment:
- Aucune stratégie ✗
- Aucune conscience du but ✗
- Équivalent d'un singe qui appuie sur des boutons ✗

**Leçon:** Il y a un fossé énorme entre "code qui tourne" et "IA qui réfléchit".

**Sur la valeur du greedy comme référence:**

Greedy m'a appris que:
- Même un algo simple (Dijkstra + jouer au centre) est TRÈS efficace
- On n'a pas besoin de minimax ou MCTS pour battre le random
- Juste avoir un "plan" (même basique) change tout
- La prochaine étape logique = copier l'approche du greedy

---

#### 🎯 Plan d'action pour la suite

**Objectifs à court terme (Version 0.2):**

1. **Implémenter une heuristique basique inspirée du greedy**
   - Calculer le plus court chemin pour connecter mes deux côtés
   - Jouer sur ce chemin (comme greedy)
   - Objectif: battre random de façon consistante

2. **Critère de succès Version 0.2:**
   - Minimum: >70% contre random (dans les deux configurations)
   - Stretch goal: >80% contre random
   - Test: Toujours 0% contre greedy (normal, on copie juste son approche)

**Objectifs à moyen terme (Version 0.3):**

1. **Ajouter une dimension défensive**
   - Calculer AUSSI le chemin adverse le plus court
   - Si adversaire est plus proche de gagner que moi → BLOQUER
   - C'est la faiblesse principale du greedy

2. **Critère de succès Version 0.3:**
   - >90% contre random
   - >10% contre greedy (commencer à exploiter sa faiblesse)
   - Devrait pouvoir battre greedy quand il est distrait/bloqué

**Approche générale:**

Progression par étapes:
1. Version 0.1: Random (baseline) ✓
2. Version 0.2: Offense pure (copier greedy)
3. Version 0.3: Offense + Défense basique
4. Version 0.4: Minimax profondeur 1
5. Version 0.5+: Minimax + alpha-beta + optimisations

**Pourquoi cette approche progressive?**
- Je peux tester et valider chaque amélioration séparément
- Si quelque chose casse, je sais exactement ce qui a changé
- Je construis progressivement ma compréhension
- Chaque version est fonctionnelle et testable

---

#### 🐛 Problèmes rencontrés et solutions

**Problème 1: Script de test initial défaillant**
- Symptôme: Affichait que random battait greedy 100%
- Cause: Mauvaise détection du gagnant dans la sortie
- Solution: Réécriture complète avec meilleure parsing + test manuel
- Leçon: Toujours valider les tests manuellement avant de faire confiance

**Problème 2: Comprendre l'avantage du premier joueur**
- Symptôme: Résultats très asymétriques (80% vs 0%)
- Cause: Ne testais qu'une configuration initialement
- Solution: Tester les deux ordres systématiquement
- Leçon: Hex n'est pas un jeu symétrique!

**Problème 3: Prints de debug ralentissaient les tests**
- Symptôme: Parties prenaient plus de temps avec output
- Solution: Version "silencieuse" de my_player.py pour les tests
- Note: Garder version avec prints pour debug individuel

---

#### 📝 Notes techniques importantes

**Structure du code actuelle:**
```python
class MyPlayer(PlayerHex):
    def __init__(self, piece_type, name="MyAgent_v0.1"):
        super().__init__(piece_type, name)

    def compute_action(self, current_state, **kwargs):
        possible_actions = list(current_state.get_possible_light_actions())
        return random.choice(possible_actions)
```

**Ce qui fonctionne bien:**
- Structure claire et simple
- Héritage correct de PlayerHex
- Utilisation correcte de get_possible_light_actions()
- Retourne bien une LightAction valide

**Ce qui doit être amélioré (v0.2):**
- Remplacer `random.choice()` par une vraie décision
- Ajouter une fonction `evaluate()` pour scorer les positions
- Implémenter un Dijkstra simple pour trouver le plus court chemin
- Garder la structure simple pour l'instant (pas de minimax encore)

**Dépendances à ajouter pour v0.2:**
```python
import numpy as np  # Pour matrices de distance
import heapq       # Pour Dijkstra (priority queue)
```

---

#### ⏱️ Gestion du temps

**Temps passé sur v0.1:**
- Setup et compréhension du code: ~2h
- Création de my_player.py: ~30min
- Debugging du script de test: ~1h
- Tests et analyse: ~30min
- **Total: ~4h**

**Temps estimé pour v0.2:**
- Implémenter Dijkstra: ~2h
- Adapter pour Hex (6 voisins): ~1h
- Tests et debug: ~1h
- **Total estimé: ~4h**

**Reste dans le planning:** Largement dans les temps pour la semaine 2!

---

#### 🚀 Prochaines étapes immédiates

1. [ ] Étudier en détail le code de `greedy_player_hex.py`
2. [ ] Comprendre comment son Dijkstra fonctionne exactement
3. [ ] Implémenter ma propre version de Dijkstra
4. [ ] Tester sur des cas simples (plateau 5x5)
5. [ ] Intégrer dans my_player.py
6. [ ] Tester contre random et comparer avec v0.1
7. [ ] Documenter les résultats

**Question à explorer:**
- Pourquoi greedy joue au centre du chemin? Est-ce vraiment optimal?
- Est-ce que je dois jouer exactement au centre ou il y a une meilleure heuristique?
- Comment gérer le cas où plusieurs chemins ont la même longueur?

---

#### 📚 Ressources et références

**Code à étudier:**
- `greedy_player_hex.py` - Mon principal modèle pour v0.2
- `game_state_hex.py` - Fonction `compute_scores()` montre comment détecter victoire avec DFS
- `board_hex.py` - Fonction `get_neighbours()` essentielle pour Dijkstra

**Concepts à maîtriser:**
- Algorithme de Dijkstra (plus court chemin)
- Graphes hexagonaux (6 voisins au lieu de 4 ou 8)
- Priority queue avec heapq
- DFS/BFS pour vérifier connectivité

**Métriques à suivre:**
- Taux de victoire vs random (config 1 et 2)
- Taux de victoire vs greedy (objectif futur)
- Temps moyen par coup (doit rester <1s pour l'instant)
- Nombre de coups pour gagner (plus court = meilleur)

---

#### 💭 Réflexions finales

Ce premier agent, bien que trivial, était une étape cruciale:
- J'ai un environnement de test qui fonctionne
- Je comprends la structure du code et l'API
- J'ai une baseline pour mesurer les progrès futurs
- J'ai découvert l'importance de l'avantage du premier joueur

La différence entre 0.5s (greedy) et 2.3s (random vs random) montre qu'il y a un fossé ÉNORME entre "avoir un plan" et "jouer au hasard". Ma prochaine version doit franchir ce fossé.

**Citation qui résume bien:**
> "Un mauvais plan vaut mieux que pas de plan du tout"

Greedy a un plan (même sans défense), random n'en a pas. Version 0.2 aura un plan!