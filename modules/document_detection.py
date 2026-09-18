# modules/document_detection.py
import cv2
import numpy as np

class DocumentDetector:
    def __init__(self, canny_low: int = 50, canny_high: int = 150):
        self.canny_low = canny_low
        self.canny_high = canny_high

    def detect_edges(self, blurred_image: np.ndarray) -> np.ndarray:
        edges = cv2.Canny(blurred_image, self.canny_low, self.canny_high)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        return closed_edges

    def find_document_corners(self, blurred_image: np.ndarray, closed_edges: np.ndarray) -> tuple:
        h, w = blurred_image.shape[:2]
        image_area = h * w
        
        # Strategy A: Contour Approximation
        contours, _ = cv2.findContours(closed_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 0.20 * image_area or area > 0.85 * image_area:
                continue
            
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            if len(approx) == 4 and cv2.isContourConvex(approx):
                return approx, "Canny Contour Detection"

        # Strategy B: Fallback Standard Page Frame
        margin_x, margin_y = int(w * 0.05), int(h * 0.05)
        fallback = np.array([
            [[margin_x, margin_y]],
            [[w - margin_x, margin_y]],
            [[w - margin_x, h - margin_y]],
            [[margin_x, h - margin_y]]
        ], dtype=np.int32)

        return fallback, "Bounding Box Fallback"