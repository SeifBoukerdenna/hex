"""
Test suite for v0.4 Minimax agent
Place in Hex/ root folder and run: python test_v0_4.py
"""

import subprocess
import time
from pathlib import Path


def run_game(agent1, agent2, headless=True):
    """Run single game, return (winner: 1 or 2, duration)"""
    args = ["python3", "main_hex.py", "-t", "local", agent1, agent2]
    if headless:
        args.append("-g")

    start = time.time()
    result = subprocess.run(args, capture_output=True, text=True, timeout=300)
    duration = time.time() - start

    output = result.stdout + result.stderr
    agent1_name = Path(agent1).stem.lower()
    agent2_name = Path(agent2).stem.lower()

    # Detect winner
    for line in output.split("\n")[-30:]:
        line_lower = line.lower()
        if any(w in line_lower for w in ["winner", "won", "wins"]):
            if agent1_name in line_lower or "myagent" in line_lower:
                return 1, duration
            elif agent2_name in line_lower:
                return 2, duration
    return 0, duration


def test_matchup(agent1, agent2, num_games=5):
    """Test agent1 vs agent2"""
    name1 = Path(agent1).stem
    name2 = Path(agent2).stem

    print(f"\n{'=' * 50}")
    print(f"{name1} (Rouge) vs {name2} (Bleu)")
    print(f"{'=' * 50}")

    wins1, wins2 = 0, 0
    total_time = 0

    for i in range(num_games):
        print(f"  Partie {i + 1}/{num_games}...", end=" ", flush=True)
        winner, duration = run_game(agent1, agent2)
        total_time += duration

        if winner == 1:
            wins1 += 1
            print(f"✓ {name1} ({duration:.1f}s)")
        elif winner == 2:
            wins2 += 1
            print(f"✓ {name2} ({duration:.1f}s)")
        else:
            print(f"? Indéterminé ({duration:.1f}s)")

    print(f"\nRésultat: {name1} {wins1}/{num_games} | {name2} {wins2}/{num_games}")
    print(f"Temps moyen: {total_time / num_games:.1f}s par partie")

    return wins1, wins2, total_time / num_games


def main():
    print("=" * 60)
    print("TEST SUITE v0.4 - MINIMAX")
    print("=" * 60)

    games_per_config = 3  # Reduce if too slow

    results = {}

    # Test 1: v0.4 vs Random (both configs)
    print("\n" + "#" * 60)
    print("# TEST 1: my_player.py vs random_player_hex.py")
    print("#" * 60)

    w1, w2, t1 = test_matchup("my_player.py", "random_player_hex.py", games_per_config)
    w3, w4, t2 = test_matchup("random_player_hex.py", "my_player.py", games_per_config)

    results["vs_random"] = {
        "wins": w1 + w4,
        "total": games_per_config * 2,
        "avg_time": (t1 + t2) / 2,
    }

    # Test 2: v0.4 vs Greedy (both configs)
    print("\n" + "#" * 60)
    print("# TEST 2: my_player.py vs greedy_player_hex.py")
    print("#" * 60)

    w1, w2, t1 = test_matchup("my_player.py", "greedy_player_hex.py", games_per_config)
    w3, w4, t2 = test_matchup("greedy_player_hex.py", "my_player.py", games_per_config)

    results["vs_greedy"] = {
        "wins": w1 + w4,
        "total": games_per_config * 2,
        "avg_time": (t1 + t2) / 2,
    }

    # Summary
    print("\n" + "=" * 60)
    print("RÉSUMÉ v0.4 MINIMAX")
    print("=" * 60)

    for opponent, data in results.items():
        pct = data["wins"] / data["total"] * 100
        print(
            f"{opponent}: {data['wins']}/{data['total']} ({pct:.0f}%) - {data['avg_time']:.1f}s/partie"
        )

    print("\n⚠️  Si temps > 60s/partie, ajouter alpha-beta (semaine 4)")
    print("=" * 60)


if __name__ == "__main__":
    main()
