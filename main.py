from PIL import Image, ImageDraw
from decimal import Decimal
import os, sys

C_BLACK = (0, 0, 0)
C_BROWN = (137, 64, 0)
C_RED = (237, 0, 0)
C_ORANGE = (244, 156, 0)
C_YELLOW = (247, 246, 0)
C_GREEN = (159, 195, 44)
C_BLUE = (11, 64, 158)
C_VIOLET = (134, 0, 194)
C_GREY = (88, 94, 97)
C_WHITE = (255, 255, 255)

C_GOLD = (189, 163, 42)
C_SILVER = (65, 70, 72)
C_NONE = (220, 195, 171)

T_1PCT = C_BROWN
T_2PCT = C_RED
T_5PCT = C_GOLD
T_10PCT = C_SILVER
T_20PCT = C_NONE

COLORS_INDEXED = [
        C_BLACK,
        C_BROWN,
        C_RED,
        C_ORANGE,
        C_YELLOW,
        C_GREEN,
        C_BLUE,
        C_VIOLET,
        C_GREY,
        C_WHITE
]


img_w = 500
img_h = 500

thin_height_ratio = 12.0 / 15.0
aspect_ratio = 48 / 20.0

res_w = img_w * (9 / 10.0)

res_h = res_w / aspect_ratio

thin_w = res_h / 2.0

leftmost = (img_w - res_w) / 2.0
rightmost = leftmost + res_w
topmost = (img_h - res_h) / 2.0
bottommost = topmost + res_h
thin_offset = (res_h - (thin_height_ratio * res_h)) / 2.0
lead_h = res_h / 6.0

def draw_resistor_body(draw):


    thin_rect = [ 
            (leftmost, round(float(topmost) + thin_offset)),
            (rightmost, round(float(bottommost) - thin_offset))
    ]

    left_rect = [
            (leftmost, topmost),
            (leftmost + thin_w, bottommost)
    ]

    right_rect = [
            (rightmost - thin_w, topmost),
            (rightmost, bottommost)
    ]

    lead_rect = [
            (0, (img_h - lead_h) / 2.0),
            (img_w, ((img_h - lead_h) / 2.0) + lead_h)
    ]

    resistor_color=(220, 195, 171)
    lead_color=(150, 150, 150)

    draw.rectangle(lead_rect, fill=lead_color)
    draw.rectangle(thin_rect, fill=resistor_color)
    draw.rectangle(left_rect, fill=resistor_color)
    draw.rectangle(right_rect, fill=resistor_color)

def draw_bands(draw, bands):
    bands_leftmost = leftmost + thin_w
    bands_rightmost = rightmost - thin_w
    bands_topmost = topmost + thin_offset
    bands_bottommost = bottommost - thin_offset
    bands_total_w = bands_rightmost - bands_leftmost

    band_w = bands_total_w / ((len(bands) - 1)  * 2.0)

    leftmost_band_x = bands_leftmost + band_w / 2

    for i in range(len(bands) - 1):
        band = bands[i]

        band_rect = [
                ((leftmost_band_x + (i * 2 * band_w)), bands_topmost),
                ((leftmost_band_x + (i * 2 * band_w) + band_w), bands_bottommost)
        ]

        draw.rectangle(band_rect, fill=band)

    tol_band_rect = [
            (bands_rightmost + (thin_w / 3.0), topmost),
            (bands_rightmost + (thin_w / 3.0 * 2.0), bottommost)
    ]

    draw.rectangle(tol_band_rect, bands[len(bands) - 1])

def draw_resistor(draw, value, tolerance):
    f = '{:.1E}'
    multiplier_offset = 1

    if tolerance == T_5PCT:
        f = '{:.1E}'
        multiplier_offset = 1
    elif tolerance == T_10PCT:
        f = '{:.1E}'
        multiplier_offset = 1
    elif tolerance == T_20PCT:
        f = '{:.1E}'
        multiplier_offset = 1
    elif tolerance == T_1PCT:
        f = '{:.2E}'
        multiplier_offset = 2
    elif tolerance == T_2PCT:
        f = '{:.2E}'
        multiplier_offset = 2
    else:
        raise "Invalid tolerance value, should be one of the T_xPCT constants"

    # TODO check if given formatting the number is accurately represented,
    # raise if not

    [val, exp] = f.format(value).split("E")

    print(val, exp)

    bands = []

    for ch in val.replace('.', ''):
        bands.append(COLORS_INDEXED[int(ch)])

    exp = int(exp) - multiplier_offset

    if exp < -2:
        raise "Invalid multiplier exponent, too small"

    if exp > 9:
        raise "Invalid multiplier exponent, too large"

    if exp >= 0:
        bands.append(COLORS_INDEXED[exp])
    elif exp == -1:
        bands.append(C_GOLD)
    elif exp == -2:
        bands.append(C_SILVER)

    bands.append(tolerance)

    draw_resistor_body(draw)
    draw_bands(draw, bands)

outfile = "test.png"
im = Image.new('RGBA', (img_w, img_h), (255, 255, 255, 0))
draw = ImageDraw.Draw(im)

draw_resistor(draw, Decimal("567"), T_1PCT)

im.save(outfile)

