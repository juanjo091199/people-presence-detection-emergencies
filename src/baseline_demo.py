import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "third_party" / "yolov7"))

import cv2
import torch

from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box


MODEL_PATH = "models/modelo_yolov7_final.pt"
IMAGE_PATH = "assets/foto1.png"
OUTPUT_PATH = "results/deteccion.png"

DEVICE = "cpu"
IMG_SIZE = 640
CONF_THRES = 0.25
IOU_THRES = 0.45


def main():
    device = torch.device(DEVICE)
    model = attempt_load(MODEL_PATH, map_location=device)
    model.eval()

    img0 = cv2.imread(IMAGE_PATH)
    if img0 is None:
        raise RuntimeError(f"No se pudo leer la imagen: {IMAGE_PATH}")

    img = letterbox(img0, new_shape=IMG_SIZE)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1).copy()
    img = torch.from_numpy(img).to(device).float()
    img /= 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    with torch.no_grad():
        pred = model(img, augment=False)[0]

    pred = non_max_suppression(pred, CONF_THRES, IOU_THRES)

    num_personas = 0
    for det in pred:
        if det is None or len(det) == 0:
            continue
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()
        for *xyxy, conf, cls in reversed(det):
            plot_one_box(xyxy, img0, label="persona", line_thickness=2)
            num_personas += 1

    Path("results").mkdir(exist_ok=True)
    cv2.imwrite(OUTPUT_PATH, img0)
    print(f"OK. Personas detectadas: {num_personas} | Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
