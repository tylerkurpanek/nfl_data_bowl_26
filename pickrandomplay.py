import os
import random
import pandas as pd

def pick_random_play(folder="./train"):
    # Pick a random week file
    week_num = random.randint(1, 18)
    csv_file = f"input_2023_w{week_num:02d}.csv"
    file_path = os.path.join(folder, csv_file)

    pre = pd.read_csv(file_path)
    csv_file_post = csv_file.replace("input", "output")
    file_path_post= os.path.join(folder, csv_file_post)



    post = pd.read_csv(file_path_post)
    # Pick a random row directly instead of multiple choices
    random_row = pre.sample(1).iloc[0]
    game_id, play_id = random_row["game_id"], random_row["play_id"]


                      


    return pre, post, game_id, play_id
