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
