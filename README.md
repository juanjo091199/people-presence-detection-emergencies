
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

# People Presence Detection for Emergency Monitoring

This project implements a **YOLOv7-based person detection system** designed for emergency monitoring scenarios.

It was developed as part of an engineering thesis and optimized for:

- 🖥 PC (image-based inference)
- 🍓 Raspberry Pi 4 Model B (camera-based capture)
- 🤖 Telegram Bot integration for remote alerts

The system detects people in an image and sends real-time alerts via Telegram.

---

## 📌 Features

- Person detection using a custom YOLOv7 trained model
- Configurable confidence and IoU thresholds
- Telegram bot integration
- Compatible with CPU (default)
- Optional Raspberry Pi camera capture (libcamera)

---

## 📂 Project Structure
people-presence-detection-emergencies/
│
├── src/
│ └── edge_detector_bot.py
│
├── third_party/
│ └── yolov7/ (must be cloned manually)
│
├── models/ (place your .pt model here)
├── assets/ (test images)
├── results/ (output images)
│
├── requirements.txt
└── README.md

---

## ⚙ Installation (Windows + Conda Recommended)

### 1️⃣ Create environment


conda create -n peoplebot python=3.10 -y
conda activate peoplebot
2️⃣ Install compatible PyTorch (CPU)
conda install -y pytorch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 cpuonly -c pytorch
3️⃣ Install project dependencies
pip install -r requirements.txt
4️⃣ Clone YOLOv7 into third_party
mkdir third_party
cd third_party
git clone https://github.com/WongKinYiu/yolov7
cd ..
5️⃣ Install YOLOv7 dependencies
pip install -r requirements.txt
📦 Model Setup

Place your trained YOLOv7 model inside:

models/best.pt

The model file is not included in this repository.

▶ Running the Bot (PC Mode)

Set your Telegram token:

set TELEGRAM_BOT_TOKEN=YOUR_TOKEN

Run:

python src/edge_detector_bot.py

In Telegram, send:

/foto

The bot will:

Load the test image

Perform detection

Send the annotated image

Send an alert message

🍓 Raspberry Pi Mode

Open edge_detector_bot.py and set:

USE_RASPBERRY_CAMERA = True

Ensure libcamera-still is installed on the Raspberry Pi.

Then run:

python3 src/edge_detector_bot.py
🖥 Optional: GPU (CUDA)

If you have an NVIDIA GPU, you may install the CUDA-enabled version of PyTorch from:

https://pytorch.org/get-started/locally/

Then change:

device = torch.device("cpu")

to:

device = torch.device("cuda")
🧠 Technical Notes

PyTorch is installed via Conda to ensure binary compatibility on Windows.

Other dependencies are installed via pip.

Designed for CPU-first execution for maximum compatibility.

Optimized detection pipeline for low-resource environments.

📄 License

This project is for academic and research purposes.

## License
MIT
