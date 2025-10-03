def calculate_offense_actual_trajectory(post, game_id, play_id,nfl_id):
    df = post[(post['game_id'] == game_id) & (post['play_id'] == play_id) & (post['nfl_id'] == nfl_id)]
    return df