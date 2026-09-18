import cv2
import numpy as np

class DocumentEnhancer:
    def __init__(self, clip_limit: float = 2.0, tile_size: tuple = (8, 8)):
        self.clip_limit = clip_limit
        self.tile_size = tile_size

    def enhance(self, image: np.ndarray) -> tuple:
        if image is None:
            raise ValueError("Invalid image input for enhancement.")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()
        
        clahe = cv2.createCLAHE(clipLimit=self.clip_limit, tileGridSize=self.tile_size)
        contrast_enhanced = clahe.apply(gray)

        threshold = cv2.adaptiveThreshold(
            contrast_enhanced,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            21,
            10
        )

        kernel = np.ones((2, 2), np.uint8)
        cleaned_scan = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

        return gray, contrast_enhanced, cleaned_scan