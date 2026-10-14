import cv2
import numpy as np
import os

img_path = r'C:\Users\D\.gemini\antigravity-ide\brain\ea0d36e8-b09a-44dc-83f2-278a84a8cbd6\.user_uploaded\media_1791984555672.jpg'
orig = cv2.imread(img_path)
h, w, _ = orig.shape
gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)

os.makedirs('svg2', exist_ok=True)

# 1. Exact Logo Bounds:
# Icon: x=343..424, y=136..228
# Wordmark: x=444..785, y=136..228
# Total logo bounds: x=343..785 (width 442), y=136..228 (height 92)

# Binary mask for the dark logo pixels (< 120) in the logo region
logo_region_mask = np.zeros_like(gray)
logo_region_mask[130:235, 335:795] = (gray[130:235, 335:795] < 120).astype(np.uint8) * 255

contours, hierarchy = cv2.findContours(logo_region_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)

# Sort contours by hierarchy to handle holes properly
# For full-image SVG (coordinates in [0..923, 0..275]):
full_logo_d = ""
for c in contours:
    approx = cv2.approxPolyDP(c, 0.35, True)
    pts = approx.reshape(-1, 2)
    full_logo_d += f"M {pts[0][0]},{pts[0][1]} "
    for pt in pts[1:]:
        full_logo_d += f"L {pt[0]},{pt[1]} "
    full_logo_d += "Z "

# For cropped logo SVG (offset by x=-343, y=-136):
# viewBox = "0 0 446 94"
cropped_logo_d = ""
for c in contours:
    approx = cv2.approxPolyDP(c, 0.35, True)
    pts = approx.reshape(-1, 2)
    cropped_logo_d += f"M {pts[0][0] - 343},{pts[0][1] - 136} "
    for pt in pts[1:]:
        cropped_logo_d += f"L {pt[0] - 343},{pt[1] - 136} "
    cropped_logo_d += "Z "

