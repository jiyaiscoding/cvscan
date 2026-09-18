import io
import cv2
import numpy as np
import streamlit as st
from PIL import Image

from modules.preprocessing import DocumentPreprocessor
from modules.document_detection import DocumentDetector
from modules.perspective import PerspectiveTransformer
from modules.enhancement import DocumentEnhancer
from modules.export import Exporter

st.set_page_config(page_title="SmartDoc Vision", page_icon="📄", layout="wide")

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "scanned_pages" not in st.session_state:
    st.session_state.scanned_pages = []

if "current_file_id" not in st.session_state:
    st.session_state.current_file_id = None

# -----------------------------------------------------------------------------
# Sidebar: Multi-Page Manager
# -----------------------------------------------------------------------------
st.sidebar.title("📚 Document Pages Manager")
st.sidebar.info(f"Total Pages Scanned: **{len(st.session_state.scanned_pages)}**")

if len(st.session_state.scanned_pages) > 0:
    if st.sidebar.button("🗑️ Clear All Pages", use_container_width=True):
        st.session_state.scanned_pages = []
        st.session_state.pop("corners", None)
        st.rerun()

    st.sidebar.markdown("### Scanned Thumbnails")
    for idx, page_data in enumerate(st.session_state.scanned_pages):
        col_thumb, col_del = st.sidebar.columns([3, 1])
        with col_thumb:
            st.image(page_data["image"], caption=f"Page {idx + 1}", use_container_width=True)
        with col_del:
            if st.button("❌", key=f"del_{idx}"):
                st.session_state.scanned_pages.pop(idx)
                st.rerun()

st.sidebar.markdown("---")

# -----------------------------------------------------------------------------
# Main Application Interface
# -----------------------------------------------------------------------------
st.title("📄 SmartDoc Vision — AI Document Scanner")
st.caption("Computer Vision Application for Automated Document Detection, Fine-Tuning & Multi-Page Export")

