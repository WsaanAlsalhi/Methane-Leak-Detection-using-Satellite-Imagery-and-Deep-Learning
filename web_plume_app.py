import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🛰️ Methane Plume Detection Web App")

st.markdown("""
Upload **2 to 5 Sentinel-5P TIFF images**  
The app will:
- Display images
- Compute differences
- Detect methane plumes
""")

# ============================
# Upload TIFF files
# ============================
uploaded_files = st.file_uploader(
    "Upload TIFF images (2–5 files)",
    type=["tiff", "tif"],
    accept_multiple_files=True
)

if uploaded_files and 2 <= len(uploaded_files) <= 5:

    images = []
    names = []

    for file in uploaded_files:
        with rasterio.open(file) as src:
            img = src.read(1).astype(np.float32)
            images.append(img)
            names.append(file.name)

    st.divider()
    st.subheader("📌 Original Methane Images")

    cols = st.columns(len(images))
    for i, col in enumerate(cols):
        with col:
            fig, ax = plt.subplots()
            im = ax.imshow(images[i], cmap="viridis")
            ax.set_title(names[i])
            plt.colorbar(im, ax=ax)
            st.pyplot(fig)

    # ============================
    # Differences
    # ============================
    st.divider()
    st.subheader("📉 Temporal Differences")

    diffs = []
    diff_cols = st.columns(len(images) - 1)

    for i in range(1, len(images)):
        diff = images[i] - images[i - 1]
        diffs.append(diff)

        with diff_cols[i - 1]:
            fig, ax = plt.subplots()
            im = ax.imshow(diff, cmap="bwr")
            ax.set_title(f"{names[i]} - {names[i-1]}")
            plt.colorbar(im, ax=ax)
            st.pyplot(fig)

    # ============================
    # Plume Detection
    # ============================
    st.divider()
    st.subheader("🔥 Plume Detection")

    plume_cols = st.columns(len(images))

    for i, img in enumerate(images):
        mean = np.mean(img)
        std = np.std(img)
        
        threshold = np.percentile(img, 98)
        plume_mask = (img >= threshold).astype(np.uint8)


        plume_pixels = plume_mask.sum()

        with plume_cols[i]:
            fig, ax = plt.subplots()
            ax.imshow(plume_mask, cmap="gray")
            ax.set_title(f"{names[i]}\nPlume pixels: {plume_pixels}")
            st.pyplot(fig)

    # ============================
    # Source Estimation
    # ============================
    st.divider()
    st.subheader("📍 Estimated Plume Sources")

    source_cols = st.columns(len(images))

    for i, img in enumerate(images):
        mean = np.mean(img)
        std = np.std(img)
        plume_mask = img > (mean + 2.5 * std)

        coords = np.column_stack(np.where(plume_mask))

        with source_cols[i]:
            if len(coords) > 0:
                y, x = coords.mean(axis=0).astype(int)
                fig, ax = plt.subplots()
                ax.imshow(img, cmap="viridis")
                ax.scatter(x, y, c="red", s=40)
                ax.set_title(f"{names[i]}\nEstimated Source")
                st.pyplot(fig)
            else:
                st.write(f"{names[i]}")
                st.write("No plume detected")

else:
    st.info("Please upload between **2 and 5 TIFF images**.")
