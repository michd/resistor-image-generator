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

T_FIFTIETH_PCT = C_YELLOW
T_TWENTIETH_PCT = C_ORANGE
T_TENTH_PCT = C_VIOLET
T_QUARTER_PCT = C_BLUE
T_HALF_PCT = C_GREEN
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

TOLERANCES = {
        0.02: T_FIFTIETH_PCT,
        0.05: T_TWENTIETH_PCT,
        0.1: T_TENTH_PCT,
        0.25: T_QUARTER_PCT,
        0.5: T_HALF_PCT,
        1.0: T_1PCT,
        2.0: T_2PCT,
        5.0: T_5PCT,
        10.0: T_10PCT,
        20.0: T_20PCT
}

PREFERRED_NUMBERS = {
    "E3": {
        "tolerance": 40.0,
        "numbers": [ 1.0, 2.2, 4.7 ]
    },
    "E6": {
        "tolerance": 20.0,
        "numbers": [ 1.0, 1.5, 2.2, 3.3, 4.7, 6.8 ]
    },
    "E12": {
        "tolerance": 10.0,
        "numbers": [ 1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2 ]
    },
    "E24": {
        "tolerance": 5.0,
        "numbers": [
            1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7,
            5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1
        ]
    },
    "E48": {
        "tolerance": 2.0,
        "numbers": [
            1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69, 1.78, 1.87,
            1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65,
            3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49, 6.81, 7.15,
            7.50, 7.87, 8.25, 8.66, 9.09, 9.53
        ]
    },
    "E96": {
        "tolerance": 1.0,
        "numbers": [
            1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37,
            1.40, 1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91,
            1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 2.61, 2.67,
            2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74,
            3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23,
            5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32,
            7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66, 8.87, 9.09, 9.31, 9.53, 9.76
        ]
    },
    "E192": {
        "tolerance": 0.5,
        "numbers": [
            1.00, 1.01, 1.02, 1.04, 1.05, 1.06, 1.07, 1.09, 1.10, 1.11, 1.13, 1.14, 1.15, 1.17,
            1.18, 1.20, 1.21, 1.23, 1.24, 1.26, 1.27, 1.29, 1.30, 1.32, 1.33, 1.35, 1.37, 1.38,
            1.40, 1.42, 1.43, 1.45, 1.47, 1.49, 1.50, 1.52, 1.54, 1.56, 1.58, 1.60, 1.62, 1.64,
            1.65, 1.67, 1.69, 1.72, 1.74, 1.76, 1.78, 1.80, 1.82, 1.84, 1.87, 1.89, 1.91, 1.93,
            1.96, 1.98, 2.00, 2.03, 2.05, 2.08, 2.10, 2.13, 2.15, 2.18, 2.21, 2.23, 2.26, 2.29,
            2.32, 2.34, 2.37, 2.40, 2.43, 2.46, 2.49, 2.52, 2.55, 2.58, 2.61, 2.64, 2.67, 2.71,
            2.74, 2.77, 2.80, 2.84, 2.87, 2.91, 2.94, 2.98, 3.01, 3.05, 3.09, 3.12, 3.16, 3.20,
            3.24, 3.28, 3.32, 3.36, 3.40, 3.44, 3.48, 3.52, 3.57, 3.61, 3.65, 3.70, 3.74, 3.79,
            3.83, 3.88, 3.92, 3.97, 4.02, 4.07, 4.12, 4.17, 4.22, 4.27, 4.32, 4.37, 4.42, 4.48,
            4.53, 4.59, 4.64, 4.70, 4.75, 4.81, 4.87, 4.93, 4.99, 5.05, 5.11, 5.17, 5.23, 5.30,
            5.36, 5.42, 5.49, 5.56, 5.62, 5.69, 5.76, 5.83, 5.90, 5.97, 6.04, 6.12, 6.19, 6.26,
            6.34, 6.42, 6.49, 6.57, 6.65, 6.73, 6.81, 6.90, 6.98, 7.06, 7.15, 7.23, 7.32, 7.41,
            7.50, 7.59, 7.68, 7.77, 7.87, 7.96, 8.06, 8.16, 8.25, 8.35, 8.45, 8.56, 8.66, 8.76,
            8.87, 8.98, 9.09, 9.20, 9.31, 9.42, 9.53, 9.65, 9.76, 9.88
        ]
    }
}

