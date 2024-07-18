
import cv2
import numpy as np
import os
import datetime

def capture_outfits_from_video(video_path, output_folder, threshold=5000):
    cap = cv2.VideoCapture(video_path)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    ret, prev_frame = cap.read()
    if not ret:
        print("Failed to read video")
        return
    
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_count = 0
    outfit_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Compute the absolute difference between the current and previous frame
        frame_diff = cv2.absdiff(frame_gray, prev_frame_gray)
        
        # Apply a threshold to identify significant changes
        _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
        
        # Calculate the number of changed pixels
        changed_pixels = np.sum(thresh) // 255
        
        # If the number of changed pixels is above the threshold, consider it a new outfit
        if changed_pixels > threshold:
            outfit_path = os.path.join(output_folder, f"outfit_{outfit_count}.jpg")
            cv2.imwrite(outfit_path, frame)
            outfit_count += 1
            
            # Reset the previous frame to the current frame
            prev_frame_gray = frame_gray.copy()
        
        frame_count += 1
    
    cap.release()
    print(f"Captured {outfit_count} outfits from {frame_count} frames")


# Main function
if __name__ == "__main__":
    video_path = "video_path\\sample3.mp4"
    output_folder = "outfit_images"

    start_time = datetime.datetime.now()

    capture_outfits_from_video(video_path, output_folder)

    end_time = datetime.datetime.now()
    diff = end_time - start_time
    print(f"Time taken {diff}")