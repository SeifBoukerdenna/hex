import random
import numpy as np
import heapq
from player_hex import PlayerHex
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.game.light_action import LightAction

class MyPlayer(PlayerHex):
    """
    Version 0.3 - Heuristique offensive + défensive

    Stratégie:
    - Calcule le plus court chemin pour MOI (offense)
    - Calcule le plus court chemin pour L'ADVERSAIRE (défense)
    - Score = distance_adversaire - ma_distance
    - Choisit le coup qui maximise ce score

    Plus le score est élevé, plus je suis en avance!
    Si score négatif = adversaire en avance → besoin de bloquer

    Attributes:
        piece_type (str): "R" ou "B"
    """

    def __init__(self, piece_type: str, name: str = "MyAgent_v0.3", *args) -> None:
        super().__init__(piece_type, name, *args)
        # Déterminer la couleur de l'adversaire
        self.opponent_type = "B" if self.piece_type == "R" else "R"

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Évalue chaque action selon une heuristique offensive + défensive.

        Pour chaque action possible:
        1. Simule le coup
        2. Calcule MA distance pour gagner
        3. Calcule la distance de L'ADVERSAIRE pour gagner
        4. Score = distance_adversaire - ma_distance
        5. Choisit le coup avec le MEILLEUR score

        Args:
            current_state (GameState): État actuel du jeu
            **kwargs: Arguments supplémentaires

        Returns:
            Action: Meilleure action selon l'heuristique
        """
        possible_actions = list(current_state.get_possible_light_actions())

        # Si une seule action, la jouer directement
        if len(possible_actions) == 1:
            return possible_actions[0]

        best_action = None
        best_score = float('-inf')  # On veut MAXIMISER le score

        # Évaluer chaque action
        for action in possible_actions:
            # Simuler le coup
            next_state = current_state.apply_action(action)

            # Calculer le score de cette position
            score = self.evaluate(next_state)

            # Garder la meilleure
            if score > best_score:
                best_score = score
                best_action = action

        return best_action if best_action else possible_actions[0]

    def evaluate(self, state: GameState) -> float:
        """
        Évalue une position avec heuristique offensive + défensive.

        Score = distance_adversaire - ma_distance

        - Score positif = je suis en avance (bon)
        - Score négatif = adversaire en avance (mauvais)
        - Score = 0 = égalité

        Args:
            state (GameState): État à évaluer

        Returns:
            float: Score de la position (plus grand = meilleur pour moi)
        """
        # Si la partie est finie, retourner score extrême
        if state.is_done():
            for player in state.players:
                if player.get_piece_type() == self.piece_type:
                    my_score = state.scores.get(player.get_id(), 0)
                    if my_score == 1.0:
                        return 10000  # J'ai gagné = excellent
                    else:
                        return -10000  # J'ai perdu = terrible

        # Calculer MA distance pour gagner
        my_distance = self.calculate_shortest_path(state, self.piece_type)

        # Calculer la distance de L'ADVERSAIRE pour gagner
        opponent_distance = self.calculate_shortest_path(state, self.opponent_type)

        # Heuristique: plus l'adversaire est loin, mieux c'est
        # Plus je suis proche, mieux c'est
        score = opponent_distance - my_distance

        return score

    def calculate_shortest_path(self, state: GameState, player_type: str) -> float:
        """
        Calcule le plus court chemin pour un joueur donné.
        Utilise Dijkstra.

        Args:
            state (GameState): État du jeu
            player_type (str): "R" ou "B" - pour quel joueur calculer

        Returns:
            float: Longueur du plus court chemin
        """
        env = state.get_rep().get_env()
        dimensions = state.get_rep().get_dimensions()

        # Matrices pour Dijkstra
        dist = np.full((dimensions[0], dimensions[1]), np.inf)
        visited = np.zeros((dimensions[0], dimensions[1]), dtype=bool)
        pq = []

        # Définir départ et arrivée selon la couleur
        if player_type == "R":
            # Rouge: de ligne 0 à ligne 13
            start_positions = [(0, j) for j in range(dimensions[1])]
            end_line = dimensions[0] - 1
            check_goal = lambda pos: pos[0] == end_line
        else:
            # Bleu: de colonne 0 à colonne 13
            start_positions = [(i, 0) for i in range(dimensions[0])]
            end_column = dimensions[1] - 1
            check_goal = lambda pos: pos[1] == end_column

        # Initialiser les positions de départ
        for pos in start_positions:
            piece = env.get(pos)
            if piece is None:
                dist[pos] = 1
                heapq.heappush(pq, (1, pos))
            elif piece.get_type() == player_type:
                dist[pos] = 0
                heapq.heappush(pq, (0, pos))
            # Pièce adverse: ne pas ajouter

        # Dijkstra
        while pq:
            d, current_pos = heapq.heappop(pq)

            if visited[current_pos]:
                continue

            visited[current_pos] = True

            # Si objectif atteint, retourner la distance
            if check_goal(current_pos):
                return d

            # Explorer les voisins
            neighbors = state.get_neighbours(current_pos[0], current_pos[1])
            for neighbor_type, neighbor_pos in neighbors.values():
                if neighbor_type == "OUTSIDE" or visited[neighbor_pos]:
                    continue

                # Calculer le coût
                if neighbor_type == "EMPTY":
                    new_dist = d + 1
                elif neighbor_type == player_type:
                    new_dist = d
                else:
                    continue  # Pièce adverse = bloqué

                # Mise à jour si meilleur chemin
                if new_dist < dist[neighbor_pos]:
                    dist[neighbor_pos] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor_pos))

        # Aucun chemin trouvé (complètement bloqué)
        return 999