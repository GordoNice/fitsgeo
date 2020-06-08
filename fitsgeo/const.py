import numpy as np
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
PI = np.pi

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
GRAY = rgb_to_vector(169, 169, 169)
DARKGRAY = rgb_to_vector(128, 128, 128)
DIMGRAY = rgb_to_vector(105, 105, 105)

# 6 shades of gray
GRAY_SCALE = [GAINSBORO, LIGHTGRAY, SILVER, GRAY, DARKGRAY, DIMGRAY]

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
DARKRED = rgb_to_vector(139, 0, 0)
PINK = rgb_to_vector(219, 112, 147)
NAVAJOWHITE = rgb_to_vector(255, 222, 173)
DARKORANGE = rgb_to_vector(255, 140, 0)
SADDLEBROWN = rgb_to_vector(139, 69, 19)
DARKBROWN = rgb_to_vector(51, 25, 0)
DARKGOLDENROD = rgb_to_vector(184, 134, 11)
PASTELYELLOW = rgb_to_vector(255, 255, 153)
PASTELGREEN = rgb_to_vector(204, 255, 153)
YELLOWGREEN = rgb_to_vector(178, 255, 102)
DARKGREEN = rgb_to_vector(0, 102, 0)
MOSSGREEN = rgb_to_vector(0, 51, 0)
BLUEGREEN = rgb_to_vector(0, 255, 128)
PASTELCYAN = rgb_to_vector(153, 255, 255)
PASTELBLUE = rgb_to_vector(153, 204, 255)
CYANBLUE = rgb_to_vector(0, 102, 102)
DARKVIOLET = rgb_to_vector(148, 0, 211)
VIOLET = rgb_to_vector(238, 130, 238)
PASTELPURPLE = rgb_to_vector(238, 130, 238)
PASTELVIOLET = rgb_to_vector(204, 153, 255)
PASTELBROWN = rgb_to_vector(131, 105, 83)

# Dictionary with ANGEL colors in correspondence to VPython colors
ANGEL_COLORS = {
	"white": WHITE,
	"lightgray": LIGHTGRAY,
	"gray": GRAY,
	"darkgray": DARKGRAY,
	"matblack": DIMGRAY,
	"black": BLACK,
	"darkred": DARKRED,
	"red": RED,
	"pink": PINK,
	"pastelpink": NAVAJOWHITE,
	"orange": DARKORANGE,
	"brown": SADDLEBROWN,
	"darkbrown": DARKBROWN,
	"pastelbrown": PASTELBROWN,
	"orangeyellow": GOLD,
	"camel": OLIVE,
	"pastelyellow": PASTELYELLOW,
	"yellow": YELLOW,
	"pastelgreen": PASTELGREEN,
	"yellowgreen": YELLOWGREEN,
	"green": GREEN,
	"darkgreen": DARKGREEN,
	"mossgreen": MOSSGREEN,
	"bluegreen": BLUEGREEN,
	"pastelcyan": PASTELCYAN,
	"pastelblue": PASTELBLUE,
	"cyan": CYAN,
	"cyanblue": CYANBLUE,
	"blue": BLUE,
	"violet": DARKVIOLET,
	"purple": PURPLE,
	"magenta": MAGENTA,
	"winered": MAROON,
	"pastelmagenta": VIOLET,
	"pastelpurple": INDIGO,
	"pastelviolet": PASTELVIOLET
}

if __name__ == "__main__":
	print(
		"--- Welcome to FitsGeo! ---\n" +
		"This is a module for FitsGeo!\nImport FitsGeo to use.")
