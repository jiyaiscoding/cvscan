import cv2
import numpy as np

class PerspectiveTransformer:
    @staticmethod
    def order_points(points: np.ndarray) -> np.ndarray:
        points = points.reshape(4, 2)
        ordered = np.zeros((4, 2), dtype=np.float32)

        sum_pts = points.sum(axis=1)
        ordered[0] = points[np.argmin(sum_pts)]
        ordered[2] = points[np.argmax(sum_pts)]

        diff_pts = np.diff(points, axis=1)
        ordered[1] = points[np.argmin(diff_pts)]
        ordered[3] = points[np.argmax(diff_pts)]

        return ordered

    def warp_perspective(self, image: np.ndarray, corners: np.ndarray) -> np.ndarray:
        if image is None or corners is None:
            raise ValueError("Invalid parameters passed to perspective transformation.")

        ordered_corners = self.order_points(corners)
        top_left, top_right, bottom_right, bottom_left = ordered_corners

        width_top = np.linalg.norm(top_right - top_left)
        width_bottom = np.linalg.norm(bottom_right - bottom_left)
        max_width = max(int(width_top), int(width_bottom))

        height_left = np.linalg.norm(bottom_left - top_left)
        height_right = np.linalg.norm(bottom_right - top_right)
        max_height = max(int(height_left), int(height_right))

        destination = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype=np.float32)

        matrix = cv2.getPerspectiveTransform(ordered_corners, destination)
        warped = cv2.warpPerspective(image, matrix, (max_width, max_height))
        return warped