import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="TIFF Plume Analyzer",
    layout="wide"
)

# =====================================
# HEADER
# =====================================
st.title("🛰️ TIFF Image Plume Analysis")
st.markdown(
    """
Upload **any TIFF image** and this system will automatically:
- Detect plume regions
- Estimate source location
- Generate clean visual analytics
"""
)

# =====================================
# UPLOAD
# =====================================
uploaded_file = st.file_uploader(
    "Upload TIFF image",
    type=["tif", "tiff"]
)

if uploaded_file:

    # =====================================
    # READ TIFF
    # =====================================
    with rasterio.open(uploaded_file) as src:
        image = src.read(1).astype(np.float32)

    # =====================================
    # NORMALIZATION
    # =====================================
    image = np.nan_to_num(image)
    norm = (image - image.min()) / (image.max() - image.min())

    # =====================================
    # PLUME DETECTION
    # =====================================
    threshold = np.percentile(norm, 99.5)
    plume_mask = norm >= threshold

    # =====================================
    # SOURCE ESTIMATION
    # =====================================
    ys, xs = np.where(plume_mask)
    if len(xs) > 0:
        source_x = int(xs.mean())
        source_y = int(ys.mean())
    else:
        source_x = source_y = None

    # =====================================
    # STATS
    # =====================================
    st.divider()
    st.subheader("📊 Image Statistics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Min", f"{image.min():.2f}")
    col2.metric("Max", f"{image.max():.2f}")
    col3.metric("Mean", f"{image.mean():.2f}")
    col4.metric("Std", f"{image.std():.2f}")

    # =====================================
    # VISUALIZATION
    # =====================================
    st.divider()
    st.subheader("🖼️ Visual Results")

    colA, colB, colC = st.columns(3)

    with colA:
        st.markdown("**Original Image**")
        fig, ax = plt.subplots()
        ax.imshow(image, cmap="viridis")
        ax.axis("off")
        st.pyplot(fig)

    with colB:
        st.markdown("**Plume Mask**")
        fig, ax = plt.subplots()
        ax.imshow(plume_mask, cmap="gray")
        ax.axis("off")
        st.pyplot(fig)

    with colC:
        st.markdown("**Overlay + Source**")
        fig, ax = plt.subplots()
        ax.imshow(image, cmap="viridis")
        ax.imshow(plume_mask, cmap="Reds", alpha=0.45)

        if source_x is not None:
            ax.scatter(source_x, source_y, c="cyan", s=60, marker="x")
            ax.text(source_x+3, source_y+3, "Source", color="cyan")

        ax.axis("off")
        st.pyplot(fig)

    # =====================================
    # HISTOGRAM
    # =====================================
    st.divider()
    st.subheader("📈 Pixel Distribution")

    fig, ax = plt.subplots()
    ax.hist(image.flatten(), bins=100)
    ax.axvline(image.mean(), linestyle="--")
    ax.set_xlabel("Pixel Value")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # =====================================
    # SUMMARY
    # =====================================
    st.success("Plume analysis completed successfully.")

else:
    st.info("Please upload a TIFF image to start analysis.")
