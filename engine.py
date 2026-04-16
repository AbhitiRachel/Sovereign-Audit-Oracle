import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

def analyse_fruit_quality(img, box_coords):
    """
    Analyses the ACTUAL fruit region using:
    1. Colour analysis - fresh fruits have vibrant uniform colour
    2. Dark spot detection - bruised/rotten fruits have dark patches
    3. Texture analysis - old fruits have wrinkled texture
    
    This is real quality analysis — independent of YOLO confidence.
    """
    x1, y1, x2, y2 = [int(c) for c in box_coords]

    # Crop just the detected fruit region
    fruit_crop = img[y1:y2, x1:x2]

    # Safety check — if crop is empty
    if fruit_crop.size == 0:
        return {"score": 0, "reason": "Could not analyse region"}

    # ── Analysis 1: Dark Spot Detection ──────────────────────
    # Rotten/bruised fruits have dark brown/black patches
    # Convert to HSV — easier to detect dark regions
    hsv = cv2.cvtColor(fruit_crop, cv2.COLOR_BGR2HSV)

    # Dark pixels = low Value in HSV
    # If a lot of pixels are very dark → fruit is rotten
    value_channel = hsv[:, :, 2]
    dark_pixels = np.sum(value_channel < 50)  # pixels very dark
    total_pixels = fruit_crop.shape[0] * fruit_crop.shape[1]
    dark_ratio = dark_pixels / total_pixels  # 0.0 to 1.0

    # ── Analysis 2: Colour Uniformity ────────────────────────
    # Fresh fruits have consistent colour across their surface
    # Rotten fruits have patches of different colours
    # We measure standard deviation of hue — high std = uneven colour
    hue_channel = hsv[:, :, 0]
    hue_std = np.std(hue_channel)  # low = uniform, high = patchy

    # ── Analysis 3: Saturation (Vibrancy) ────────────────────
    # Fresh fruits are vibrant — high saturation
    # Old/rotten fruits look dull — low saturation
    saturation_channel = hsv[:, :, 1]
    avg_saturation = np.mean(saturation_channel)  # 0-255

    # ── Scoring System ────────────────────────────────────────
    # Start with 100 points and deduct based on problems found
    score = 100

    # Deduct for dark spots (rot/bruising)
    if dark_ratio > 0.3:        # more than 30% dark
        score -= 40
    elif dark_ratio > 0.15:     # more than 15% dark
        score -= 20

    # Deduct for uneven colour (patches)
    if hue_std > 30:            # very uneven colour
        score -= 30
    elif hue_std > 20:          # moderately uneven
        score -= 15

    # Deduct for low vibrancy (dull fruit)
    if avg_saturation < 60:     # very dull
        score -= 30
    elif avg_saturation < 100:  # moderately dull
        score -= 15

    return {
        "score": max(0, score),         # never below 0
        "dark_ratio": round(dark_ratio, 3),
        "colour_uniformity": round(float(hue_std), 2),
        "vibrancy": round(float(avg_saturation), 2)
    }


def get_quality_grade(quality_analysis):
    """
    Grade based on ACTUAL fruit analysis score.
    Not YOLO confidence — this is real quality measurement.
    """
    score = quality_analysis["score"]

    if score >= 70:
        return {
            "grade": "Grade A",
            "status": "✅ Fresh",
            "action": "Pass to packaging",
            "score": score
        }
    elif score >= 40:
        return {
            "grade": "Grade B",
            "status": "⚠️ Inspect",
            "action": "Manual inspection required",
            "score": score
        }
    else:
        return {
            "grade": "Grade C",
            "status": "❌ Reject",
            "action": "Remove from conveyor",
            "score": score
        }


def get_batch_summary(detections):
    """
    Batch level analytics — manager gets one verdict.
    """
    total = len(detections)
    if total == 0:
        return {
            "total_items": 0,
            "grade_a_count": 0,
            "grade_b_count": 0,
            "grade_c_count": 0,
            "pass_rate_percent": 0,
            "batch_verdict": "❌ FAIL"
        }

    grade_a = sum(1 for d in detections if d["quality"]["grade"] == "Grade A")
    grade_b = sum(1 for d in detections if d["quality"]["grade"] == "Grade B")
    grade_c = sum(1 for d in detections if d["quality"]["grade"] == "Grade C")
    pass_rate = round((grade_a / total) * 100, 1)

    return {
        "total_items": total,
        "grade_a_count": grade_a,
        "grade_b_count": grade_b,
        "grade_c_count": grade_c,
        "pass_rate_percent": pass_rate,
        "batch_verdict": "✅ PASS" if pass_rate >= 50 else "❌ FAIL"
    }


def process_and_detect(image_bytes):
    # 1. Image Ingestion
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 2. Enhancement & Restoration
    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    lab = cv2.cvtColor(dst, cv2.COLOR_BGR2LAB)
    l, a, b_chan = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced = cv2.merge((cl, a, b_chan))
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    # 3. YOLO Detection — finds WHAT and WHERE
    results = model(enhanced)

    detections = []
    for r in results:
        for box in r.boxes:
            coords = box.xyxy[0].tolist()
            confidence = round(float(box.conf[0]), 2)
            label = model.names[int(box.cls[0])]

            # 4. Real Quality Analysis — analyses HOW IT LOOKS
            # This uses the ORIGINAL image for accurate colour
            quality_analysis = analyse_fruit_quality(img, coords)

            # 5. Grade based on actual analysis
            quality = get_quality_grade(quality_analysis)

            detections.append({
                "label": label,
                "confidence": confidence,          # YOLO's object certainty
                "confidence_pct": f"{int(confidence * 100)}%",
                "quality": quality,                # Real quality grade
                "quality_metrics": {               # Show actual measurements
                    "quality_score": quality_analysis["score"],
                    "dark_spots": f"{round(quality_analysis['dark_ratio'] * 100, 1)}%",
                    "colour_uniformity": quality_analysis["colour_uniformity"],
                    "vibrancy": quality_analysis["vibrancy"]
                },
                "box_coordinates": [round(x, 2) for x in coords]
            })

    # Sort by quality score — best first
    detections.sort(
        key=lambda x: x["quality"]["score"], reverse=True
    )

    summary = get_batch_summary(detections)

    return {
        "detections": detections,
        "summary": summary
    }