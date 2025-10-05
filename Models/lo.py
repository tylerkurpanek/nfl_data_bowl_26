import pandas as pd
import numpy as np
from Models.fit_play_parabola import fit_play_parabola


def train_linearoffense(pre, post, game_id, play_id):
    target_rows = pre[
        (pre['game_id'] == game_id) &
        (pre['play_id'] == play_id) &
        (pre['player_role'] == 'Targeted Receiver')
    ]


    # Football landing
    ball_x, ball_y = target_rows['ball_land_x'].iloc[0], target_rows['ball_land_y'].iloc[0]
    target_player = target_rows['nfl_id'].iloc[0]


    # Last known frame info
    last_row = target_rows.sort_values('frame_id').iloc[-1]
    current_x, current_y = last_row['x'], last_row['y']
    speed = last_row['s']
    accel = last_row['a']
    orentation = last_row['o']
    direction = np.deg2rad(last_row['dir'])




    target_rows_post = post[
        (post['game_id'] == game_id) &
        (post['play_id'] == play_id) &
        (post['nfl_id'] == target_player)
    ]

    return fit_play_parabola(target_rows_post,game_id, play_id, target_player, degree=2, plot=True)