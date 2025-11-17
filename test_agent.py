#!/usr/bin/env python3
"""
Script de test pour comparer les performances de deux agents Hex.
Lance plusieurs parties et compte les victoires.
"""

import subprocess
import sys
import time
from pathlib import Path

def run_single_game(agent1, agent2, game_num, verbose=False):
    """
    Lance UNE partie entre deux agents et retourne le gagnant.

    Args:
        agent1: Chemin vers le premier agent (jouera Rouge)
        agent2: Chemin vers le deuxième agent (jouera Bleu)
        game_num: Numéro de la partie (pour debug)
        verbose: Afficher les détails

    Returns:
        int: 1 si agent1 gagne, 2 si agent2 gagne, 0 si erreur/indéterminé
    """
    try:
        # Lancer la partie en mode headless (-g) sans enregistrement
        result = subprocess.run(
            ["python3", "main_hex.py", "-t", "local", agent1, agent2, "-g"],
            capture_output=True,
            text=True,
            timeout=180  # 3 minutes max
        )

        # Combiner stdout et stderr
        output = result.stdout + "\n" + result.stderr

        if verbose:
            print(f"\n--- Sortie partie {game_num} ---")
            print(output[-500:])
            print("--- Fin sortie ---")

        # Chercher le gagnant dans la sortie
        # Le système affiche le nom du joueur gagnant
        output_lower = output.lower()

        # Patterns de détection
        agent1_name = Path(agent1).stem.lower()
        agent2_name = Path(agent2).stem.lower()

        # Détecter les messages de victoire
        if any(word in output_lower for word in ['winner', 'won', 'wins', 'victoire', 'gagnant']):
            # Vérifier quel agent est mentionné
            lines = output.split('\n')
            for line in lines[-30:]:  # Chercher dans les dernières lignes
                line_lower = line.lower()
                if any(word in line_lower for word in ['winner', 'won', 'wins', 'victoire', 'gagnant']):
                    if agent1_name in line_lower or 'myagent' in line_lower or 'my_player' in line_lower:
                        return 1
                    elif agent2_name in line_lower:
                        return 2

        # Fallback: chercher les scores dans la sortie
        if 'score' in output_lower:
            # Essayer de parser les scores
            for line in output.split('\n')[-20:]:
                if '1.0' in line or '1' in line:
                    if 'player 1' in line.lower() or agent1_name in line.lower():
                        return 1
                    elif 'player 2' in line.lower() or agent2_name in line.lower():
                        return 2

        # Si on arrive ici, on n'a pas pu déterminer le gagnant
        if verbose:
            print(f"⚠️  Partie {game_num}: Impossible de déterminer le gagnant")
        return 0

    except subprocess.TimeoutExpired:
        print(f"⏱️  Partie {game_num}: Timeout (>3min)")
        return 0
    except Exception as e:
        print(f"❌ Partie {game_num}: Erreur - {e}")
        return 0


def test_agents(agent1, agent2, num_games=10, verbose=False):
    """
    Teste deux agents l'un contre l'autre.

    Args:
        agent1: Premier agent
        agent2: Deuxième agent
        num_games: Nombre de parties
        verbose: Mode verbeux

    Returns:
        tuple: (victoires_agent1, victoires_agent2, parties_indéterminées)
    """
    wins_agent1 = 0
    wins_agent2 = 0
    undetermined = 0

    agent1_name = Path(agent1).stem
    agent2_name = Path(agent2).stem

    print(f"\n{'='*70}")
    print(f"🎮 Test: {agent1_name} (Rouge) vs {agent2_name} (Bleu)")
    print(f"{'='*70}")

    for i in range(num_games):
        print(f"Partie {i+1}/{num_games}...", end=' ', flush=True)

        start_time = time.time()
        winner = run_single_game(agent1, agent2, i+1, verbose=verbose)
        elapsed = time.time() - start_time

        if winner == 1:
            wins_agent1 += 1
            print(f"✓ {agent1_name} gagne ({elapsed:.1f}s)")
        elif winner == 2:
            wins_agent2 += 1
            print(f"✓ {agent2_name} gagne ({elapsed:.1f}s)")
        else:
            undetermined += 1
            print(f"? Indéterminé ({elapsed:.1f}s)")

    print(f"\n{'='*70}")
    print(f"📊 Résultats:")
    print(f"  {agent1_name}: {wins_agent1}/{num_games} victoires ({wins_agent1/num_games*100:.1f}%)")
    print(f"  {agent2_name}: {wins_agent2}/{num_games} victoires ({wins_agent2/num_games*100:.1f}%)")
    if undetermined > 0:
        print(f"  ⚠️  Indéterminé: {undetermined}/{num_games}")
    print(f"{'='*70}\n")

    return wins_agent1, wins_agent2, undetermined


def test_both_orders(agent1, agent2, num_games_per_order=5):
    """
    Teste les deux agents dans les deux ordres pour compenser l'avantage du premier joueur.

    Args:
        agent1: Premier agent
        agent2: Deuxième agent
        num_games_per_order: Nombre de parties par configuration
    """
    print(f"\n{'#'*70}")
    print(f"# TEST COMPLET: {Path(agent1).stem} vs {Path(agent2).stem}")
    print(f"# {num_games_per_order} parties par configuration (total: {num_games_per_order*2})")
    print(f"{'#'*70}")

    # Configuration 1: agent1 commence (Rouge)
    print("\n📍 Configuration 1: agent1 joue Rouge (commence)")
    w1_a, w2_a, u_a = test_agents(agent1, agent2, num_games_per_order)

    # Configuration 2: agent2 commence (Rouge)
    print("\n📍 Configuration 2: agent2 joue Rouge (commence)")
    w2_b, w1_b, u_b = test_agents(agent2, agent1, num_games_per_order)

    # Totaux
    total_games = num_games_per_order * 2
    total_w1 = w1_a + w1_b
    total_w2 = w2_a + w2_b
    total_u = u_a + u_b

    print(f"\n{'#'*70}")
    print(f"# 📊 RÉSULTATS FINAUX")
    print(f"{'#'*70}")
    print(f"  {Path(agent1).stem}: {total_w1}/{total_games} victoires ({total_w1/total_games*100:.1f}%)")
    print(f"  {Path(agent2).stem}: {total_w2}/{total_games} victoires ({total_w2/total_games*100:.1f}%)")
    if total_u > 0:
        print(f"  ⚠️  Indéterminé: {total_u}/{total_games}")
    print(f"{'#'*70}\n")

    return total_w1, total_w2, total_u


if __name__ == "__main__":
    print("🎯 Script de test pour agents Hex\n")

    # Vérifier que les fichiers existent
    agents_to_test = [
        ("my_player.py", "random_player_hex.py"),
        ("my_player.py", "greedy_player_hex.py")
    ]

    for agent1, agent2 in agents_to_test:
        if not Path(agent1).exists():
            print(f"❌ Erreur: {agent1} n'existe pas!")
            sys.exit(1)
        if not Path(agent2).exists():
            print(f"❌ Erreur: {agent2} n'existe pas!")
            sys.exit(1)

    # Lancer les tests
    print("\n" + "="*70)
    print("TEST 1: My Player vs Random Player")
    print("="*70)
    test_both_orders("my_player.py", "random_player_hex.py", num_games_per_order=20)

    print("\n" + "="*70)
    print("TEST 2: My Player vs Greedy Player")
    print("="*70)
    test_both_orders("my_player.py", "greedy_player_hex.py", num_games_per_order=20)

    print("\n✅ Tests terminés!")