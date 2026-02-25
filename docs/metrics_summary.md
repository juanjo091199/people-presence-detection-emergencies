# Model Training & Evaluation Summary

## Dataset Description

The dataset was created for indoor emergency monitoring scenarios, containing annotated images of people in enclosed classroom environments.

- Annotation platform: Roboflow
- Format: YOLO
- Train/Validation/Test split applied during training
- Indoor scenarios evaluated:
  - Full classroom
  - Half-filled classroom
  - Few people
  - Empty classroom
  - Low-light condition

---

## Model Comparison

Three models were trained and evaluated:

- YOLOv5s
- YOLOv5x
- YOLOv7

Evaluation focused on:

- Detection precision
- Inference time on Raspberry Pi 4 Model B
- Robustness under different occupancy and lighting conditions

---

## Precision Results (Average)

| Model     | Average Precision (%) |
|-----------|----------------------|
| YOLOv5s   | 94.64% |
| YOLOv5x   | 94.28% |
| YOLOv7    | 96.08% |

YOLOv7 achieved the highest average precision among the three evaluated models.

---

## Inference Time on Raspberry Pi 4 (Average)

| Model     | Average Inference Time (seconds) |
|-----------|----------------------------------|
| YOLOv5s   | 6.97 s |
| YOLOv5x   | 25.01 s |
| YOLOv7    | 16.96 s |

YOLOv5s was the fastest model, but YOLOv7 offered a better balance between detection accuracy and computational cost.

---

## Final Model Selection Rationale

Although YOLOv5s provided the lowest inference time, YOLOv7 was selected for deployment because:

- It achieved the highest precision (≈96%)
- It maintained acceptable inference time for emergency monitoring
- It demonstrated stable performance across all classroom scenarios
- It provided a better accuracy-performance trade-off for edge deployment

---

## Deployment Configuration

- Confidence threshold: 0.50
- IoU threshold: 0.45
- Only "person" class considered
- CPU-based inference (optimized for Raspberry Pi 4)

---

## Conclusion

YOLOv7 was determined to be the most suitable model for emergency indoor monitoring scenarios, balancing reliability, robustness, and computational feasibility on embedded hardware.
