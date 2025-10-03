from pickrandomplay import pick_random_play
from play_slideshow_prethrow import play_slideshow_prethrow
from play_slideshow_postthrow import play_post_simple
from play_slideshow_both import play_full_slideshow
from OffenseBall import calculate_offense_trajectory
from OffenseActual import calculate_offense_actual_trajectory
from calcrmse import calculate_play_rmse
from determinedefense import determinedefense

if __name__ == "__main__":

    '''
    n_runs = 10
    rmse_list = []
    iter = 0
    
    for _ in range(n_runs):
        pre, post, game_id, play_id = pick_random_play()
        predicted_df, nfl_id = calculate_offense_trajectory(pre, game_id, play_id)
        actual_df = calculate_offense_actual_trajectory(post, game_id, play_id, nfl_id)
        rmse = calculate_play_rmse(actual_df, predicted_df)
        rmse_list.append(rmse)
        iter +=1
        print (iter)


    mean_rmse = sum(rmse_list) / len(rmse_list)
    print(f"Mean RMSE over {n_runs} random plays: {mean_rmse:.4f}")
    '''

    pre, post, game_id, play_id = pick_random_play()
    predicted_df, nfl_id = calculate_offense_trajectory(pre, game_id, play_id)
    #print(determinedefense(pre, game_id, play_id))

    #play_full_slideshow(pre, post, game_id, play_id)
    play_slideshow_prethrow(pre, game_id, play_id)
    play_post_simple(post, game_id, play_id)