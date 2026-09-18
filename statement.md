# Project Statement & Scope: SmartDoc Vision

## Problem Statement
In daily academic and professional workflows, users frequently receive document photos, lecture slides, or paper assignments directly on their laptops via email, messaging platforms, or cloud storage. However, existing document scanning and flattening applications are predominantly mobile-first. This forces users into an inefficient transfer loop: downloading the raw image on a PC, transferring it to a mobile phone to run through a scanning app, and then sending the cleaned file back to the laptop for submission. SmartDoc Vision eliminates this back-and-forth friction by offering a native desktop Computer Vision application built with Streamlit and OpenCV. It allows users to process, correct, enhance, and compile document images directly on their laptops with automatic boundary detection, custom coordinate tuning, and high-contrast filtering.

## Scope of the Project
SmartDoc Vision bridges automated feature extraction with fine-grained user overrides in a clean desktop interface:

* **Automated Boundary Detection**: Implements morphological operations and contour analysis using OpenCV to locate document edges automatically with safe fallback boundaries.
* **Fine-Tuned Interactive Controls**: Provides a custom directional joystick UI in Streamlit to allow users to make sub-pixel and multi-pixel 2D coordinate adjustments (±1px, ±5px) to refine document corners on a laptop screen.
* **Perspective Correction**: Applies 4-point homography transformations to re-project tilted or skewed document boundaries into flat, top-down rectangular digital outputs.
* **Image Enhancement Pipeline**: Integrates contrast enhancement (CLAHE) and adaptive binarization to clean up shadows, improve legibility, and convert raw photos into document-grade outputs.
* **Multi-Page Compilation**: Manages session state to stash individual processed pages during a study session and export them into a unified PDF file.

### Platform & Technical Scope
* **Target Platform**: Optimized specifically for PC and laptop desktop browsers running Streamlit.
* **Input Specifications**: Single-page image files (`.jpg`, `.jpeg`, `.png`) uploaded directly through the user interface.
* **Output Specifications**: Processed high-contrast document images and multi-page concatenated PDF files.

### Architectural Boundaries & Limitations
* **Camera Capture**: The application processes pre-captured uploaded images; it does not connect directly to real-time flatbed hardware scanners or live mobile video streams.
* **Complex Backgrounds**: Auto-detection depends on contrast between the document and its surrounding surface. Highly textured or visually noisy backgrounds may require manual joystick adjustment.
* **OCR Integration**: The current scope focuses exclusively on image processing, geometric transformation, and document enhancement; Optical Character Recognition (OCR) text extraction is out of scope.

## Target Users
* **Students & Academics**: Individuals needing to digitize physical assignments, whiteboard notes, and reference books directly on their laptops without mobile transfer steps.
* **Remote Workers & Professionals**: Users handling receipts, contracts, and administrative paperwork from desktop workstations.
* **Computer Vision Developers**: Enthusiasts seeking a modular reference implementation of Streamlit-based interactive contour detection and homography transformations.

## High-Level Features
* **Desktop-First Dual-Column Layout**: Real-time side-by-side comparison between raw image input and transformed document outputs.
* **Intelligent Edge & Fallback Detection**: Automatic 4-corner contour discovery with automatic boundary bounding if contours fail.
* **Directional Joystick Fine-Tuning**: Mouse-driven 2D coordinate nudges for precise corner adjustment on high-resolution screens.
* **Advanced Document Filtering**: One-click switching between Original, Grayscale, CLAHE Contrast Equalization, and Adaptive Gaussian Binarization.
* **Session-Based PDF Stashing**: Interactive page queuing to compile multiple processed documents into a single downloadable PDF stream.