uploaded_file = st.file_uploader("Upload a document photo (JPG / PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Reset corner session state if a new image file is uploaded
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        if st.session_state.current_file_id != file_id:
            st.session_state.current_file_id = file_id
            st.session_state.pop("corners", None)

        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        raw_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if raw_image is None:
            st.error("Failed to decode image file.")
            st.stop()

        # 1. Preprocessing
        image = DocumentPreprocessor.resize_image(raw_image, max_width=1000)
        h, w = image.shape[:2]
        gray, blurred = DocumentPreprocessor.process_gray_and_blur(image)

        # 2. Auto Detection & State Corner Initialization
        if "corners" not in st.session_state:
            detector = DocumentDetector()
            edges = detector.detect_edges(blurred)
            auto_corners, _ = detector.find_document_corners(blurred, edges)

            if auto_corners is not None:
                st.session_state.corners = PerspectiveTransformer.order_points(auto_corners)
            else:
                st.session_state.corners = np.array([
                    [w * 0.05, h * 0.05], [w * 0.95, h * 0.05],
                    [w * 0.95, h * 0.95], [w * 0.05, h * 0.95]
                ], dtype=np.float32)

        # ---------------------------------------------------------------------
        # Sidebar: Joystick Corner Nudge Controls
        # ---------------------------------------------------------------------
        st.sidebar.header("🕹️ Corner Nudge Controls")

        target_corner = st.sidebar.radio(
            "Select Corner to Adjust:",
            ["1. Top-Left", "2. Top-Right", "3. Bottom-Right", "4. Bottom-Left"]
        )
        corner_idx = ["1. Top-Left", "2. Top-Right", "3. Bottom-Right", "4. Bottom-Left"].index(target_corner)

        step = st.sidebar.select_slider("Nudge Sensitivity (Pixels):", options=[5, 15, 30, 50], value=15)

        st.sidebar.markdown("**Directional Nudge:**")
        u_col1, u_col2, u_col3 = st.sidebar.columns([1, 1, 1])
        if u_col2.button("⬆️ Up"):
            st.session_state.corners[corner_idx][1] = max(0, st.session_state.corners[corner_idx][1] - step)

        l_col1, l_col2, l_col3 = st.sidebar.columns([1, 1, 1])
        if l_col1.button("⬅️ Left"):
            st.session_state.corners[corner_idx][0] = max(0, st.session_state.corners[corner_idx][0] - step)
        if l_col3.button("➡️ Right"):
            st.session_state.corners[corner_idx][0] = min(w, st.session_state.corners[corner_idx][0] + step)

        d_col1, d_col2, d_col3 = st.sidebar.columns([1, 1, 1])
        if d_col2.button("⬇️ Down"):
            st.session_state.corners[corner_idx][1] = min(h, st.session_state.corners[corner_idx][1] + step)

        st.sidebar.markdown("---")
        if st.sidebar.button("🔄 Reset Corners", use_container_width=True):
            st.session_state.corners = np.array([
                [w * 0.05, h * 0.05], [w * 0.95, h * 0.05],
                [w * 0.95, h * 0.95], [w * 0.05, h * 0.95]
            ], dtype=np.float32)

        selected_corners = st.session_state.corners

        # Render preview overlay
        preview_image = image.copy()
        pts_int = selected_corners.astype(np.int32).reshape((-1, 1, 2))
        cv2.polylines(preview_image, [pts_int], True, (0, 255, 0), 3)

        corner_labels = ["1 (TL)", "2 (TR)", "3 (BR)", "4 (BL)"]
        for idx, (x, y) in enumerate(selected_corners):
            color = (0, 0, 255) if idx == corner_idx else (255, 0, 0)
            cv2.circle(preview_image, (int(x), int(y)), 12, color, -1)
            cv2.putText(preview_image, corner_labels[idx], (int(x) + 12, int(y) - 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        st.subheader("1️⃣ Corner Selection Preview")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Original Photo**")
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_container_width=True)
        with col2:
            st.write(f"**Adjusted Outline** (Active: `{target_corner}`)")
            st.image(cv2.cvtColor(preview_image, cv2.COLOR_BGR2RGB), use_container_width=True)

        # 3. Perspective Correction & 4. Enhancement
        transformer = PerspectiveTransformer()
        warped = transformer.warp_perspective(image, selected_corners)

        enhancer = DocumentEnhancer()
        gray_scan, contrast_scan, final_scan = enhancer.enhance(warped)

        st.subheader("2️⃣ Flattened Output")
        st.image(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB), use_container_width=True)

        st.subheader("3️⃣ Document Enhancement Filters")
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            st.write("Grayscale")
            st.image(gray_scan, use_container_width=True)
        with ec2:
            st.write("CLAHE Contrast")
            st.image(contrast_scan, use_container_width=True)
        with ec3:
            st.write("Final Binarized Scan")
            st.image(final_scan, use_container_width=True)

        # ---------------------------------------------------------------------
        # Add Current Processed Page to Document Stack
        # ---------------------------------------------------------------------
        st.markdown("---")
        st.subheader("4️⃣ Add Page to Multi-Page Document")
        
        btn_add1, btn_add2 = st.columns([1, 2])
        with btn_add1:
            filter_choice = st.radio("Select Scan Filter for PDF/PNG export:", ("Final Binarized", "CLAHE Contrast", "Grayscale", "Color Warped"))
            
            if filter_choice == "Final Binarized":
                page_to_save = final_scan
            elif filter_choice == "CLAHE Contrast":
                page_to_save = contrast_scan
            elif filter_choice == "Grayscale":
                page_to_save = gray_scan
            else:
                page_to_save = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)

            if st.button("➕ Add Current Page to Stack", type="primary", use_container_width=True):
                st.session_state.scanned_pages.append({
                    "image": page_to_save.copy()
                })
                st.success(f"Added Page {len(st.session_state.scanned_pages)} to document stack!")
                st.rerun()

    except Exception as e:
        st.error(f"Processing Error: {str(e)}")

# -----------------------------------------------------------------------------
# Combined Multi-Page PDF Download
# -----------------------------------------------------------------------------
if len(st.session_state.scanned_pages) > 0:
    st.markdown("---")
    st.subheader("📦 Export Final Multi-Page Document")
    st.write(f"Total pages collected in current stack: **{len(st.session_state.scanned_pages)} page(s)**")

    try:
        pil_images = []
        for page_data in st.session_state.scanned_pages:
            img_arr = page_data["image"]
            if len(img_arr.shape) == 2:
                pil_img = Image.fromarray(img_arr).convert("L")
            else:
                pil_img = Image.fromarray(img_arr).convert("RGB")
            pil_images.append(pil_img)

        pdf_buffer = io.BytesIO()
        if pil_images:
            pil_images[0].save(
                pdf_buffer, format="PDF", save_all=True, append_images=pil_images[1:]
            )
            pdf_bytes = pdf_buffer.getvalue()

            exp_col1, exp_col2 = st.columns(2)
            with exp_col1:
                st.download_button(
                    label=f"📄 Download Complete PDF ({len(st.session_state.scanned_pages)} Pages)",
                    data=pdf_bytes,
                    file_name="combined_scanned_document.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            with exp_col2:
                st.info("💡 Upload a new photo above, adjust with the joystick, and click **➕ Add Current Page to Stack** to add more pages.")
    except Exception as e:
        st.error(f"Multi-page compilation error: {str(e)}")