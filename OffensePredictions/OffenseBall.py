import pandas as pd
import numpy as np

def calculate_offense_trajectory(pre, game_id, play_id):
    target_rows = pre[
        (pre['game_id'] == game_id) &
        (pre['play_id'] == play_id) &
        (pre['player_role'] == 'Targeted Receiver')
    ]

    # Football landing
    ball_x, ball_y = target_rows['ball_land_x'].iloc[0], target_rows['ball_land_y'].iloc[0]
    target_player = target_rows['nfl_id'].iloc[0]
    frames_to_predict = int(target_rows['num_frames_output'].iloc[0])

    # Last known frame info
    last_row = target_rows.sort_values('frame_id').iloc[-1]
    current_x, current_y = last_row['x'], last_row['y']
    speed = last_row['s']
    accel = last_row['a']
    direction = np.deg2rad(last_row['dir'])  # convert to radians

    # Store trajectory
    x_vals, y_vals, frame_ids = [], [], []

    for f in range(1, frames_to_predict + 1):
        # Update speed with acceleration
        speed = max(0, speed + accel * 0.1)  # assume ~0.1s per frame

        # Step in current direction
        dx = speed * np.cos(direction) * 0.1
        dy = speed * np.sin(direction) * 0.1
        current_x += dx
        current_y += dy

        # Curve toward football
        vec_to_ball = np.array([ball_x - current_x, ball_y - current_y])
        angle_to_ball = np.arctan2(vec_to_ball[1], vec_to_ball[0])

        # Blend direction slightly toward ball each frame
        direction = 0.9 * direction + 0.1 * angle_to_ball  

        # Save frame
        x_vals.append(current_x)
        y_vals.append(current_y)
        frame_ids.append(f)

    df = pd.DataFrame({
        'game_id': [game_id] * frames_to_predict,
        'play_id': [play_id] * frames_to_predict,
        'nfl_id': [target_player] * frames_to_predict,
        'frame_id': frame_ids,
        'x': x_vals,
        'y': y_vals
    })

    return df, target_player