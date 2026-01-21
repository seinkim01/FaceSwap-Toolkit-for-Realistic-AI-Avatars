from moviepy.editor import VideoFileClip, clips_array, vfx, concatenate_videoclips
import os

def load_and_repeat_videos_from_directory(directory, repeat_count=3):
    clips = []
    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):
            filepath = os.path.join(directory, filename)
            try:
                clip = VideoFileClip(filepath)
                # Repeat the video
                repeated_clip = vfx.loop(clip, n=repeat_count)
                clips.append(repeated_clip)
                print(f"Loaded and repeated {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    return clips

def play_and_save_videos_side_by_side(clips, output_path):
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Arrange clips side by side
        final_clip = clips_array([clips])
        print("Clips arranged side by side")

        # Save the final clip to a file using ffmpeg
        final_clip.write_videofile(output_path, codec='libx264', fps=24)
        print(f"Final video saved to {output_path}")
        
        # Preview the final clip
        final_clip.preview()
    except Exception as e:
        print(f"Error during playback or saving: {e}")

if __name__ == "__main__":
    video_directory = "/share/selena/StyleGANEX/output"  # Replace with the actual path to the 'output' directory
    output_path = "/share/selena/StyleGANEX/output/video_repeat.mp4"  # Replace with the actual path to save the final output
    
    clips = load_and_repeat_videos_from_directory(video_directory, repeat_count=3)
    if clips:
        play_and_save_videos_side_by_side(clips, output_path)
    else:
        print("No video clips loaded.")
