import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

def calculate_play_rmse(solution: pd.DataFrame, submission: pd.DataFrame) -> float:
    """
    Compute RMSE for a single play given actual (solution) and predicted (submission) DataFrames.
    Both DataFrames must have columns:
        ['game_id', 'play_id', 'nfl_id', 'frame_id', 'x', 'y']
    """
    # Merge on keys
    merged = pd.merge(
        solution,
        submission,
        on=['game_id', 'play_id', 'nfl_id', 'frame_id'],
        suffixes=('_true', '_pred')
    )

    # Compute RMSE across x and y
    rmse = np.sqrt(
        0.5 * (
            mean_squared_error(merged['x_true'], merged['x_pred']) +
            mean_squared_error(merged['y_true'], merged['y_pred'])
        )
    )

    return float(rmse)