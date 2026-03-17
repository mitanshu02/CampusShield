# backend/analyzers/visual_detector.py

import os
import cv2
import numpy as np
import imagehash
from PIL import Image
from playwright.sync_api import sync_playwright
import base64

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)

# Template files and their brand names
TEMPLATES = {
    "college_real.png": "NIT Bhopal Fee Portal",
    "phonepe_real.png": "PhonePe",
}

SIMILARITY_THRESHOLD = 40 # % match to trigger spoofing alert


def capture_screenshot(url: str, output_path: str) -> bool:
    """Captures a fixed 1280x720 screenshot of the URL."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                viewport={"width": 1280, "height": 720}
            )
            # Hide dynamic popups before screenshot
            page.add_style_tag(content="""
                [id*="cookie"], [class*="cookie"],
                [id*="chat"],   [class*="chat"],
                [id*="popup"],  [class*="popup"],
                [id*="banner"], [class*="banner"] {
                    display: none !important;
                }
            """)
            page.goto(url, timeout=20000, wait_until="networkidle")
            page.screenshot(path=output_path, full_page=False)
            browser.close()
        return True
    except Exception as e:
        print(f"Screenshot failed for {url}: {e}")
        return False


def compute_similarity(img_path1: str, img_path2: str) -> int:
    """Returns perceptual hash similarity score 0-100."""
    try:
        hash1 = imagehash.phash(Image.open(img_path1))
        hash2 = imagehash.phash(Image.open(img_path2))
        max_distance = 64
        distance = hash1 - hash2
        similarity = round((1 - distance / max_distance) * 100)
        return max(0, min(100, similarity))
    except Exception as e:
        print(f"Similarity check failed: {e}")
        return 0


def generate_heatmap(
    suspect_path: str,
    template_path: str,
    output_path: str
) -> bool:
    """Generates red-zone difference heatmap between two images."""
    try:
        img1 = cv2.imread(suspect_path)
        img2 = cv2.imread(template_path)

        # Resize template to match suspect dimensions
        h, w = img1.shape[:2]
        img2 = cv2.resize(img2, (w, h))

        # Pixel-level absolute difference
        diff = cv2.absdiff(img1, img2)

        # Convert to grayscale and threshold
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

        # Create red overlay on original image
        red_overlay = np.zeros_like(img1)
        red_overlay[:, :, 2] = thresh  # red channel = diff mask

        # Blend original with red overlay
        result = cv2.addWeighted(img1, 0.6, red_overlay, 0.8, 0)
        cv2.imwrite(output_path, result)
        return True
    except Exception as e:
        print(f"Heatmap generation failed: {e}")
        return False


def image_to_base64(path: str) -> str:
    """Converts image file to base64 string for frontend display."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_visual(url: str) -> dict:
    """
    Full pipeline:
    1. Screenshot suspicious URL
    2. Compare against all templates
    3. If similarity >= threshold, generate heatmap
    4. Return all three images as base64
    """
    # Step 1 — capture screenshot of suspicious URL
    suspect_path = os.path.join(GENERATED_DIR, "suspect_screenshot.png")
    success = capture_screenshot(url, suspect_path)

    if not success:
        return {
            "visual_similarity": 0,
            "detected_brand":    None,
            "heatmap_url":       None,
            "risk":              None,
            "available":         False,
            "reason":            "Could not load page for visual analysis"
        }

    # Step 2 — compare against all templates
    best_score    = 0
    best_brand    = None
    best_template = None

    for filename, brand_name in TEMPLATES.items():
        template_path = os.path.join(TEMPLATES_DIR, filename)
        if not os.path.exists(template_path):
            continue
        score = compute_similarity(suspect_path, template_path)
        print(f"Similarity to {brand_name}: {score}%")
        if score > best_score:
            best_score    = score
            best_brand    = brand_name
            best_template = template_path

    # Step 3 — if below threshold, no spoofing detected
    if best_score < SIMILARITY_THRESHOLD or best_template is None:
        return {
            "visual_similarity": best_score,
            "detected_brand":    None,
            "heatmap_url":       None,
            "risk":              "low",
            "available":         True,
            "spoofing_detected": False,
            "suspect_image":     image_to_base64(suspect_path),
            "template_image":    None,
            "heatmap_image":     None,
            "reason": f"No significant visual similarity to known templates (best: {best_score}%)"
        }

    # Step 4 — generate heatmap
    heatmap_path = os.path.join(GENERATED_DIR, "heatmap.png")
    generate_heatmap(suspect_path, best_template, heatmap_path)

    return {
        "visual_similarity": best_score,
        "detected_brand":    best_brand,
        "heatmap_url":       "/generated/heatmap.png",
        "risk":              "high" if best_score >= 75 else "medium",
        "available":         True,
        "spoofing_detected": True,
        "suspect_image":     image_to_base64(suspect_path),
        "template_image":    image_to_base64(best_template),
        "heatmap_image":     image_to_base64(heatmap_path),
        "reason": f"Page is {best_score}% visually similar to {best_brand}"
    }