import random
import numpy as np
import heapq
from player_hex import PlayerHex
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.game.light_action import LightAction

class MyPlayer(PlayerHex):
    """
    Version 0.2 - Heuristique basique: plus court chemin

    Stratégie: Greedy - joue toujours le coup qui minimise la distance pour gagner

    Attributes:
        piece_type (str): "R" ou "B"
    """

    def __init__(self, piece_type: str, name: str = "MyAgent_v0.2", *args) -> None:
        super().__init__(piece_type, name, *args)

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Version GREEDY SIMPLE: choisit directement sur le chemin le plus court.
        Copie exactement la logique de greedy_player_hex.py
        """
        possible_actions = current_state.get_possible_light_actions()

        # Exactement comme greedy: calculer le chemin optimal
        env = current_state.rep.env
        dist = np.full((current_state.rep.dimensions[0], current_state.rep.dimensions[1]), np.inf)
        preds = np.full((current_state.rep.dimensions[0], current_state.rep.dimensions[1]), None, dtype=object)
        objectives = []
        pq = []

        if self.piece_type == "R":
            # Rouge: connecter ligne 0 à ligne 13
            for j in range(current_state.rep.dimensions[1]):
                objectives.append((current_state.rep.dimensions[0]-1, j))
                if env.get((0,j)) is None:
                    dist[0, j] = 1
                elif env.get((0,j)).piece_type == "R":
                    dist[0, j] = 0
                else:
                    continue
                heapq.heappush(pq, (dist[0, j], (0, j), None))
        else:
            # Bleu: connecter colonne 0 à colonne 13
            for i in range(current_state.rep.dimensions[0]):
                objectives.append((i, current_state.rep.dimensions[1]-1))
                if env.get((i,0)) is None:
                    dist[i, 0] = 1
                elif env.get((i,0)).piece_type == "B":
                    dist[i, 0] = 0
                else:
                    continue
                heapq.heappush(pq, (dist[i, 0], (i, 0), None))

        # Dijkstra
        path = []
        while len(pq) != 0:
            d, (i, j), pred = heapq.heappop(pq)
            if d > dist[i, j]:
                continue
            preds[i,j] = pred
            if (i,j) in objectives:
                path = self.retrace_path(preds, (i,j))
                break
            for n_type, (ni, nj) in current_state.rep.get_neighbours(i, j).values():
                if n_type == "EMPTY":
                    new_dist = d + 1
                elif n_type == self.piece_type:
                    new_dist = d
                else:
                    continue
                if new_dist < dist[ni, nj]:
                    dist[ni, nj] = new_dist
                    heapq.heappush(pq, (new_dist, (ni, nj), (i, j)))

        # Choisir une case vide sur le chemin, au plus proche du centre
        hq = []
        for pos in path:
            if env.get(pos) == None:
                heapq.heappush(hq, (abs(pos[0]-6.5) + abs(pos[1]-6.5), pos))

        if hq:
            _ , pos = heapq.heappop(hq)
            return LightAction({"piece": self.piece_type, "position": pos})
        else:
            # Fallback si aucune case sur le chemin
            return random.choice(list(possible_actions))

    def retrace_path(self, preds, end):
        """Reconstruit le chemin depuis les prédécesseurs"""
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = preds[current]
        return path