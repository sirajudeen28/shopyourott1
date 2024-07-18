import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image

def calculate_histogram(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    return cv2.normalize(hist, hist).flatten()

def calculate_ssim(img1, img2, win_size=7):
    # Ensure win_size is odd and not larger than the smallest image dimension
    min_dim = min(img1.shape[0], img1.shape[1], img2.shape[0], img2.shape[1])
    win_size = min(win_size, min_dim - 1)
    win_size = win_size if win_size % 2 == 1 else win_size - 1
    
    return ssim(img1, img2, win_size=win_size, channel_axis=2)

def are_images_similar(img1, img2, hist_threshold=0.9, ssim_threshold=0.8):
    # Compare histograms
    hist1 = calculate_histogram(img1)
    hist2 = calculate_histogram(img2)
    hist_similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    
    # Comparing structural similarity
    ssim_score = calculate_ssim(img1, img2)
    
    return hist_similarity > hist_threshold and ssim_score > ssim_threshold

def keep_unique_outfits(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    unique_images = []
    
    for i, image_file in enumerate(image_files):
        print(f"Processing image {i+1}/{len(image_files)}: {image_file}")
        current_image_path = os.path.join(input_folder, image_file)
        current_image = cv2.imread(current_image_path)
        print(f"Image shape: {current_image.shape}")
        
        if current_image is None:
            print(f"Failed to read image: {image_file}")
            continue
        
        # Ensure the image is in RGB format
        current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
        
        is_unique = True
        for unique_image in unique_images:
            if are_images_similar(current_image, unique_image):
                is_unique = False
                break
        
        if is_unique:
            unique_images.append(current_image)
            output_path = os.path.join(output_folder, image_file)
            cv2.imwrite(output_path, cv2.cvtColor(current_image, cv2.COLOR_RGB2BGR))
    
    print(f"Kept {len(unique_images)} unique images out of {len(image_files)} total images.")


def execute_distinct_outfit():
    input_folder = "outfit_images"
    output_folder = "distinct_outfits"
    keep_unique_outfits(input_folder, output_folder)
    return "Process Completed"