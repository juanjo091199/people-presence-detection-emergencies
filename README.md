
# People Presence Detection for Emergencies (YOLOv7 + Raspberry Pi + Telegram)
Embedded computer vision system that detects **human presence** in indoor spaces during emergencies to support faster evacuation and rescue decisions.  
This project was developed as an academic capstone thesis at **Universidad Técnica del Norte (Ecuador, 2024)**.

## Why this matters
During emergencies, verifying whether someone remains inside a room often requires manual checks, which can delay rescue response.  
This system automates presence detection and sends an alert with an annotated image to security staff.

## What I built
- **Embedded device** (Raspberry Pi 4) with a camera to capture images.
- **Object detection model** (YOLO family) to detect and count people.
- **Alerting pipeline**: sends notification + image via **Telegram Bot API**.
- **Model benchmarking**: compared YOLOv5s, YOLOv5x and YOLOv7 and selected the best trade-off for the device.

## Tech Stack
- Python
- PyTorch
- OpenCV
- YOLOv5 / YOLOv7
- Raspberry Pi 4
- Telegram Bot API
- Roboflow (dataset labeling / export)

## Repository structure
