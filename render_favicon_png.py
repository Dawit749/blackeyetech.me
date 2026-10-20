"""Render apple-touch-icon.png (180x180) from the favicon.svg geometry.

The 'be' monogram path consists of lines and circular arcs only, so we flatten
the arcs into polygon points (SVG spec endpoint->center parameterization),
supersample 8x for antialiasing, then downscale with Pillow.
Full-bleed white square (opaque) per apple-touch-icon convention; iOS masks
the corners itself.
"""
import math
from PIL import Image, ImageDraw

INK = (0, 0, 0, 255)           # black mark
CANVAS = (255, 255, 255, 255)  # white background
SS = 8                          # supersample factor
SIZE = 180
S = SIZE * SS
VB = 93.0                       # viewBox 0 0 93 93
scale = S / VB

def arc_points(p1, p2, r, large, sweep, steps=96):
    """Flatten a circular SVG arc into points (endpoint parameterization)."""
    x1, y1 = p1
    x2, y2 = p2
    x1p, y1p = (x1 - x2) / 2, (y1 - y2) / 2
    q = x1p**2 + y1p**2
    if q == 0:
        return [p2]
    if q > r * r:  # scale radius up if endpoints don't fit
        r = math.sqrt(q)
    sign = 1.0 if large != sweep else -1.0
    coef = sign * math.sqrt(max((r * r - q) / q, 0.0))
    cx = coef * y1p + (x1 + x2) / 2
    cy = -coef * x1p + (y1 + y2) / 2
    a1 = math.atan2(y1 - cy, x1 - cx)
    a2 = math.atan2(y2 - cy, x2 - cx)
    dtheta = a2 - a1
    if sweep == 0 and dtheta > 0:
        dtheta -= 2 * math.pi
    if sweep == 1 and dtheta < 0:
        dtheta += 2 * math.pi
    return [(cx + r * math.cos(a1 + dtheta * i / steps),
             cy + r * math.sin(a1 + dtheta * i / steps))
            for i in range(1, steps + 1)]

# Path from svg/blackeyetech-icon.svg (the master geometric monogram),
# scaled 0.9 and centered to match favicon.svg's translate(9.6,4.65) scale(0.9).
SCALE_F, DX, DY = 0.9, 9.6, 4.65
pts = [(0.0, 0.0)]
pts.append((12.5, 0.0))
pts.append((12.5, 22.53))
pts += arc_points(pts[-1], (81.63, 57.5), 41, 0, 1)
pts.append((56.02, 57.5))
pts += arc_points(pts[-1], (55.83, 46.0), 16, 1, 1)
pts.append((68.86, 46.0))
pts += arc_points(pts[-1], (65.54, 66.5), 28.5, 1, 0)
pts.append((79.35, 66.5))
pts += arc_points(pts[-1], (0.0, 52.0), 41, 0, 1)
pts.append((0.0, 0.0))

px = [((x * SCALE_F + DX) * scale, (y * SCALE_F + DY) * scale) for x, y in pts]

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rectangle([0, 0, S - 1, S - 1], fill=CANVAS)
d.polygon(px, fill=INK)
img = img.resize((SIZE, SIZE), Image.LANCZOS)
img.save("apple-touch-icon.png")
print("apple-touch-icon.png written:", img.size)
