import random
from player_hex import PlayerHex
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.game.light_action import LightAction

class MyPlayer(PlayerHex):
    """
    Mon premier agent pour Hex - Version 0.1
    Stratégie: aléatoire (pour tester que tout fonctionne)

    Attributes:
        piece_type (str): "R" ou "B"
    """

    def __init__(self, piece_type: str, name: str = "MyAgent_v0.1", *args) -> None:
        """
        Initialize the PlayerHex instance.

        Args:
            piece_type (str): Type of the player's game piece "R" or "B"
            name (str, optional): Name of the player
        """
        super().__init__(piece_type, name, *args)

    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Choisit une action aléatoire parmi les actions possibles.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: Randomly selected feasible action
        """
        possible_actions = list(current_state.get_possible_light_actions())
        chosen_action = random.choice(possible_actions)
        return chosen_action