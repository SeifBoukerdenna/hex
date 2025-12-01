"""
Test suite for v0.5 Alpha-Beta agent
Run: python test_v0_5.py
"""

import subprocess
import time
from pathlib import Path


def run_game(agent1, agent2):
    """Run single game, return (winner: 1 or 2, duration)"""
    args = ["python3", "main_hex.py", "-t", "local", agent1, agent2, "-g"]

    start = time.time()
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return 0, 300
    duration = time.time() - start

    output = result.stdout + result.stderr
    agent1_name = Path(agent1).stem.lower()
    agent2_name = Path(agent2).stem.lower()

    for line in output.split("\n")[-30:]:
        line_lower = line.lower()
        if any(w in line_lower for w in ["winner", "won", "wins"]):
            if agent1_name in line_lower or "myagent" in line_lower:
                return 1, duration
            elif agent2_name in line_lower:
                return 2, duration
    return 0, duration


def test_matchup(agent1, agent2, num_games):
    """Test agent1 vs agent2"""
    name1 = Path(agent1).stem
    name2 = Path(agent2).stem

    print(f"\n{name1} (Rouge) vs {name2} (Bleu)")
    print("-" * 40)

    wins1, wins2, times = 0, 0, []

    for i in range(num_games):
        print(f"  Partie {i + 1}/{num_games}...", end=" ", flush=True)
        winner, duration = run_game(agent1, agent2)
        times.append(duration)

        if winner == 1:
            wins1 += 1
            print(f"✓ {name1} ({duration:.1f}s)")
        elif winner == 2:
            wins2 += 1
            print(f"✓ {name2} ({duration:.1f}s)")
        else:
            print(f"? ({duration:.1f}s)")

    avg_time = sum(times) / len(times)
    print(f"→ {name1}: {wins1}/{num_games} | Temps moy: {avg_time:.1f}s")
    return wins1, wins2, avg_time


def main():
    print("=" * 50)
    print("TEST SUITE v0.5 - ALPHA-BETA")
    print("=" * 50)

    n = 5  # games per config

    # vs Random
    print("\n### vs RANDOM ###")
    r1, _, t1 = test_matchup("my_player.py", "random_player_hex.py", n)
    _, r2, t2 = test_matchup("random_player_hex.py", "my_player.py", n)

    # vs Greedy
    print("\n### vs GREEDY ###")
    g1, _, t3 = test_matchup("my_player.py", "greedy_player_hex.py", n)
    _, g2, t4 = test_matchup("greedy_player_hex.py", "my_player.py", n)

    # Summary
    print("\n" + "=" * 50)
    print("RÉSUMÉ FINAL")
    print("=" * 50)
    print(f"vs Random: {r1 + r2}/{n * 2} ({(r1 + r2) / (n * 2) * 100:.0f}%)")
    print(f"vs Greedy: {g1 + g2}/{n * 2} ({(g1 + g2) / (n * 2) * 100:.0f}%)")
    print(f"Temps moyen: {(t1 + t2 + t3 + t4) / 4:.1f}s/partie")
    print("=" * 50)


if __name__ == "__main__":
    main()
