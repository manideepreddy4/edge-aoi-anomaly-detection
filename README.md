# edge-aoi-anomaly-detection
PatchCore-based unsupervised anomaly detection system for industrial visual inspection with coreset optimization and real-time Streamlit UI.
# Edge AOI: High-Speed Unsupervised Anomaly Detection for Industrial Inspection

## Overview

This project is an unsupervised anomaly detection system for industrial visual inspection.

The main idea is simple: instead of training on defect images, the model learns what normal looks like and then flags anything that looks different. That fits real manufacturing settings much better, because defects are usually rare and hard to collect.

I built this project using a PatchCore-style approach with a CNN feature extractor, a memory bank of normal patch embeddings, and nearest-neighbor similarity search. I also added a Streamlit UI so the results can be tested visually.

## Why I built this

I wanted a project that is actually useful for industrial CV roles, not just another generic object detection demo.

This project is designed for situations where:
- defect samples are rare
- normal samples are available
- localization matters
- speed and memory usage matter

## Dataset

I used the **MVTec AD** dataset, which is a standard benchmark for industrial anomaly detection.

For my experiments, I focused on five categories:
- bottle
- carpet
- grid
- capsule
- transistor

These categories gave a good mix of easy cases, texture-heavy cases, and harder localization cases.

## Method

The pipeline is straightforward:

1. A pretrained CNN extracts patch-level features from normal training images.
2. All normal patch embeddings are stored in a memory bank.
3. At inference time, each test image is converted into patch embeddings.
4. The model compares those patches with the memory bank using nearest-neighbor distance.
5. Larger distances mean the image is more likely to contain an anomaly.
6. The patch scores are mapped back to an image heatmap for visualization.

I also used coreset sampling to reduce memory usage while keeping the most representative features.

## What makes this project different

A lot of student projects stop at “model runs on one dataset.”

I pushed this further by:
- testing multiple categories
- comparing 224 vs 384 resolution
- measuring image-level and pixel-level AUROC
- building a UI for live inspection
- keeping the whole pipeline reproducible

## Results

### 224 Resolution Baseline

| Category | Image AUROC | Pixel AUROC | F1 | Threshold |
|---|---:|---:|---:|---:|
| bottle | 1.0000 | 0.9542 | 1.0000 | 0.6505 |
| carpet | 0.9960 | 0.9588 | 0.9834 | 0.6002 |
| grid | 0.9699 | 0.9639 | 0.9643 | 0.5659 |
| capsule | 0.9446 | 0.9321 | 0.9636 | 0.4484 |
| transistor | 0.9996 | 0.7702 | 0.9877 | 0.6932 |

### 384 Resolution Experiment

| Category | Image AUROC | Pixel AUROC | F1 | Threshold |
|---|---:|---:|---:|---:|
| bottle | 0.9992 | 0.9648 | 0.9921 | 0.7083 |
| carpet | 0.9976 | 0.9587 | 0.9944 | 0.5993 |
| grid | 0.9841 | 0.9894 | 0.9912 | 0.6757 |
| capsule | 0.9597 | 0.9307 | 0.9820 | 0.5749 |
| transistor | 0.9837 | 0.7271 | 0.9620 | 0.7534 |

### What I learned from this
- 384 helped a lot on grid localization.
- 224 was more stable for transistor.
- There is a real trade-off between detail and robustness.

## Memory Bank Summary

The coreset step reduced the memory bank size by about 10x.

For example:
- bottle: 240,768 vectors → 24,077 vectors
- carpet: 322,560 vectors → 32,256 vectors
- grid: 304,128 vectors → 30,413 vectors

That made the system much more practical without collapsing performance.

## Visual Examples

### Bottle Example

![Bottle UI](assets/screenshots/bottle_ui.png)

### Grid Example

![Grid UI](assets/screenshots/grid_ui.png)

### Transistor Example

![Transistor UI](assets/screenshots/transistor_ui.png)

### Comparison Between 224 and 384

![224 vs 384](assets/comparisons/comparison_224.png)
![224 vs 384](assets/comparisons/comparison_384.png)

## Architecture

![Architecture](assets/screenshots/architecture.png)

## How to run

### 1. Clone and enter the project directory
```bash
git clone <repo-url>
cd MTVEC_project/edge_aoi
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

Dependencies: `torch`, `torchvision`, `numpy`, `opencv-python`, `pillow`, `scikit-learn`, `matplotlib`, `pandas`, `streamlit`

### 3. Download the MVTec AD dataset
Place the dataset under `edge_aoi/data/mvtec/` so the structure looks like:
```
edge_aoi/data/mvtec/bottle/train/good/
edge_aoi/data/mvtec/bottle/test/good/
edge_aoi/data/mvtec/bottle/test/broken_large/
...
```

### 4. Build memory banks
```bash
# From inside edge_aoi/
python -m src.build_memory --category bottle
```

### 5. Evaluate
```bash
python -m src.evaluate --category bottle
```

### 6. Run all categories at once
```bash
python run_all.py
```

### 7. Launch the Streamlit UI
```bash
streamlit run app/ui.py
```
