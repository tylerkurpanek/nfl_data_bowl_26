import pandas as pd
import numpy as np

def calculate_offense_trajectory_ball_other(pre, game_id, play_id):
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

    x_vals, y_vals, frame_ids = [], [], []

    # Precompute vector to ball and perpendicular for curvature
    vec_to_ball = np.array([ball_x - current_x, ball_y - current_y])
    dist_to_ball = np.linalg.norm(vec_to_ball)
    if dist_to_ball == 0:
        vec_norm = np.array([0.0, 0.0])
        perp = np.array([0.0, 0.0])
    else:
        vec_norm = vec_to_ball / dist_to_ball
        perp = np.array([-vec_norm[1], vec_norm[0]])  # perpendicular vector

    # Determine curvature magnitude from speed and direction
    speed_factor = speed / 10  # adjust scaling as needed
    angle_factor = np.abs(np.sin(direction))  # wide angle → larger curve
    curvature = speed_factor * angle_factor * 0.5  # tweak multiplier for smoothness

    for f in range(1, frames_to_predict + 1):
        t = f / frames_to_predict  # normalized time from 0 → 1

        # Parabolic blend toward ball with perpendicular offset
        offset = np.sin(np.pi * t) * curvature  # peaks in middle
        cur_pos = np.array([current_x, current_y]) + vec_norm * dist_to_ball * t + perp * offset

        x_vals.append(cur_pos[0])
        y_vals.append(cur_pos[1])
        frame_ids.append(f)

    # Ensure last frame exactly hits the ball
    x_vals[-1] = ball_x
    y_vals[-1] = ball_y

    df = pd.DataFrame({
        'game_id': [game_id] * frames_to_predict,
        'play_id': [play_id] * frames_to_predict,
        'nfl_id': [target_player] * frames_to_predict,
        'frame_id': frame_ids,
        'x': x_vals,
        'y': y_vals
    })

    return df, target_player
