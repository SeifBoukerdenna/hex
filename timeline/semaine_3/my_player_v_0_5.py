import random
import numpy as np
import heapq
from player_hex import PlayerHex
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.game.light_action import LightAction


class MyPlayer(PlayerHex):
    """
    Version 0.5 - Minimax + Alpha-Beta Pruning

    Optimisation: coupe les branches inutiles pour aller plus vite
    """

    def __init__(self, piece_type: str, name: str = "MyAgent_v0.5", *args) -> None:
        super().__init__(piece_type, name, *args)
        self.opponent_type = "B" if self.piece_type == "R" else "R"
        self.max_depth = 2

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        possible_actions = list(current_state.get_possible_light_actions())

        if len(possible_actions) == 1:
            return possible_actions[0]

        # Trier les actions: priorité au centre (meilleur pour alpha-beta)
        possible_actions.sort(
            key=lambda a: abs(a.data["position"][0] - 6.5)
            + abs(a.data["position"][1] - 6.5)
        )

        best_action = None
        best_score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for action in possible_actions:
            next_state = current_state.apply_action(action)
            score = self.alphabeta(next_state, self.max_depth - 1, alpha, beta, False)

            if score > best_score:
                best_score = score
                best_action = action

            alpha = max(alpha, score)

        return best_action if best_action else possible_actions[0]

    def alphabeta(
        self, state: GameState, depth: int, alpha: float, beta: float, maximizing: bool
    ) -> float:
        """
        Minimax avec élagage alpha-beta.
        Coupe les branches qu'on sait déjà ne pas être optimales.
        """
        if depth == 0 or state.is_done():
            return self.evaluate(state)

        possible_actions = list(state.get_possible_light_actions())

        if not possible_actions:
            return self.evaluate(state)

        # Trier pour améliorer le pruning
        possible_actions.sort(
            key=lambda a: abs(a.data["position"][0] - 6.5)
            + abs(a.data["position"][1] - 6.5)
        )

        if maximizing:
            max_eval = float("-inf")
            for action in possible_actions:
                next_state = state.apply_action(action)
                eval_score = self.alphabeta(next_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Coupe beta
            return max_eval
        else:
            min_eval = float("inf")
            for action in possible_actions:
                next_state = state.apply_action(action)
                eval_score = self.alphabeta(next_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Coupe alpha
            return min_eval

    def evaluate(self, state: GameState) -> float:
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
