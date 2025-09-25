import cv2
import numpy as np
from PIL import Image
import os

def validate_image(file_path):
    """
    Validate if the file is a valid image
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except:
        return False

def resize_image(image_path, target_size=(224, 224)):
    """
    Resize image to target dimensions
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")

        resized = cv2.resize(image, target_size)
        return resized
    except Exception as e:
        raise Exception(f"Error resizing image: {str(e)}")

def enhance_image_quality(image_path):
    """
    Apply basic image enhancement techniques
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")

        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        # Split channels
        l, a, b = cv2.split(lab)

        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)

        # Merge channels and convert back to BGR
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

        return enhanced
    except Exception as e:
        raise Exception(f"Error enhancing image: {str(e)}")

def extract_image_features(image_path):
    """
    Extract basic features from image for classification
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")

        # Convert to different color spaces
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate basic statistics
        features = {
            'mean_brightness': np.mean(gray),
            'std_brightness': np.std(gray),
            'mean_hue': np.mean(hsv[:, :, 0]),
            'mean_saturation': np.mean(hsv[:, :, 1]),
            'dominant_colors': extract_dominant_colors(image),
            'texture_features': calculate_texture_features(gray)
        }

        return features
    except Exception as e:
        raise Exception(f"Error extracting features: {str(e)}")

def extract_dominant_colors(image, k=3):
    """
    Extract dominant colors using K-means clustering
    """
    try:
        # Reshape image to be a list of pixels
        pixels = image.reshape((-1, 3))
        pixels = np.float32(pixels)

        # Apply K-means clustering
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        # Convert centers to integers
        centers = np.uint8(centers)

        return centers.tolist()
    except:
        return []

def calculate_texture_features(gray_image):
    """
    Calculate basic texture features
    """
    try:
        # Calculate gradient
        grad_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

        # Calculate magnitude
        magnitude = np.sqrt(grad_x**2 + grad_y**2)

        return {
            'mean_gradient': np.mean(magnitude),
            'std_gradient': np.std(magnitude),
            'edge_density': np.sum(magnitude > np.mean(magnitude)) / magnitude.size
        }
    except:
        return {}

def save_processed_image(image, output_path):
    """
    Save processed image to file
    """
    try:
        cv2.imwrite(output_path, image)
        return True
    except:
        return False