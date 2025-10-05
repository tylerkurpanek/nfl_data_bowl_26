import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fit_play_parabola(post, game_id, play_id, nfl_id, degree=2, plot=True):
    """
    Fit a parametric curve (polynomial) to a player's post-pass trajectory.

    Parameters
    ----------
    post : pd.DataFrame
        The post-pass frame data, columns: ['game_id', 'play_id', 'nfl_id', 'frame_id', 'x', 'y']
    game_id : int
        Game identifier
    play_id : int
        Play identifier
    nfl_id : int
        Player identifier
    degree : int
        Degree of polynomial to fit (default 2 for parabola)
    plot : bool
        If True, plots the fitted curve and original points

    Returns
    -------
    smooth_df : pd.DataFrame
        DataFrame with smooth 'x' and 'y' values along the trajectory
    """

    # Filter for the specific player and play
    df = post[
        (post['game_id'] == game_id) &
        (post['play_id'] == play_id) &
        (post['nfl_id'] == nfl_id)
    ].sort_values('frame_id')

    t = df['frame_id'].values
    x = df['x'].values
    y = df['y'].values

    # Fit polynomials for x(t) and y(t)
    coeffs_x = np.polyfit(t, x, degree)
    coeffs_y = np.polyfit(t, y, degree)

    # Generate smooth t values
    t_smooth = np.linspace(t[0], t[-1], 50)
    x_smooth = np.polyval(coeffs_x, t_smooth)
    y_smooth = np.polyval(coeffs_y, t_smooth)

    smooth_df = pd.DataFrame({
        'frame_id': t_smooth,
        'x': x_smooth,
        'y': y_smooth
    })

    if plot:
        plt.figure(figsize=(6, 6))
        plt.plot(x, y, 'o', label='Original Frames')
        plt.plot(x_smooth, y_smooth, '-', label=f'Fitted Polynomial (deg={degree})')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Player {nfl_id} Trajectory (Game {game_id}, Play {play_id})')
        plt.legend()
        plt.axis('equal')
        plt.show()

    return smooth_df
