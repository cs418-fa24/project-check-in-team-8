import pandas as pd
import matplotlib.pyplot as plt

combined = pd.read_csv("combinedQBStats.csv")

qb_performance = combined.groupby("Name").agg(
    avg_QBR=("QBR", "mean"),
    avg_passing_yards=("Passing Yards", "mean"),
    draft_pick=("Draft Pick", "first"),
    win_rate=("Game Result (W/L)", lambda x: (x == "W").mean())
).reset_index()

plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    qb_performance["draft_pick"],
    qb_performance["avg_QBR"],
    s=qb_performance["avg_passing_yards"] * 0.5,  
    c=qb_performance["win_rate"], cmap="coolwarm", alpha=0.7
)

plt.colorbar(scatter, label="Win Rate")
plt.xlabel("Draft Pick")
plt.ylabel("Average QBR")
plt.title("Draft Pick vs. Average QBR with Passing Yards and Win Rate")

plt.grid(True)

plt.show()
