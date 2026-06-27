"""
This script just creates a simple, light-colored certificate background image.
Run this once to create 'template.png' (already included, no need to re-run).
"""

from PIL import Image, ImageDraw, ImageFont

# Canvas size (looks like a landscape A4 page)
WIDTH, HEIGHT = 1600, 1100

# Light theme colors
BACKGROUND_COLOR = "#ffffff"   # white background
BORDER_COLOR = "#a8d8ff"       # light blue border
TEXT_COLOR = "#333333"         # dark grey text (easy to read on light bg)
ACCENT_COLOR = "#5fa8d3"       # soft blue accent

img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND_COLOR)
draw = ImageDraw.Draw(img)

# Simple border
draw.rectangle([20, 20, WIDTH - 20, HEIGHT - 20], outline=BORDER_COLOR, width=10)

# Fonts
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
title_font = ImageFont.truetype(FONT_PATH, 65)
sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)

def draw_centered_text(y, text, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (WIDTH - text_width) / 2
    draw.text((x, y), text, font=font, fill=color)

draw_centered_text(100, "CERTIFICATE OF COMPLETION", title_font, ACCENT_COLOR)
draw_centered_text(220, "This certificate is presented to", sub_font, TEXT_COLOR)

# Line where the name will appear later
draw.line([(500, 480), (1100, 480)], fill=ACCENT_COLOR, width=2)

img.save("template.png")
print("template.png created successfully.")
