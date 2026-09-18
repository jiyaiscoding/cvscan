import cv2
import io
import numpy as np
from PIL import Image

class Exporter:
    @staticmethod
    def image_to_bytes(image: np.ndarray, format_ext: str = "PNG") -> bytes:
        if len(image.shape) == 3:
            pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            pil_img = Image.fromarray(image)
        
        buffer = io.BytesIO()
        pil_img.save(buffer, format=format_ext.upper())
        return buffer.getvalue()

    @staticmethod
    def image_to_pdf_bytes(image: np.ndarray) -> bytes:
        if len(image.shape) == 3:
            pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            pil_img = Image.fromarray(image)
        
        buffer = io.BytesIO()
        pil_img.save(buffer, format="PDF", resolution=100.0)
        return buffer.getvalue()