import cv2
import dlib
import numpy as np
import subprocess


def process_video(input_video_path, output_video_path, scale=1.2):
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('temp_output.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(3)), int(cap.get(4))))
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        if len(faces) > 0:
            landmarks = predictor(gray, faces[0])
            mouth_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(48, 68)])
            
            hull = cv2.convexHull(mouth_points)
            x, y, w, h = cv2.boundingRect(hull)
            y -= 10
            h += 20
            mouth_region = frame[y:y+h, x:x+w]
            
            mouth_region_resized = cv2.resize(mouth_region, (int(w*1.1), int(h*1.1)))
            
            blended_frame = frame.copy()
            blended_frame[y + h // 2 - mouth_region_resized.shape[0] // 2:y + h // 2 + mouth_region_resized.shape[0] // 2,
                          x + w // 2 - mouth_region_resized.shape[1] // 2:x + w // 2 + mouth_region_resized.shape[1] // 2] = mouth_region_resized
            
            mouth_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
            hull = cv2.convexHull(mouth_points)
            x, y, w, h = cv2.boundingRect(hull)
            y -= 10
            h += 20
            eye_one_region = frame[y:y+h, x:x+w]
            eye_one_region_resized = cv2.resize(eye_one_region, (int(w*1.4), int(h*1.4)))
            blended_frame[y + h // 2 - eye_one_region_resized.shape[0] // 2:y + h // 2 + eye_one_region_resized.shape[0] // 2,
                          x + w // 2 - eye_one_region_resized.shape[1] // 2:x + w // 2 + eye_one_region_resized.shape[1] // 2] = eye_one_region_resized
            
            mouth_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
            hull = cv2.convexHull(mouth_points)
            x, y, w, h = cv2.boundingRect(hull)
            y -= 10
            h += 20
            eye_two_region = frame[y:y+h, x:x+w]
            eye_two_region_resized = cv2.resize(eye_two_region, (int(w*1.4), int(h*1.4)))
            blended_frame[y + h // 2 - eye_two_region_resized.shape[0] // 2:y + h // 2 + eye_two_region_resized.shape[0] // 2,
                          x + w // 2 - eye_two_region_resized.shape[1] // 2:x + w // 2 + eye_two_region_resized.shape[1] // 2] = eye_two_region_resized
            
            out.write(blended_frame)
        else:
            out.write(frame)
    
    cap.release()
    out.release()
    
    # Extract audio from input video
    extract_audio_command = f"ffmpeg -i {input_video_path} -q:a 0 -map a temp_audio.mp3"
    subprocess.call(extract_audio_command, shell=True)

    # Combine processed video and extracted audio
    combine_command = f"ffmpeg -i temp_output.mp4 -i temp_audio.mp3 -c:v copy -c:a aac -strict experimental {output_video_path}"
    subprocess.call(combine_command, shell=True)

    # Clean up temporary files
    subprocess.call("rm temp_output.mp4 temp_audio.mp3", shell=True)

# Example usage
process_video('input_video.mp4', 'output_video_with_audio.mp4')
