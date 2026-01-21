from moviepy.editor import VideoFileClip, clips_array, vfx, concatenate_videoclips, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

def create_text_image(text, size, font_size=24):
    img = Image.new('RGB', size, color='black')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    position = ((size[0] - text_w) // 2, (size[1] - text_h) // 2)
    draw.text(position, text, font=font, fill='white')
    return img

def load_and_repeat_videos_from_directory(directory, repeat_count=3):
    clips = []
    min_duration = None

    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):
            filepath = os.path.join(directory, filename)
            try:
                clip = VideoFileClip(filepath)
                if min_duration is None or clip.duration < min_duration:
                    min_duration = clip.duration
                repeated_clip = vfx.loop(clip, n=repeat_count)
                text_img = create_text_image(filename, (repeated_clip.w, 30))
                text_clip = ImageClip(np.array(text_img)).set_duration(repeated_clip.duration).set_position('top')
                titled_clip = CompositeVideoClip([repeated_clip, text_clip])
                clips.append(titled_clip)
                print(f"Loaded, repeated, and titled {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    if min_duration is not None:
        # Truncate all clips to the minimum duration found
        clips = [clip.subclip(0, min_duration) for clip in clips]
    else:
        print("No valid video clips found.")
        return []

    return clips

def play_and_save_videos_side_by_side(clips, output_path):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final_clip = clips_array([clips])
        print("Clips arranged side by side")

        # Ensure audio and video have the same length
        final_clip = final_clip.set_duration(final_clip.duration)
        final_clip.write_videofile(output_path, codec='libx264', fps=24)
        print(f"Final video saved to {output_path}")
        final_clip.preview()
    except Exception as e:
        print(f"Error during playback or saving: {e}")

if __name__ == "__main__":
    video_directory = "/share/selena/StyleGANEX/output"
    output_path = "/share/selena/StyleGANEX/output/video_repeat.mp4"
    
    clips = load_and_repeat_videos_from_directory(video_directory, repeat_count=3)
    if clips:
        play_and_save_videos_side_by_side(clips, output_path)
    else:
        print("No video clips loaded.")


### Edit grid

from moviepy.editor import VideoFileClip, clips_array, vfx, concatenate_videoclips, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

def create_text_image(text, size, font_size=24):
    img = Image.new('RGB', size, color='black')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    position = ((size[0] - text_w) // 2, (size[1] - text_h) // 2)
    draw.text(position, text, font=font, fill='white')
    return img

def load_and_repeat_videos_from_directory(directory, repeat_count=3):
    clips = []
    min_duration = None

    for filename in os.listdir(directory):
        if filename.endswith('.mp4'):
            filepath = os.path.join(directory, filename)
            try:
                clip = VideoFileClip(filepath)
                if min_duration is None or clip.duration < min_duration:
                    min_duration = clip.duration
                repeated_clip = vfx.loop(clip, n=repeat_count)
                text_img = create_text_image(filename, (repeated_clip.w, 30))
                text_clip = ImageClip(np.array(text_img)).set_duration(repeated_clip.duration).set_position('top')
                titled_clip = CompositeVideoClip([repeated_clip, text_clip])
                clips.append(titled_clip)
                print(f"Loaded, repeated, and titled {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    if min_duration is not None:
        # Truncate all clips to the minimum duration found
        clips = [clip.subclip(0, min_duration) for clip in clips]
    else:
        print("No valid video clips found.")
        return []

    return clips

def arrange_clips_in_grid(clips, clips_per_row, num_rows):
    grid = []
    for i in range(0, len(clips), clips_per_row):
        row_clips = clips[i:i + clips_per_row]
        if len(row_clips) < clips_per_row:
            row_clips += [row_clips[-1]] * (clips_per_row - len(row_clips))  # Duplicate last clip to fill the row
        grid.append(row_clips)
    # Ensure grid has the required number of rows
    if len(grid) < num_rows:
        last_row = grid[-1] if grid else []
        while len(grid) < num_rows:
            grid.append(last_row)
    return grid[:num_rows]

def play_and_save_videos_side_by_side(clips, output_path, clips_per_row=5, num_rows=3):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        grid = arrange_clips_in_grid(clips, clips_per_row, num_rows)
        final_clip = clips_array(grid)
        print("Clips arranged in grid")

        # Ensure audio and video have the same length
        final_clip = final_clip.set_duration(final_clip.duration)
        final_clip.write_videofile(output_path, codec='libx264', fps=24)
        print(f"Final video saved to {output_path}")
        final_clip.preview()
    except Exception as e:
        print(f"Error during playback or saving: {e}")

if __name__ == "__main__":
    video_directory = "/share/selena/StyleGANEX/output"
    output_path = "/share/selena/StyleGANEX/output/video_repeat.mp4"
    
    clips = load_and_repeat_videos_from_directory(video_directory, repeat_count=3)
    if clips:
        play_and_save_videos_side_by_side(clips, output_path)
    else:
        print("No video clips loaded.")