# For standalone icon SVG (offset by x=-343, y=-136, bbox x <= 425):
icon_mask = np.zeros_like(gray)
icon_mask[130:235, 335:430] = (gray[130:235, 335:430] < 120).astype(np.uint8) * 255
icon_contours, _ = cv2.findContours(icon_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
cropped_icon_d = ""
for c in icon_contours:
    approx = cv2.approxPolyDP(c, 0.35, True)
    pts = approx.reshape(-1, 2)
    cropped_icon_d += f"M {pts[0][0] - 343},{pts[0][1] - 136} "
    for pt in pts[1:]:
        cropped_icon_d += f"L {pt[0] - 343},{pt[1] - 136} "
    cropped_icon_d += "Z "

# -------------------------------------------------------------
# SVG 1: full-image.svg (Complete original image in vector SVG)
# Dimensions: 923 x 275
# Colors sampled directly from original image:
# - Outer Canvas: #D3DAD2
# - Window Header Bar: #C3C6BB
# - Window Border Lines & Dots: #88897D
# - Logo: #110C06
# -------------------------------------------------------------
svg_full_image = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 923 275" width="923" height="275" aria-label="Original Mockup Image Vector">
  <!-- Outer Canvas Background -->
  <rect width="923" height="275" fill="#D3DAD2"/>
  
  <!-- Browser Window Container with Rounded Top-Left Corner -->
  <path d="M 108,275 L 108,60 A 16 16 0 0 1 124,44 L 923,44 L 923,275 Z" fill="#D3D8D1" stroke="#88897D" stroke-width="1.5"/>
  
  <!-- Window Top Bar Header Area -->
  <path d="M 108,104 L 108,60 A 16 16 0 0 1 124,44 L 923,44 L 923,104 Z" fill="#C3C6BB" stroke="#88897D" stroke-width="1.5"/>
  
  <!-- Window Control Dots (Three Circles on Top Left) -->
  <circle cx="146" cy="74" r="8.5" fill="none" stroke="#88897D" stroke-width="1.8"/>
  <circle cx="182" cy="74" r="8.5" fill="none" stroke="#88897D" stroke-width="1.8"/>
  <circle cx="220" cy="74" r="8.5" fill="none" stroke="#88897D" stroke-width="1.8"/>
  
  <!-- Bottom Panels / Columns Outlines -->
  <rect x="343" y="250" width="150" height="25" rx="4" fill="none" stroke="#88897D" stroke-width="1.5"/>
  <rect x="500" y="250" width="160" height="25" rx="4" fill="none" stroke="#88897D" stroke-width="1.5"/>
  <rect x="668" y="250" width="160" height="25" rx="4" fill="none" stroke="#88897D" stroke-width="1.5"/>
  
  <!-- Exact Extracted blackeyeTech Logo -->
  <path d="{full_logo_d}" fill="#110C06" fill-rule="evenodd"/>
</svg>'''

# -------------------------------------------------------------
# SVG 2: extracted-logo.svg (Exact extracted logo, transparent background)
# -------------------------------------------------------------
svg_extracted_logo = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 446 94" width="446" height="94" fill="none" aria-label="blackeyeTech Extracted Logo">
  <!-- Exact vector contours extracted directly from original image -->
  <path d="{cropped_logo_d}" fill="#110C06" fill-rule="evenodd"/>
</svg>'''

# -------------------------------------------------------------
# SVG 3: extracted-logo-with-bg.svg (Logo with original canvas background)
# -------------------------------------------------------------
svg_extracted_logo_with_bg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 486 134" width="486" height="134" aria-label="blackeyeTech Extracted Logo with Background">
  <rect width="486" height="134" rx="8" fill="#D3DAD2"/>
  <g transform="translate(20, 20)">
    <path d="{cropped_logo_d}" fill="#110C06" fill-rule="evenodd"/>
  </g>
</svg>'''

# -------------------------------------------------------------
# SVG 4: extracted-icon.svg (Standalone icon, transparent background)
# -------------------------------------------------------------
svg_extracted_icon = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 82 94" width="82" height="94" fill="none" aria-label="blackeyeTech Extracted Icon">
  <!-- Exact 'be' icon vector extracted directly from original image -->
  <path d="{cropped_icon_d}" fill="#110C06" fill-rule="evenodd"/>
</svg>'''

# -------------------------------------------------------------
# SVG 5: extracted-icon-with-bg.svg (Icon with original canvas background)
# -------------------------------------------------------------
svg_extracted_icon_with_bg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122 134" width="122" height="134" aria-label="blackeyeTech Extracted Icon with Background">
  <rect width="122" height="134" rx="8" fill="#D3DAD2"/>
  <g transform="translate(20, 20)">
    <path d="{cropped_icon_d}" fill="#110C06" fill-rule="evenodd"/>
  </g>
</svg>'''

# -------------------------------------------------------------
# SVG 6: browser-window-header-logo.svg (Window Header with 3 dots and Logo)
# -------------------------------------------------------------
svg_window_header = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 120" width="760" height="120" aria-label="Browser Header Logo">
  <rect width="760" height="120" rx="10" fill="#D3DAD2"/>
  <rect x="0" y="0" width="760" height="48" rx="10" fill="#C3C6BB" stroke="#88897D" stroke-width="1.5"/>
  <circle cx="28" cy="24" r="6.5" fill="none" stroke="#88897D" stroke-width="1.6"/>
  <circle cx="48" cy="24" r="6.5" fill="none" stroke="#88897D" stroke-width="1.6"/>
  <circle cx="68" cy="24" r="6.5" fill="none" stroke="#88897D" stroke-width="1.6"/>
  <g transform="translate(160, 56) scale(0.68)">
    <path d="{cropped_logo_d}" fill="#110C06" fill-rule="evenodd"/>
  </g>
</svg>'''

# Write files into svg2/
files = {
    'svg2/full-image.svg': svg_full_image,
    'svg2/extracted-logo.svg': svg_extracted_logo,
    'svg2/extracted-logo-with-bg.svg': svg_extracted_logo_with_bg,
    'svg2/extracted-icon.svg': svg_extracted_icon,
    'svg2/extracted-icon-with-bg.svg': svg_extracted_icon_with_bg,
    'svg2/browser-window-header-logo.svg': svg_window_header,
    'svg2/traced-logo-original.svg': svg_extracted_logo,
    'svg2/traced-icon-original.svg': svg_extracted_icon,
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Successfully created {path}')

print('All authentic image-extracted SVGs created in svg2/!')
