import random
import numpy as np
import heapq
from player_hex import PlayerHex
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.game.light_action import LightAction


class MyPlayer(PlayerHex):
    """
    Version 0.4 - Minimax avec heuristique offensive + défensive

    Stratégie:
    - Minimax pour regarder plusieurs coups en avance
    - Heuristique: distance_adversaire - ma_distance
    - Profondeur configurable (commence à 2)

    Attributes:
        piece_type (str): "R" ou "B"
    """

    def __init__(self, piece_type: str, name: str = "MyAgent_v0.4", *args) -> None:
        super().__init__(piece_type, name, *args)
        self.opponent_type = "B" if self.piece_type == "R" else "R"
        self.max_depth = 2  # Profondeur de recherche (ajustable)

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Utilise minimax pour choisir la meilleure action.
        """
        possible_actions = list(current_state.get_possible_light_actions())

        if len(possible_actions) == 1:
            return possible_actions[0]

        best_action = None
        best_score = float("-inf")

        for action in possible_actions:
            next_state = current_state.apply_action(action)

            # Minimax: on vient de jouer, c'est au tour de l'adversaire (minimizing)
            score = self.minimax(next_state, self.max_depth - 1, False)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action if best_action else possible_actions[0]

    def minimax(self, state: GameState, depth: int, maximizing: bool) -> float:
        """
        Algorithme Minimax classique.

        Args:
            state: État du jeu actuel
            depth: Profondeur restante à explorer
            maximizing: True si c'est mon tour (maximiser), False si adversaire (minimiser)

        Returns:
            float: Score évalué de la position
        """
        # Cas terminal: partie finie ou profondeur atteinte
        if depth == 0 or state.is_done():
            return self.evaluate(state)

        possible_actions = list(state.get_possible_light_actions())

        if not possible_actions:
            return self.evaluate(state)

        if maximizing:
            # Mon tour: je veux MAXIMISER mon score
            max_eval = float("-inf")
            for action in possible_actions:
                next_state = state.apply_action(action)
                eval_score = self.minimax(next_state, depth - 1, False)
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            # Tour adversaire: il veut MINIMISER mon score
            min_eval = float("inf")
            for action in possible_actions:
                next_state = state.apply_action(action)
                eval_score = self.minimax(next_state, depth - 1, True)
                min_eval = min(min_eval, eval_score)
            return min_eval

    def evaluate(self, state: GameState) -> float:
        """
        Évalue une position: score = distance_adversaire - ma_distance
        """
        if state.is_done():
            for player in state.players:
                if player.get_piece_type() == self.piece_type:
                    if state.scores.get(player.get_id(), 0) == 1.0:
                        return 10000
                    else:
                        return -10000

        my_distance = self.calculate_shortest_path(state, self.piece_type)
        opponent_distance = self.calculate_shortest_path(state, self.opponent_type)

        return opponent_distance - my_distance

    def calculate_shortest_path(self, state: GameState, player_type: str) -> float:
        """
        Calcule le plus court chemin pour un joueur (Dijkstra).
        """
        env = state.get_rep().get_env()
        dimensions = state.get_rep().get_dimensions()

        dist = np.full((dimensions[0], dimensions[1]), np.inf)
        visited = np.zeros((dimensions[0], dimensions[1]), dtype=bool)
        pq = []

        if player_type == "R":
            start_positions = [(0, j) for j in range(dimensions[1])]
            check_goal = lambda pos: pos[0] == dimensions[0] - 1
        else:
            start_positions = [(i, 0) for i in range(dimensions[0])]
            check_goal = lambda pos: pos[1] == dimensions[1] - 1

        for pos in start_positions:
            piece = env.get(pos)
            if piece is None:
                dist[pos] = 1
                heapq.heappush(pq, (1, pos))
            elif piece.get_type() == player_type:
                dist[pos] = 0
                heapq.heappush(pq, (0, pos))

        while pq:
            d, current_pos = heapq.heappop(pq)

            if visited[current_pos]:
                continue
            visited[current_pos] = True

            if check_goal(current_pos):
                return d

            neighbors = state.get_neighbours(current_pos[0], current_pos[1])
            for neighbor_type, neighbor_pos in neighbors.values():
                if neighbor_type == "OUTSIDE" or visited[neighbor_pos]:
                    continue

                if neighbor_type == "EMPTY":
                    new_dist = d + 1
                elif neighbor_type == player_type:
                    new_dist = d
                else:
                    continue

                if new_dist < dist[neighbor_pos]:
                    dist[neighbor_pos] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor_pos))

        return 999
