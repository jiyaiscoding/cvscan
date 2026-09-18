# SmartDoc Vision 

> SmartDoc Vision is a Computer Vision desktop application built with Python, OpenCV, and Streamlit, specifically optimized for PCs and laptops to process and clean up uploaded document photos. Designed for wide-screen desktop displays, the application provides side-by-side visual analysis to transform uneven, perspective-distorted document images into crisp, flattened digital documents.
> The core pipeline features automatic 4-corner contour detection with fallback boundary safeguards, an interactive directional joystick UI for desktop coordinate fine-tuning, advanced contrast enhancement via CLAHE and adaptive binarization filters, and session-based multi-page state management for unified PDF exports.

---

##  Key Features

* **PC & Laptop Optimized:** Designed for wide-screen desktop displays with side-by-side image comparison columns and dedicated mouse-driven sidebar controls.
* **Automated Corner Detection:** Uses Canny edge detection, morphological dilation, and contour approximation to isolate document boundaries reliably.
* **Interactive Directional Joystick:** Allows precise $2\text{D}$ coordinate nudges ($\pm1\text{px}$, $\pm5\text{px}$) for manual fine-tuning without heavy canvas dependencies.
* **Homography Perspective Transformation:** Warps skewed document regions into flat, top-down rectangular outputs using destination matrix mappings.
* **Adaptive Enhancement Filters:** Integrates Grayscale conversion, CLAHE (Contrast Limited Adaptive Histogram Equalization) for shadow equalization, and Adaptive Gaussian Binarization for clean text extraction.
* **Multi-Page Compilation:** Features interactive page stashing to combine multiple processed document pages into a single, downloadable PDF file.

---

## 📁 Repository Structure

```text
SmartDoc_Computer-Vision/
├── modules/
│   ├── __init__.py
│   ├── preprocessing.py       # Image resizing, color conversions, blurring
│   ├── document_detection.py  # Edge detection, contour analysis, joystick logic
│   ├── perspective.py         # 4-point ordering, matrix transformation, warping
│   ├── enhancement.py         # Grayscale, CLAHE, Adaptive Binarization
│   └── export.py              # Single/Multi-page PIL image compilation & PDF export
├── tests/
│   ├── __init__.py
│   └── test_processing.py     # Pytest unit tests for transformation math & edge cases
├── sample_images/             # Test document samples
├── app.py                     # Primary Streamlit desktop UI dashboard
├── requirements.txt           # Project dependencies
├── statement.md               # Project scope and problem statement
└── README.md                  # Documentation

---

**Installation & Setup**
**1. Prerequisites**
Ensure you have Python 3.9+ installed on your system.

**2. Clone Repository**
git clone [https://github.com/Aristhi/SmartDoc_Computer-Vision.git](https://github.com/Aristhi/SmartDoc_Computer-Vision.git)
cd SmartDoc_Computer-Vision

**3. Create & Activate Virtual Environment**
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS / Linux
python3 -m venv venv
source venv/bin/activate

**4. Install Dependencies**
pip install -r requirements.txt

**Running the Application:**

Launch the desktop UI dashboard locally via Streamlit:
streamlit run app.py

Steps:
i. Open your browser at http://localhost:8501.

ii. Upload a document image (.jpg, .jpeg, .png) or use a sample image.

iii. Adjust corner detection sensitivity or use the Joystick Controls to fine-tune bounds.

iv. Select your preferred filter (Original, Grayscale, CLAHE, or Adaptive Binarization).

v. Add the processed page to your session and export as a single or multi-page PDF.

**Instructions for testing**

Execute the automated test suite to verify pipeline transformations and edge cases:
pytest

**Technologies Used:**

**OpenCV** - Core Computer Vision image processing pipeline.
**Streamlit** - Desktop application framework and interactive session handling.
**NumPy** - Vectorized matrix operations and coordinate mathematical transformations.
**Pillow (PIL)** - Image file format handling and PDF byte stream rendering.

---

## Application Screenshots

<p align="center">
  <img src="Images/Screenshot%202026-09-18%20205330.png" width="400" alt="UI Dashboard"/>
  <img src="Images/Screenshot%202026-09-18%20205731.png" width="400" alt="Document Upload"/>
</p>

<p align="center">
  <img src="Images/Screenshot%202026-09-18%20205825.png" width="400" alt="Boundary Detection"/>
  <img src="Images/Screenshot%202026-09-18%20205837.png" width="400" alt="Joystick Tuning"/>
</p>

<p align="center">
  <img src="Images/Screenshot%202026-09-18%20205848.png" width="400" alt="Perspective Correction"/>
  <img src="Images/Screenshot%202026-09-18%20205853.png" width="400" alt="Image Filtering"/>
</p>

<p align="center">
  <img src="Images/Screenshot%202026-09-18%20205859.png" width="400" alt="Multi-Page Queue"/>
  <img src="Images/Screenshot%202026-09-18%20205904.png" width="400" alt="PDF Export"/>
</p>

---
