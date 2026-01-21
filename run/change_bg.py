import os
import cv2
import numpy as np
from tqdm import tqdm
from PIL import Image
import argparse
import glob
import subprocess

def erode_mask(mask, erosion_size=5):
    kernel = np.ones((erosion_size, erosion_size), np.uint8)
    eroded_mask = cv2.erode(mask, kernel, iterations=1)
    return eroded_mask

def blur_mask(mask, blur_size=5):
    blurred_mask = cv2.GaussianBlur(mask, (blur_size, blur_size), 0)
    return blurred_mask

def process_frame(frame, background=True):
    output = remove(frame)  # Assuming remove function is defined somewhere
    output_np = np.array(output)

    if output_np.shape[2] == 4:  # RGBA 이미지인 경우
        mask = output_np[:, :, 3]
    else:  # RGB 이미지인 경우
        mask = np.array(output.convert("L"))

    eroded_mask = erode_mask(mask)
    blurred_mask = blur_mask(eroded_mask)

    output_np[:, :, 3] = blurred_mask
    output = Image.fromarray(output_np, mode="RGBA")

    if background:
        result = Image.new("RGB", output.size, (223, 240, 253))
        result.paste(output, mask=output.split()[3])
    else:
        result = output

    return result

def main(input_path, output_path, background=True):
    video_files = glob.glob(input_path + '/*.mp4')

    for video_file in tqdm(video_files):
        cap = cv2.VideoCapture(video_file)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None

        # Extract audio from the input video
        audio_file = os.path.join(output_path, 'audio.aac')
        subprocess.run(['ffmpeg', '-i', video_file, '-q:a', '0', '-map', 'a', audio_file], check=True)

        output_video_path = os.path.join(output_path, os.path.basename(video_file).split('.')[0] + '_change_bg.mp4')
        out_temp_video_path = os.path.join(output_path, 'temp_' + os.path.basename(video_file).split('.')[0] + '.mp4')

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_frame = Image.fromarray(frame_rgb)

            processed_frame = process_frame(pil_frame, background)
            processed_frame = np.array(processed_frame)
            processed_frame_bgr = cv2.cvtColor(processed_frame, cv2.COLOR_RGB2BGR)

            if out is None:
                h, w, _ = processed_frame_bgr.shape
                out = cv2.VideoWriter(out_temp_video_path, fourcc, 30, (w, h))

            out.write(processed_frame_bgr)

        cap.release()
        if out:
            out.release()

        # Combine the processed video with the extracted audio
        subprocess.run(['ffmpeg', '-i', out_temp_video_path, '-i', audio_file, '-c', 'copy', '-map', '0:v:0', '-map', '1:a:0', output_video_path], check=True)

        # Clean up temporary files
        os.remove(out_temp_video_path)
        os.remove(audio_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Removing background of videos and preserving audio')
    parser.add_argument('--input_path', type=str, required=True, help='source video path')
    parser.add_argument('--output_path', type=str, required=True, help='output video path')

    args = parser.parse_args()

    os.makedirs(args.output_path, exist_ok=True)
    main(args.input_path, args.output_path)
