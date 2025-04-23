import pygambit as gbt
import itertools

# Define players and player-specific strategies
players = ["Player1", "Player2", "Player3"]
p1_actions = ["A1", "A2", "A3"]
p2_actions = ["B1", "B2", "B3"]
p3_actions = ["C1", "C2", "C3"]

# Base payoff matrix (strategy index to base payoff)
base_payoffs = {
    "Player1": [3, 5, 2],
    "Player2": [4, 1, 6],
    "Player3": [7, 3, 2]
}

# Helper: compute adjusted zero-sum payoffs
def adjusted_payoffs(p1_idx, p2_idx, p3_idx):
    raw = [
        base_payoffs["Player1"][p1_idx],
        base_payoffs["Player2"][p2_idx],
        base_payoffs["Player3"][p3_idx]
    ]
    avg = sum(raw) / 3
    return [round(p - avg, 2) for p in raw]

# Create a new extensive-form game tree
g = gbt.Game.new_tree(players=players, title="Three-player sequential zero-sum V1")

# Player1 chooses first
g.append_move(g.root, "Player1", p1_actions)

for i, node_p1 in enumerate(g.root.children):
    # Player2 acts second
    g.append_move(node_p1, "Player2", p2_actions)

    for j, node_p2 in enumerate(node_p1.children):
        # Player3 acts third
        g.append_move(node_p2, "Player3", p3_actions)

        for k, node_p3 in enumerate(node_p2.children):
            # Get adjusted zero-sum payoffs
            adj = adjusted_payoffs(i, j, k)
            label = f"Outcome_{p1_actions[i]}_{p2_actions[j]}_{p3_actions[k]}"
            g.set_outcome(node_p3, g.add_outcome(adj, label=label))

# # Print or save the game in EFG format
# efg_str = g.write(format='native')
# print(efg_str) 

# # Set your full export path
# # export_path = "/Users/yourname/Documents/games/three_player_zero_sum_game.efg"  # macOS/Linux
# export_path = r"C:\Research Game Data Generator\Generated_Data\EFG\3player_3action_v1.efg"  # Windows

# # Write to file
# with open(export_path, "w") as f:
#     f.write(g.write(format='efg'))
