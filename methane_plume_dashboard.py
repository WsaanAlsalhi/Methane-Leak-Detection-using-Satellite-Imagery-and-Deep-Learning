import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os

# ===============================
# USER INPUT
# ===============================
FILES = [
    "2026-01-26.tiff",
    "2026-01-27.tiff",
    "2026-01-28.tiff",
    "2026-01-29.tiff"
]

THRESHOLD_PERCENTILE = 99.5

# ===============================
# STORAGE
# ===============================
plume_sizes = []
plume_strengths = []
dates = []
images = []
masks = []

# ===============================
# LOAD + DETECT
# ===============================
for f in FILES:
    with rasterio.open(f) as src:
        img = src.read(1).astype(np.float32)

    threshold = np.percentile(img, THRESHOLD_PERCENTILE)
    plume_mask = img >= threshold

    plume_pixels = np.sum(plume_mask)
    background = img[~plume_mask].mean()
    plume_strength = np.sum(img[plume_mask] - background)

    plume_sizes.append(plume_pixels)
    plume_strengths.append(plume_strength)
    dates.append(f.replace(".tiff", ""))

    images.append(img)
    masks.append(plume_mask)

# ===============================
# DASHBOARD
# ===============================
n_days = len(FILES)

fig = plt.figure(figsize=(15, 4*n_days))
gs = fig.add_gridspec(n_days + 1, 3, height_ratios=[1]*n_days + [1.2])

# ---- Per-day images ----
for i in range(n_days):
    ax1 = fig.add_subplot(gs[i, 0])
    ax2 = fig.add_subplot(gs[i, 1])
    ax3 = fig.add_subplot(gs[i, 2])

    ax1.imshow(images[i], cmap="viridis")
    ax1.set_title(f"{dates[i]} – Methane")
    ax1.axis("off")

    ax2.imshow(masks[i], cmap="gray")
    ax2.set_title("Plume Mask")
    ax2.axis("off")

    ax3.imshow(images[i], cmap="viridis")
    ax3.imshow(masks[i], cmap="Reds", alpha=0.5)
    ax3.set_title("Plume Overlay")
    ax3.axis("off")

# ---- Time series plots ----
ax_size = fig.add_subplot(gs[-1, 0:2])
ax_strength = fig.add_subplot(gs[-1, 2])

ax_size.plot(dates, plume_sizes, marker="o")
ax_size.set_title("Plume Size Over Time")
ax_size.set_ylabel("Plume Pixels")
ax_size.grid(True)

ax_strength.plot(dates, plume_strengths, marker="o")
ax_strength.set_yscale("log")
ax_strength.set_title("Plume Strength (log)")
ax_strength.grid(True)

plt.tight_layout()
plt.show()
