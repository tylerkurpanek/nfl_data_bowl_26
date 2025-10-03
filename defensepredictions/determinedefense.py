import pandas as pd
import numpy as np

def determinedefense(pre, game_id, play_id):
    all_frames = pre[(pre['game_id'] == game_id) & (pre['play_id'] == play_id)]
    unique_players = all_frames['nfl_id'].unique()

    # Use frame at the snap
    snap_df = pre[(pre['game_id'] == game_id) & (pre['play_id'] == play_id) & (pre['frame_id'] == 1)]
    
    # Split offense vs defense, keep position
    offense = snap_df[snap_df['player_side'] == 'Offense'][['nfl_id', 'player_position', 'x', 'y']].rename(
        columns={'nfl_id': 'offense_id', 'player_position': 'offense_position'}
    )
    defense = snap_df[snap_df['player_side'] == 'Defense'][['nfl_id', 'player_position', 'x', 'y']].rename(
        columns={'nfl_id': 'defense_id', 'player_position': 'defense_position'}
    )

    results = []

    for _, d_row in defense.iterrows():
        d_x, d_y = d_row['x'], d_row['y']
        d_id = d_row['defense_id']
        d_pos = d_row['defense_position']

        # Compute distances to all offensive players
        offense = offense.copy()
        offense['dist'] = np.sqrt((offense['x'] - d_x)**2 + (offense['y'] - d_y)**2)

        # Nearest offensive player
        nearest = offense.loc[offense['dist'].idxmin()]

        results.append({
            'defense_id': d_id,
            'defense_position': d_pos,
            'nearest_offense_id': nearest['offense_id'],
            'offense_position': nearest['offense_position'],
            'min_distance': nearest['dist']
        })

    return pd.DataFrame(results)
