import pandas as pd

def calculate_offense_trajectory(pre, game_id, play_id):
    target_rows = pre[
        (pre['game_id'] == game_id) &
        (pre['play_id'] == play_id) &
        (pre['player_role'] == 'Targeted Receiver')
    ]

    ball_x, ball_y = target_rows['ball_land_x'].iloc[0], target_rows['ball_land_y'].iloc[0]
    target_player = target_rows['nfl_id'].iloc[0]
    frames_to_predict = target_rows['num_frames_output'].iloc[0]
    current_x = target_rows.sort_values('frame_id')['x'].iloc[-1]
    current_y = target_rows.sort_values('frame_id')['y'].iloc[-1]

    x_step = (ball_x - current_x) / frames_to_predict
    y_step = (ball_y - current_y) / frames_to_predict

    # Generate frame ids: from 1 up to num_frames_output
    frame_ids = list(range(1, frames_to_predict + 1))

    # Generate positions
    x_vals = [current_x + (i) * x_step for i in range(frames_to_predict)]
    y_vals = [current_y + (i) * y_step for i in range(frames_to_predict)]

    # Build DataFrame
    df = pd.DataFrame({
        'game_id': [game_id] * frames_to_predict,
        'play_id': [play_id] * frames_to_predict,
        'nfl_id': [target_player] * frames_to_predict,
        'frame_id': frame_ids,
        'x': x_vals,
        'y': y_vals
    })

    return df, target_player