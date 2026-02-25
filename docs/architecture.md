# System Architecture

## Overview

The system is designed as an edge-based computer vision pipeline for detecting human presence in indoor emergency scenarios.

It integrates:

- Embedded hardware (Raspberry Pi 4)
- Camera acquisition
- YOLO-based object detection
- Alerting via Telegram Bot API

The architecture prioritizes reliability, low computational overhead, and deployability on resource-constrained devices.

---

## High-Level Architecture
---
Camera / Image Source
│
▼
Image Preprocessing (Resize + Normalization)
│
▼
YOLOv7 Inference Engine (PyTorch)
│
▼
Non-Maximum Suppression (NMS)
│
▼
Person Counting
│
▼
Image Annotation
│
▼
Telegram Alert (Image + Message)
---


---

## Components

### 1️⃣ Image Acquisition Layer

Two operating modes are supported:

- **PC Mode**
  - Static image loaded from disk
  - Used for testing and validation

- **Raspberry Pi Mode**
  - Image captured using `libcamera-still`
  - Designed for real-time deployment in classrooms

---

### 2️⃣ Preprocessing

The input image undergoes:

- Letterbox resizing to 640x640
- Tensor conversion
- Normalization (pixel values scaled to [0,1])
- Channel reordering (HWC → CHW)

This ensures compatibility with the YOLOv7 model input requirements.

---

### 3️⃣ Detection Engine

- Framework: PyTorch
- Model: YOLOv7 (custom trained weights)
- Execution: CPU (default), GPU optional

The model performs single-pass object detection and outputs bounding boxes with confidence scores.

---

### 4️⃣ Post-Processing

- Non-Maximum Suppression (NMS)
- Confidence threshold filtering (0.50)
- IoU threshold (0.45)
- Class filter: person only

Detected individuals are counted and bounding boxes are drawn on the original image.

---

### 5️⃣ Alerting System

The annotated image is:

1. Saved locally
2. Sent to Telegram via Bot API
3. Accompanied by a contextual alert message:
   - 0 people detected
   - 1 person detected
   - Multiple people detected

The system includes retry logic to handle temporary API disconnections.

---

## Edge Deployment Considerations

- CPU-optimized inference
- Model selection based on accuracy vs inference time trade-off
- Reduced complexity pipeline (no real-time streaming)
- Single-frame inference to minimize resource usage

---

## Design Decisions

- YOLOv7 selected for best precision-performance balance
- CPU-first execution for portability
- Modular structure separating detection and alert logic
- External model weights to avoid repository size inflation

---

## Scalability

The architecture can be extended to:

- Multi-camera systems
- Real-time video streaming
- Integration with centralized monitoring dashboards
- Cloud-based logging or analytics

---

## Summary

The system combines computer vision and embedded deployment principles to provide a practical emergency monitoring solution.

It demonstrates:

- Model benchmarking and selection
- Edge optimization
- API integration
- End-to-end system implementation
