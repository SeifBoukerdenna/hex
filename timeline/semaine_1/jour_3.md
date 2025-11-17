### Jour 3: Regarder les agents fournis
- [x] Lancer random vs greedy plusieurs fois
  ```bash
  python main_hex.py -t local random_player_hex.py greedy_player_hex.py
  ```
- [x] Observer qui gagne et pourquoi
- [x] Jouer contre le greedy pour voir son comportement
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