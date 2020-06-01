import numpy
import vpython


def rgb_to_vector(r: float, g: float, b: float):
	"""
	Make vpython.vector color from rgb values

	:param r: red value 0-255
	:param g: green value 0-255
	:param b: blue value 0-255
	:return: vpython.vector with color
	"""
	return vpython.vector(r/255, g/255, b/255)


# Math constants
PI = numpy.pi

# Define basic colors as constants
RED = vpython.color.red
LIME = vpython.color.green
BLUE = vpython.color.blue

BLACK = vpython.color.black
WHITE = vpython.color.white

CYAN = vpython.color.cyan
YELLOW = vpython.color.yellow
MAGENTA = vpython.color.magenta
ORANGE = vpython.color.orange

GAINSBORO = rgb_to_vector(220, 220, 220)
LIGHTGRAY = rgb_to_vector(211, 211, 211)
SILVER = rgb_to_vector(192, 192, 192)
DARKGRAY = rgb_to_vector(169, 169, 169)
GRAY = rgb_to_vector(128, 128, 128)
DIMGRAY = rgb_to_vector(105, 105, 105)

# 7 shades of gray
GRAY_SCALE = [GAINSBORO, LIGHTGRAY, SILVER, DARKGRAY, GRAY, DIMGRAY, BLACK]

GREEN = rgb_to_vector(0, 128, 0)
OLIVE = rgb_to_vector(128, 128, 0)
BROWN = rgb_to_vector(139, 69, 19)
NAVY = rgb_to_vector(0, 0, 128)
TEAL = rgb_to_vector(0, 128, 128)
PURPLE = rgb_to_vector(128, 0, 128)
MAROON = rgb_to_vector(128, 0, 0)
CRIMSON = rgb_to_vector(220, 20, 60)
TOMATO = rgb_to_vector(255, 99, 71)
GOLD = rgb_to_vector(255, 215, 0)
CHOCOLATE = rgb_to_vector(210, 105, 30)
PERU = rgb_to_vector(205, 133, 63)
INDIGO = rgb_to_vector(75, 0, 130)
KHAKI = rgb_to_vector(240, 230, 140)
SIENNA = rgb_to_vector(160, 82, 45)
