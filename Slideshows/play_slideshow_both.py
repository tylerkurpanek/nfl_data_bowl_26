import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.animation import FuncAnimation
import numpy as np

def play_full_slideshow(pre_df, post_df, game_id, play_id):
    # Pre-throw and post-throw data
    pre_play_df = pre_df[(pre_df['game_id'] == game_id) & (pre_df['play_id'] == play_id)]
    post_play_df = post_df[(post_df['game_id'] == game_id) & (post_df['play_id'] == play_id)]

    pre_frames = sorted(pre_play_df['frame_id'].unique())
    post_frames = sorted(post_play_df['frame_id'].unique())

    if not pre_frames and not post_frames:
        print("No frames found for this play.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))

    # Ball location from pre-throw to keep fixed
    if not pre_play_df.empty:
        ball_x, ball_y = pre_play_df[['ball_land_x', 'ball_land_y']].iloc[0]
    else:
        ball_x, ball_y = 60, 26.65  # fallback in the middle of field

    # Combine frames
    all_frames = [('pre', f) for f in pre_frames] + [('post', f) for f in post_frames]

    def draw_frame(frame_index):
        ax.clear()
        phase, frame_id = all_frames[frame_index]

        if phase == 'pre':
            frame_df = pre_play_df[pre_play_df['frame_id'] == frame_id]
            if frame_df.empty:
                return

            los = frame_df['absolute_yardline_number'].iloc[0]
            play_direction = frame_df['play_direction'].iloc[0].lower()

            ax.set_title(f"Pre-Throw | Game {game_id}, Play {play_id}, Frame {frame_id}")

            # Players with arrows, speed, role, etc.
            for _, row in frame_df.iterrows():
                color = 'blue' if row['player_side'] == 'Offense' else 'red'
                marker = 'o' if row['player_to_predict'] else 'x'

                ax.scatter(row['x'], row['y'], c=color, marker=marker, s=100, edgecolors='black')
                ax.text(row['x'], row['y'] + 1, f"{row['s']:.1f}", fontsize=6, ha='center')
                ax.text(row['x'], row['y'] - 2, f"{row['player_name']} ({row['player_position']})", fontsize=6, ha='center')

                if not np.isnan(row['dir']):
                    angle_rad = np.deg2rad(90 - row['dir'])
                    length = max(abs(row['a']), 0.2)
                    dx, dy = np.cos(angle_rad) * length, np.sin(angle_rad) * length
                    arrow_color = 'green' if row['a'] > 0 else 'red'
                    ax.arrow(row['x'], row['y'], dx, dy, head_width=1, head_length=1.5,
                             fc=arrow_color, ec=arrow_color, alpha=0.7, linewidth=1)

            ax.axvline(x=los, color='yellow', linestyle='--', linewidth=2)

            # Ball (fixed)
            ball = Ellipse((ball_x, ball_y), width=2, height=1, color='saddlebrown', alpha=0.9)
            ax.add_patch(ball)
            ax.text(ball_x, ball_y + 1, "Ball Land", fontsize=8, ha='center', color='saddlebrown')

            arrow_dx = 20 if play_direction == 'right' else -20
            ax.arrow(60, 53.3 / 2, arrow_dx, 0, head_width=3, head_length=5, fc='grey', ec='grey', alpha=0.8, linewidth=3)

            role_text = "\n".join([f"{row['player_name']} - {row['player_role']}" for _, row in frame_df.iterrows()])
            ax.text(121, 50, role_text, fontsize=8, va='top', ha='left', bbox=dict(facecolor='lightgrey', alpha=0.5))

        else:  # post-throw
            frame_df = post_play_df[post_play_df['frame_id'] == frame_id]
            if frame_df.empty:
                return

            ax.set_title(f"Post-Throw | Game {game_id}, Play {play_id}, Frame {frame_id}")

            # Players only
            for _, row in frame_df.iterrows():
                ax.scatter(row['x'], row['y'], c='blue', marker='o', s=100, edgecolors='black')
                ax.text(row['x'], row['y'] - 2, f"{row['nfl_id']}", fontsize=6, ha='center')

            # Keep the same ball from pre-throw
            ball = Ellipse((ball_x, ball_y), width=2, height=1, color='saddlebrown', alpha=0.9)
            ax.add_patch(ball)
            ax.text(ball_x, ball_y + 1, "Ball Land", fontsize=8, ha='center', color='saddlebrown')

        ax.set_xlim(0, 120)
        ax.set_ylim(0, 53.3)
        ax.set_facecolor('white')

    anim = FuncAnimation(fig, draw_frame, frames=len(all_frames), interval=500, repeat=False)
    plt.show()
