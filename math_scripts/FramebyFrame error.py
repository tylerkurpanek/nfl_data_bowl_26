import pandas as pd
import numpy as np

def calculate_frame_errors(actual_df, predicted_df):
    # Merge on frame_id (assuming same player, game, and play)
    merged = pd.merge(
        actual_df[['frame_id', 'x', 'y']],
        predicted_df[['frame_id', 'x', 'y']],
        on='frame_id',
        suffixes=('_actual', '_pred')
    )
    
    # Compute Euclidean distance for each frame
    merged['error'] = np.sqrt((merged['x_actual'] - merged['x_pred'])**2 + (merged['y_actual'] - merged['y_pred'])**2)
    
    return merged[['frame_id', 'error']]