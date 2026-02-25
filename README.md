
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
docs/ → architecture diagrams, demo media, thesis (sanitized)
src/ → inference + alerting code (edge deployment)
notebooks/ → training / evaluation notebooks (with notes)
results/ → metrics summary, figures, comparisons
data/ → dataset instructions (no raw data unless allowed)


## Results (high level)
- Best model selected: **YOLOv7**
- Metric highlights and inference-time comparisons are documented in `results/`.

## Reproducibility (coming next)
- [ ] Setup instructions
- [ ] Inference script on Raspberry Pi
- [ ] Telegram alert configuration
- [ ] Model evaluation summary

## Attribution
Model training was performed using the official training pipelines/notebooks provided by the YOLO repositories.  
This project focuses on **dataset preparation, fine-tuning configuration, evaluation, and edge deployment integration**.

## License
MIT