EXPONENTS = [ 0, 1, 2, 3, 4, 5, 6 ]

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

    if tolerance in [ T_5PCT, T_10PCT, T_20PCT ]:
        f = '{:.1E}'
        multiplier_offset = 1
    elif tolerance in [ 
            T_FIFTIETH_PCT, T_TWENTIETH_PCT, T_TENTH_PCT, T_QUARTER_PCT, T_HALF_PCT, T_1PCT, T_2PCT 
            ]:
        f = '{:.2E}'
        multiplier_offset = 2
    else:
        raise "Invalid tolerance value, should be one of the T_xPCT constants"

    # TODO check if given formatting the number is accurately represented,
    # raise if not

    [val, exp] = f.format(value).split("E")

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

# Returns a pretty print conventional value for a given resistance value in
# ohms; for example: 20 ohms = 20R, 390000 ohms = 390k, 6800 = 6.8k
def get_value_name(value):
    suffix = "R"
    divided_value = value / Decimal("1.0")

    if value >= 1_000_000:
        suffix = "M"
        divided_value = value / Decimal("1000000.0")
    elif value >= 1_000:
        suffix = "k"
        divided_value = value / Decimal("1000.0")

    if divided_value == round(divided_value):
        divided_value = round(divided_value)

    return "{:}{:}".format(divided_value, suffix)

def get_nearest_tolerance(start_tolerance, max_tolerance):
    nearest = None

    for candidate in TOLERANCES.keys():
        if candidate > max_tolerance:
            return nearest

        if nearest is None or abs(start_tolerance - candidate) < nearest:
            nearest = candidate

    return nearest

def get_series_values(series_key, tolerance = None):
    values = []

    if (series_key not in PREFERRED_NUMBERS):
        raise Exception("Unknown series " + series_key + ". Available: " + \
                ", ".join(PREFERRED_NUMBERS.keys()))

    series = PREFERRED_NUMBERS[series_key]

    if tolerance != None and tolerance > series["tolerance"]:
        raise Exception("Tolerance " + str(tolerance) + "% too loose for series " + series_key+ ", must be " + \
                "at most " + str(series["tolerance"]) + "%")
    elif tolerance == None:
        tolerance = series["tolerance"]
    else:
        tolerance = get_nearest_tolerance(tolerance, max_tolerance=series["tolerance"])

    for exp in EXPONENTS:
        for num in series["numbers"]:
            values.append(
                    Decimal(str(num)) * (10 ** exp))

    values.append(Decimal(str(series["numbers"][0])) * (10 ** (EXPONENTS[-1] + 1)))

    return (values, tolerance)

def get_resistor_file_path(series, value, tolerance):
    label = get_value_name(value)
    tol = str(tolerance)

    if (tolerance == round(tolerance)):
        tol = str(round(tolerance))

    return os.path.join(series, "{:}_{:}pct.png".format(label, tol))

def generate_series_images(series_key, tolerance = None):
    (values, tolerance) = get_series_values(series_key, tolerance)

    try:
        os.mkdir(series_key)
    except FileExistsError:
        pass

    for val in values:
        r_filepath = get_resistor_file_path(series_key, val, tolerance)
        print("Generating {:}".format(r_filepath))
        im = Image.new('RGBA', (img_w, img_h), (255, 255, 255, 0))
        draw = ImageDraw.Draw(im)
        draw_resistor(draw, val, TOLERANCES[tolerance])
        im.save(r_filepath)

generate_series_images("E192")
