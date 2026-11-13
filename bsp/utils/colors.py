import colorsys
import random

def generate_hex_colors(n, saturation=0.7, value=0.95):
    """
    Generate n visually distinct hex colors suitable for charts.
    """
    if n <= 0:
        return []
    colors = []
    for i in range(n):
        hue = i / n
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        colors.append(hex_color)
    random.shuffle(colors)
    return colors

