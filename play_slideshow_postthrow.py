import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.animation import FuncAnimation
import numpy as np

def play_post_simple(post_df, game_id, play_id):
    play_df = post_df[(post_df['game_id'] == game_id) & (post_df['play_id'] == play_id)]
    frame_ids = sorted(play_df['frame_id'].unique())
    
    if not frame_ids:
        print("No frames found for this play.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))

    def draw_frame(frame_index):
        ax.clear()
        frame_df = play_df[play_df['frame_id'] == frame_ids[frame_index]]
        if frame_df.empty:
            return

        # Field setup
        ax.set_xlim(0, 120)
        ax.set_ylim(0, 53.3)
        ax.set_facecolor('white')
        ax.set_title(f"Post-Throw | Game {game_id}, Play {play_id}, Frame {frame_ids[frame_index]}")

        # Players
        for _, row in frame_df.iterrows():
            ax.scatter(row['x'], row['y'], c='blue', marker='o', s=100, edgecolors='black')
            ax.text(row['x'], row['y'] - 2, f"{row['nfl_id']}", fontsize=6, ha='center')


    anim = FuncAnimation(fig, draw_frame, frames=len(frame_ids), interval=500, repeat=False)
    plt.show()