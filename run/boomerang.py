import subprocess
import imageio
import glob
import shutil
from skimage import img_as_ubyte
import skimage.io as skio
import cv2
import argparse

def extract_frames(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cmd = f'ffmpeg -i {input_file} {output_dir}/frame_%03d.png'
    subprocess.run(cmd, shell=True)

def create_boomerang_effect(input_file, frames_dir, output_video_path, num_repeats=4, FPS=25.0):
    extract_frames(input_file, frames_dir)

    # Get a list of all image files in the input folder
    image_files = [f for f in os.listdir(frames_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort() # Sort the files to maintain the order

    # Read the first image to get frame dimensions
    first_frame = cv2.imread(os.path.join(frames_dir, image_files[0]))
    frame_height, frame_width, _ = first_frame.shape

    # Output video settings
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, FPS, (frame_width, frame_height))

    frames = []

    # Read all frames
    for image_file in image_files:
        frame = cv2.imread(os.path.join(frames_dir, image_file))
        frames.append(frame)

    for i in range(num_repeats):
        for frame in frames:
            out.write(frame)
        for frame in reversed(frames):
            out.write(frame)
    out.release()
    # os.remove(frames_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inference face mask with dlib and grabcut')

    parser.add_argument('--input-file', type=str, default='/share/selena/LivePortrait_update/assets/examples/driving/ffmpeg_boomerang.mp4', help='source video file path')
    parser.add_argument('--frame-dir', type=str, default='/share/selena/LivePortrait_update/assets/examples/driving/frames', help='temp directory for extracted frames')
    parser.add_argument('--output-file', type=str, default='/share/selena/LivePortrait_update/assets/examples/driving/ffmpeg_output_boomerang.mp4', help='output video path')
    parser.add_argument('--num-boomerangs', type=int, default=4, help='number of repeats of boomerang')
    args = parser.parse_args()
    print(args)

    create_boomerang_effect(args.input_file, args.frame_dir, args.output_file, args.num_boomerangs)
