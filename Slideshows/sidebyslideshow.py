import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Slideshows.play_slideshow_both import play_full_slideshow  # Assuming you already have this function

def compare_slideshows(pre, df1, df2, game_id, play_id):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 6))  # Side-by-side axes

    # Get frame IDs from both dataframes
    frames1 = sorted(df1['frame_id'].unique())
    frames2 = sorted(df2['frame_id'].unique())
    n_frames = max(len(frames1), len(frames2))

    def draw_frame(i):
        ax1.clear()
        ax2.clear()

        # Slideshow 1
        frame_df1 = df1[df1['frame_id'] == frames1[i % len(frames1)]]
        play_full_slideshow(pre, frame_df1, game_id, play_id, ax=ax1)  # Modify play_full_slideshow to accept ax

        # Slideshow 2
        frame_df2 = df2[df2['frame_id'] == frames2[i % len(frames2)]]
        play_full_slideshow(pre, frame_df2, game_id, play_id, ax=ax2)  # Modify play_full_slideshow to accept ax

    anim = FuncAnimation(fig, draw_frame, frames=n_frames, interval=200, repeat=False)
    plt.show()