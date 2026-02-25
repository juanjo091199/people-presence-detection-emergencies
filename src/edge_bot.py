import os
import sys
import time
import subprocess
from pathlib import Path

import cv2
import torch
import telepot
import urllib3

# --- YOLOv7 path (third_party/yolov7) ---
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "third_party" / "yolov7"))

from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box


# ==============================
# CONFIG
# ==============================

MODEL_PATH = "models/best.pt"
IMAGE_PATH = "assets/sample.jpg"
OUTPUT_PATH = "results/deteccion.jpg"

IMG_SIZE = 640
CONF_THRES = 0.50
IOU_THRES = 0.45

MAX_RETRIES = 3

# Mode selection (manual comment/uncomment)
USE_RASPBERRY_CAMERA = False  # <-- PC mode by default


# Telegram: set these as environment variables (recommended)
# Windows (cmd):
#   set TELEGRAM_BOT_TOKEN=xxxxx
#   set TELEGRAM_CHAT_ID=123456789   (optional)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")  # optional


# ==============================
# TELEGRAM HELPERS
# ==============================

def enviar_mensaje_con_reintentos(bot, chat_id, mensaje, intentos=MAX_RETRIES):
    while intentos > 0:
        try:
            bot.sendMessage(chat_id, mensaje)
            return
        except urllib3.exceptions.ProtocolError as e:
            print(f"[telegram] Error de conexión: {e}")
            intentos -= 1
            if intentos > 0:
                print("[telegram] Reintentando en 5 segundos...")
                time.sleep(5)
    print("[telegram] Agotados los intentos. No se pudo enviar el mensaje.")


def mensaje_alerta(num_personas: int) -> str:
    if num_personas == 0:
        return "No se han encontrado personas"
    if num_personas == 1:
        return "*****ALERTA*****\nSe detectó 1 persona"
    return f"*****ALERTA*****\nSe detectaron {num_personas} personas"


# ==============================
# IMAGE ACQUISITION (2 modes)
# ==============================

def capturar_imagen() -> "cv2.Mat":
    """
    2 modes:
      - PC image file (IMAGE_PATH)
      - Raspberry Pi camera (libcamera-still) -> OUTPUT_PATH, then read
    """
    if USE_RASPBERRY_CAMERA:
        Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["libcamera-still", "-o", OUTPUT_PATH], check=True)
        img = cv2.imread(OUTPUT_PATH)
    else:
        img = cv2.imread(IMAGE_PATH)

    if img is None:
        raise RuntimeError("No se pudo cargar la imagen (revisa IMAGE_PATH o libcamera).")
    return img


# ==============================
# DETECTION
# ==============================

def detectar_personas(model, img_bgr: "cv2.Mat") -> tuple[int, "cv2.Mat"]:
    img_original = img_bgr.copy()

    # Preprocess (edge-friendly)
    img = letterbox(img_bgr, new_shape=(IMG_SIZE, IMG_SIZE))[0]
    img = img[:, :, ::-1].copy()  # BGR->RGB + avoid negative strides

    tensor = torch.from_numpy(img).float() / 255.0
    tensor = tensor.permute(2, 0, 1).unsqueeze(0)  # CHW + batch

    with torch.no_grad():
        pred = model(tensor, augment=False)[0]

    # Only person class (COCO-style)
    pred = non_max_suppression(pred, CONF_THRES, IOU_THRES, classes=0, agnostic=False)

    num_personas = 0
    for det in pred:
        if det is None or len(det) == 0:
            continue

        det[:, :4] = scale_coords(tensor.shape[2:], det[:, :4], img_original.shape).round()

        for *xyxy, conf, cls in reversed(det):
            plot_one_box(xyxy, img_original, label="persona", line_thickness=2)
            num_personas += 1

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(OUTPUT_PATH, img_original)

    return num_personas, img_original


# ==============================
# MAIN (Telegram loop always on)
# ==============================

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError(
            "Falta TELEGRAM_BOT_TOKEN. Configúralo como variable de entorno.\n"
            "Windows: set TELEGRAM_BOT_TOKEN=xxxxx"
        )

    # Load model
    device = torch.device("cpu")
    model = attempt_load(MODEL_PATH, map_location=device)
    model.eval()

    bot = telepot.Bot(TELEGRAM_BOT_TOKEN)

    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != "text":
            return

        text = msg.get("text", "").strip()

        # Command to trigger detection
        if text == "/foto":
            try:
                img = capturar_imagen()
                num_personas, _ = detectar_personas(model, img)

                # Send photo
                target_chat = TELEGRAM_CHAT_ID if TELEGRAM_CHAT_ID else chat_id
                with open(OUTPUT_PATH, "rb") as photo:
                    bot.sendPhoto(target_chat, photo)

                # Send alert message
                enviar_mensaje_con_reintentos(bot, target_chat, mensaje_alerta(num_personas))

                print(f"/foto procesado | personas={num_personas} | output={OUTPUT_PATH}")

            except Exception as e:
                print(f"[error] {e}")
                enviar_mensaje_con_reintentos(bot, chat_id, f"Error ejecutando detección: {e}")

    bot.message_loop(handle)
    print("✅ Bot corriendo. Envía /foto para capturar/detectar. (Ctrl+C para salir)")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
