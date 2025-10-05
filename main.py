from math_scripts.pickrandomplay import pick_random_play
from Slideshows.play_slideshow_prethrow import play_slideshow_prethrow
from Slideshows.play_slideshow_postthrow import play_post_simple
from Slideshows.play_slideshow_both import play_full_slideshow
from OffensePredictions.OffenseBall import calculate_offense_trajectory
from OffensePredictions.OffenseActual import calculate_offense_actual_trajectory
from math_scripts.calcrmse import calculate_play_rmse
from defensepredictions.determinedefense import determinedefense
from OffensePredictions.Offenseballother import calculate_offense_trajectory_ball_other
from Slideshows.sidebyslideshow import compare_slideshows
from math_scripts.FramebyFrameerror import calculate_frame_errors
from Models.fit_play_parabola import fit_play_parabola
from Models.lo import train_linearoffense
if __name__ == "__main__":

    '''
    n_runs = 500
    rmse_list = []
    iter = 0
    rmse_list_other = []
    
    for _ in range(n_runs):
        pre, post, game_id, play_id = pick_random_play()
        predicted_df, nfl_id = calculate_offense_trajectory(pre, game_id, play_id)
        predicted_df_other,nfl_id = calculate_offense_trajectory_ball_other(pre, game_id, play_id)
        actual_df = calculate_offense_actual_trajectory(post, game_id, play_id, nfl_id)
        rmse = calculate_play_rmse(actual_df, predicted_df)
        rmse_other = calculate_play_rmse(actual_df, predicted_df_other)
        rmse_list.append(rmse)
        rmse_list_other.append(rmse_other)
        iter +=1
        print (iter)


    mean_rmse = sum(rmse_list) / len(rmse_list)
    mean_rmse_other = sum(rmse_list_other) / len(rmse_list_other)
    print(f"Mean RMSE over {n_runs} random plays Just BALL: {mean_rmse:.4f}")
    print(f"Mean RMSE over {n_runs} random plays OTHER: {mean_rmse_other:.4f}")
    '''


    pre, post, game_id, play_id = pick_random_play()
    print(train_linearoffense(pre, post, game_id, play_id))


