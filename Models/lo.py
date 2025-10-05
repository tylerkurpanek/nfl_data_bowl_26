import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from math_scripts.pickrandomplay import pick_random_play
import matplotlib.pyplot as plt
from math_scripts.FramebyFrameerror import calculate_frame_errors


# ------------------------------------
# FEATURE + TARGET EXTRACTION HELPERS
# ------------------------------------

def extract_features(pre, game_id, play_id):
    """Extract pre-throw features for the targeted receiver."""
    target_rows = pre[
        (pre['game_id'] == game_id) &
        (pre['play_id'] == play_id) &
        (pre['player_role'] == 'Targeted Receiver')
    ]
    if target_rows.empty:
        return None, None

    target_player = target_rows['nfl_id'].iloc[0]
    last_row = target_rows.sort_values('frame_id').iloc[-1]

    # Example feature vector — can expand later
    features = np.array([
        last_row['x'],
        last_row['y'],
        last_row['s'],
        last_row['a'],
        np.deg2rad(last_row['dir']),
        np.deg2rad(last_row['o'])
    ])
    return features, target_player


def extract_targets(post, game_id, play_id, target_player):
    """Fit a simple spatial parabola y = a*x^2 + b*x + c to the post-throw trajectory."""
    target_rows_post = post[
        (post['game_id'] == game_id) &
        (post['play_id'] == play_id) &
        (post['nfl_id'] == target_player)
    ]
    if target_rows_post.empty:
        return None

    df_sorted = target_rows_post.sort_values('frame_id')
    x = df_sorted['x'].values
    y = df_sorted['y'].values

    # Need at least 3 points to fit a parabola
    if len(x) < 3:
        return None

    coeffs = np.polyfit(x, y, 2)  # [a, b, c]
    return coeffs


# ------------------------------------
# TRAINING LOOP
# ------------------------------------

def train_parabola_predictor(n_runs=200):
    X, Y = [], []
    iter = 0

    for i in range(n_runs):
        print(iter)
        iter += 1
        try:
            pre, post, game_id, play_id = pick_random_play()
            features, target_player = extract_features(pre, game_id, play_id)
            if features is None:
                continue

            coeffs = extract_targets(post, game_id, play_id, target_player)
            if coeffs is None:
                continue

            X.append(features)
            Y.append(coeffs)

            if (i + 1) % 10 == 0:
                print(f"Processed {i+1}/{n_runs} plays")

        except Exception as e:
            print(f"Error on play {i+1}: {e}")
            continue

    X = np.array(X)
    Y = np.array(Y)

    print(f"\n✅ Collected {len(X)} valid plays out of {n_runs}")

    # Train model
    model = LinearRegression()
    model.fit(X, Y)

    # Evaluate performance on training data
    preds = model.predict(X)
    mse = mean_squared_error(Y, preds)
    print(f"Training MSE on {len(X)} plays: {mse:.6f}")

    return model, X, Y, preds


def plot_coeff_comparison(Y_true, Y_pred):
    coeff_names = ['a', 'b', 'c']
    for i in range(3):
        plt.figure()
        plt.scatter(Y_true[:, i], Y_pred[:, i], alpha=0.6)
        plt.xlabel(f"True {coeff_names[i]}")
        plt.ylabel(f"Predicted {coeff_names[i]}")
        plt.title(f"{coeff_names[i]} coefficient: True vs Predicted")
        plt.plot(
            [Y_true[:, i].min(), Y_true[:, i].max()],
            [Y_true[:, i].min(), Y_true[:, i].max()],
            'r--', label="Ideal"
        )
        plt.legend()
        plt.show()


def predict_play_trajectory(actual_df, coeffs):
    """Generate predicted (x, y) trajectory for each frame based on parabola coefficients."""
    a, b, c = coeffs
    x_vals = actual_df['x'].values  # use actual x positions per frame
    y_pred = a * x_vals**2 + b * x_vals + c

    predicted_df = pd.DataFrame({
        'frame_id': actual_df['frame_id'],
        'x': x_vals,
        'y': y_pred
    })
    return predicted_df


def evaluate_random_plays(model, n_runs=200):
    all_frame_errors = []

    for i in range(n_runs):
        pre, post, game_id, play_id = pick_random_play()
        
        # Extract features for targeted receiver
        target_rows = pre[
            (pre['game_id'] == game_id) &
            (pre['play_id'] == play_id) &
            (pre['player_role'] == 'Targeted Receiver')
        ]
        if target_rows.empty:
            continue

        last_row = target_rows.sort_values('frame_id').iloc[-1]
        features = np.array([
            last_row['x'],
            last_row['y'],
            last_row['s'],
            last_row['a'],
            np.deg2rad(last_row['dir']),
            np.deg2rad(last_row['o'])
        ])

        target_player = target_rows['nfl_id'].iloc[0]

        # Fit true parabola to get actual coefficients (optional)
        target_rows_post = post[
            (post['game_id'] == game_id) &
            (post['play_id'] == play_id) &
            (post['nfl_id'] == target_player)
        ].sort_values('frame_id')
        if len(target_rows_post) < 3:
            continue

        # Predict parabola coefficients
        predicted_coeffs = model.predict(features.reshape(1, -1))[0]

        # Generate predicted trajectory
        predicted_df = predict_play_trajectory(target_rows_post, predicted_coeffs)

        # Compute frame errors
        frame_errors = calculate_frame_errors(target_rows_post, predicted_df)
        all_frame_errors.append(frame_errors)

        # Optional: plot first few plays for visualization
        if i < 3:
            plt.figure()
            plt.plot(target_rows_post['x'], target_rows_post['y'], 'o', label='Actual')
            plt.plot(predicted_df['x'], predicted_df['y'], '-', label='Predicted')
            plt.title(f"Game {game_id}, Play {play_id}")
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.legend()
            plt.show()

    return all_frame_errors