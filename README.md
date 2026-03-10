# Methane Leak Detection using Satellite Imagery and Deep Learning

## Overview

This project focuses on detecting and tracking methane (CH₄) emissions using satellite imagery and deep learning techniques. Methane is a potent greenhouse gas with a significant impact on global warming. Early detection of methane leaks is essential for environmental monitoring and mitigation.

The system processes satellite imagery, identifies methane hotspots, and performs segmentation using deep learning models to visualize methane plume distribution.

## Objectives

* Detect methane emission hotspots from satellite imagery.
* Segment methane plumes using deep learning.
* Track methane dispersion over time.
* Provide visual outputs for environmental monitoring.

## Data Sources

Satellite imagery used in this project includes:

* Sentinel-2
* Landsat 8 / Landsat 9
* High-resolution Earth observation datasets

These datasets provide multispectral images that allow analysis of atmospheric gas patterns.

## Methodology

### 1. Data Acquisition

Satellite images are collected from open Earth observation datasets.

### 2. Preprocessing

* Image normalization
* Band selection
* Noise removal
* Resizing images for model input

### 3. Methane Hotspot Detection

Potential methane emission areas are identified using spectral analysis and thresholding techniques.

### 4. Deep Learning Model

A convolutional neural network is used for segmentation.

Model architecture:

* U-Net / CNN
* Binary segmentation (Methane / No Methane)

### 5. Training Pipeline

Steps include:

* Dataset splitting (train / validation / test)
* Model training
* Loss optimization
* Performance evaluation

### 6. Visualization

Results are exported as:

* PNG segmentation maps
* Heatmaps of methane concentration
* Satellite overlays showing plume spread


### Launch visualization interface

```
streamlit run methane_app.py
```

## Applications

* Environmental monitoring
* Oil and gas leak detection
* Climate research
* Smart environmental management systems

## Future Improvements

* Integrate real-time satellite feeds
* Improve detection accuracy using larger datasets
* Deploy the model as a cloud service
* Add temporal methane dispersion tracking

## Author

Wasan Al-Salhi
Mariam Al-Risi

This project is intended for research and educational purposes.

