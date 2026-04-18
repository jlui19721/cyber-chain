# @file app/render.py
# @brief Rendering function for displaying an AppState on an ST7789 LCD display.

from PIL import Image, ImageDraw, ImageFont
from app.state import AppState

# @brief Returns a PIL Image reflecting the current AppState to display
# @param state - The current AppState
# @param w - The width of the image (default: 240)
# @param h - The height of the image (default: 240)
# @return A PIL Image reflecting the current AppState to display
def render(state: AppState, w: int = 240, h: int = 240) -> Image.Image:
    img = Image.new("RGB", (w, h), color = (20, 20, 30))  # Black-ish
    draw = ImageDraw.Draw(img)

    # Using TTF because example code uses it & YOLO
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
        small = font

    draw.text(xy = (12, 12), text = "cyber-chain", fill=(200, 200, 255), font=font)
    draw.text(xy = (12, 50), text = f"counter: {state.counter}", fill=(255, 255, 255), font=font)
    draw.text(xy = (12, 70), text = f"last pressed: {state.last_label}", fill=(180, 180, 200), font=small)
    draw.text(xy = (12, 130), text = f"frame: {state.frame_idx}", fill=(120, 120, 140), font=small)

    return img