import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.animation import FuncAnimation
import numpy as np

def play_slideshow_prethrow(df, game_id, play_id):
    play_df = df[(df['game_id'] == game_id) & (df['play_id'] == play_id)]
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

        los = frame_df['absolute_yardline_number'].iloc[0]
        play_direction = frame_df['play_direction'].iloc[0].lower()
        ball_x, ball_y = frame_df[['ball_land_x', 'ball_land_y']].iloc[0]

        # Field setup
        ax.set_xlim(0, 120)
        ax.set_ylim(0, 53.3)
        ax.set_facecolor('white')
        ax.set_title(f"File: {df.attrs.get('source_file','?')} | Game {game_id}, Play {play_id}, Frame {frame_ids[frame_index]}")

        # Players
        for _, row in frame_df.iterrows():
            color = 'blue' if row['player_side'] == 'Offense' else 'red'
            marker = 'o' if row['player_to_predict'] else 'x'

            ax.scatter(row['x'], row['y'], c=color, marker=marker, s=100, edgecolors='black')

            # Speed above head
            ax.text(row['x'], row['y'] + 1, f"{row['s']:.1f}", fontsize=6, ha='center')

            # Name + position under
            ax.text(row['x'], row['y'] - 2, f"{row['player_name']} ({row['player_position']})",
                    fontsize=6, ha='center')

            # Motion arrow (scaled by acceleration)
            if not np.isnan(row['dir']):
                angle_rad = np.deg2rad(90 - row['dir'])
                length = max(abs(row['a']), 0.2)
                dx, dy = np.cos(angle_rad) * length, np.sin(angle_rad) * length
                arrow_color = 'green' if row['a'] > 0 else 'red'
                ax.arrow(row['x'], row['y'], dx, dy,
                         head_width=1, head_length=1.5,
                         fc=arrow_color, ec=arrow_color,
                         alpha=0.7, linewidth=1)

        # Line of scrimmage
        ax.axvline(x=los, color='yellow', linestyle='--', linewidth=2)

        # Ball
        ball = Ellipse((ball_x, ball_y), width=2, height=1, color='saddlebrown', alpha=0.9)
        ax.add_patch(ball)
        ax.text(ball_x, ball_y + 1, "Ball Land", fontsize=8, ha='center', color='saddlebrown')

        # Play direction arrow
        arrow_dx = 20 if play_direction == 'right' else -20
        ax.arrow(60, 53.3 / 2, arrow_dx, 0,
                 head_width=3, head_length=5,
                 fc='grey', ec='grey', alpha=0.8, linewidth=3)

        # Role box sidebar
        role_text = "\n".join([f"{row['player_name']} - {row['player_role']}"
                               for _, row in frame_df.iterrows()])
        ax.text(121, 50, role_text, fontsize=8, va='top', ha='left',
                bbox=dict(facecolor='lightgrey', alpha=0.5))

    anim = FuncAnimation(fig, draw_frame, frames=len(frame_ids), interval=200, repeat=False)
    plt.show()
