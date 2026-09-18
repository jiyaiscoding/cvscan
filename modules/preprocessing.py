import cv2
import numpy as np

class DocumentPreprocessor:
    @staticmethod
    def resize_image(image: np.ndarray, max_width: int = 1000) -> np.ndarray:
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image input for resizing.")
        
        height, width = image.shape[:2]
        if width > max_width:
            scale = max_width / float(width)
            new_width = max_width
            new_height = int(height * scale)
            return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return image.copy()

    @staticmethod
    def process_gray_and_blur(image: np.ndarray, kernel_size: tuple = (5, 5)) -> tuple:
        if image is None or not isinstance(image, np.ndarray):
            raise ValueError("Invalid image input for grayscale and blurring.")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        blurred = cv2.GaussianBlur(gray, kernel_size, 0)
        return gray, blurred