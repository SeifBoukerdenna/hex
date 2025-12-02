# ============================================================================
# INF8175 - Projet Hex
# Matricule 1: 2206304
# Matricule 2: 2205281
# ============================================================================

import numpy as np
import heapq
import time
from player_hex import PlayerHex
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.game.light_action import LightAction


class MyPlayer(PlayerHex):
    """
    Agent Hex utilisant Minimax avec Alpha-Beta Pruning et Iterative Deepening.

    Stratégie:
    - Heuristique: différence des plus courts chemins (adversaire - moi)
    - Alpha-beta pruning pour optimiser la recherche
    - Iterative deepening pour gérer le temps efficacement
    - Tri des actions par proximité au centre pour améliorer le pruning
    """

    def __init__(self, piece_type: str, name: str = "MyAgent", *args) -> None:
        super().__init__(piece_type, name, *args)
        self.opponent_type = "B" if self.piece_type == "R" else "R"
        self.max_depth = 10
        self.time_per_move = 5.0

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Sélectionne la meilleure action via iterative deepening + alpha-beta.
        """
        possible_actions = list(current_state.get_possible_light_actions())

        if len(possible_actions) == 1:
            return possible_actions[0]

        # Tri des actions: centre d'abord (améliore alpha-beta)
        possible_actions.sort(
            key=lambda a: abs(a.data["position"][0] - 6.5)
            + abs(a.data["position"][1] - 6.5)
        )

        start_time = time.time()
        best_action = possible_actions[0]

        # Iterative deepening
        for depth in range(1, self.max_depth + 1):
            try:
                current_best_action = None
                current_best_score = float("-inf")
                alpha = float("-inf")
                beta = float("inf")

                for action in possible_actions:
                    if time.time() - start_time > self.time_per_move:
                        raise TimeoutError()

                    next_state = current_state.apply_action(action)
                    score = self._alphabeta(
                        next_state, depth - 1, alpha, beta, False, start_time
                    )

                    if score > current_best_score:
                        current_best_score = score
                        current_best_action = action

                    alpha = max(alpha, score)

                if current_best_action:
                    best_action = current_best_action

            except TimeoutError:
                break

        return best_action

    def _alphabeta(
        self,
        state: GameState,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
        start_time: float,
    ) -> float:
        """
        Minimax avec élagage alpha-beta.
        """
        if time.time() - start_time > self.time_per_move:
            raise TimeoutError()

        if depth == 0 or state.is_done():
            return self._evaluate(state)

        possible_actions = list(state.get_possible_light_actions())

        if not possible_actions:
            return self._evaluate(state)

        possible_actions.sort(
            key=lambda a: abs(a.data["position"][0] - 6.5)
            + abs(a.data["position"][1] - 6.5)
        )

        if maximizing:
            max_eval = float("-inf")
            for action in possible_actions:
                next_state = state.apply_action(action)
                eval_score = self._alphabeta(
                    next_state, depth - 1, alpha, beta, False, start_time
                )
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for action in possible_actions:
                next_state = state.apply_action(action)
                eval_score = self._alphabeta(
                    next_state, depth - 1, alpha, beta, True, start_time
                )
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def _evaluate(self, state: GameState) -> float:
        """
        Heuristique: distance_adversaire - ma_distance
        Plus le score est élevé, meilleure est la position pour moi.
        """
        if state.is_done():
            my_id = None
            for player in state.players:
                if (
                    hasattr(player, "piece_type")
                    and player.piece_type == self.piece_type
                ):
                    my_id = player.get_id()
                    break
            if my_id and state.scores.get(my_id, 0) == 1.0:
                return 10000
            return -10000

        my_distance = self._shortest_path(state, self.piece_type)
        opponent_distance = self._shortest_path(state, self.opponent_type)
        return opponent_distance - my_distance

    def _shortest_path(self, state: GameState, player_type: str) -> float:
        """
        Calcule le plus court chemin via Dijkstra.
        Coût: 0 pour cases déjà occupées, 1 pour cases vides.
        """
        env = state.rep.env
        dim = state.rep.dimensions

        dist = np.full((dim[0], dim[1]), np.inf)
        visited = np.zeros((dim[0], dim[1]), dtype=bool)
        pq = []

        if player_type == "R":
            start_positions = [(0, j) for j in range(dim[1])]
            end_row = dim[0] - 1
        else:
            start_positions = [(i, 0) for i in range(dim[0])]
            end_col = dim[1] - 1

        for pos in start_positions:
            piece = env.get(pos)
            if piece is None:
                dist[pos] = 1
                heapq.heappush(pq, (1, pos))
            elif piece.piece_type == player_type:
                dist[pos] = 0
                heapq.heappush(pq, (0, pos))

        while pq:
            d, current_pos = heapq.heappop(pq)
            if visited[current_pos]:
                continue
            visited[current_pos] = True

            if player_type == "R" and current_pos[0] == end_row:
                return d
            if player_type == "B" and current_pos[1] == end_col:
                return d

            for n_type, (ni, nj) in state.rep.get_neighbours(
                current_pos[0], current_pos[1]
            ).values():
                if n_type == "OUTSIDE" or visited[(ni, nj)]:
                    continue
                if n_type == "EMPTY":
                    new_dist = d + 1
                elif n_type == player_type:
                    new_dist = d
                else:
                    continue
                if new_dist < dist[(ni, nj)]:
                    dist[(ni, nj)] = new_dist
                    heapq.heappush(pq, (new_dist, (ni, nj)))

        return 999
