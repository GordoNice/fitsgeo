import itertools
from numpy import linalg as la
from numpy import format_float_positional, abs, power, sqrt, sum, random, \
	amin, inner, cross
from scipy.special import ellipe, ellipk
from vpython import canvas, arrow, vertex, vector

from .const import *
from .material import Material, MAT_WATER

# Counter for objects, every new object will have n+1 surface number
surface_counter = itertools.count(1)

created_surfaces = []  # All objects after initialisation go here


def list_all_surfaces():
	"""
	List with all implemented surfaces for now

	"""
	text = """\nList with all implemented surfaces

P (PX, PY, PZ) - multi-purpose planes (as well as vertical with x, y, z axes);
BOX - optional box (all angles are 90deg);
RPP - rectangular solid (each surface is vertical with x, y, z axes);
SPH - general sphere;
RCC - cylinder;
TRC - cone (may be unstable in visualization, use truncated=False flag);
T (TX, TY, TZ) - general torus (rotational x, y, z axes);
REC - Right elliptical cylinder (careful, because A and B vectors have only 
magnitude meaning for visualization, direction of vectors is meaningless);
WED - wedge surface, note that only right triangle can be used as bottom;
...
Look at README.md for more information\n"""
	print(text)


def create_scene(
		axes=True, width=1200, height=800, resizable=True,
		ax_length=2.0, ax_opacity=0.2, background=GRAY_SCALE[1]):
	"""
	Create vpython.canvas with some default settings (axes etc)

		*zoom:* mouse wheel

		*rotate:* right mouse button (ctrl+left mouse button)

		*pan:* shift+left mouse button

	:param axes: add axes to scene if True
	:param width: set width for visualization window in pixels
	:param height: set height for visualization window in pixels
	:param resizable: if True makes window resizable
	:param ax_length: axis length, better set as maximum size of whole geometry
	:param ax_opacity: set axis opacity, where 1.0 is fully visible
	:param background: set background color for scene
	:return: vpython.canvas object
	"""
	scene = canvas(
		width=width, height=height,
		resizable=resizable, background=background)

	if axes:  # Create axis
		shaft_width = 0.003 * ax_length

		ax_x = arrow(axis=vector(ax_length, 0, 0), color=RED)
		ax_y = arrow(axis=vector(0, ax_length, 0), color=GREEN)
		ax_z = arrow(axis=vector(0, 0, ax_length), color=BLUE)

		for ax in [ax_x, ax_y, ax_z]:
			ax.opacity = ax_opacity
			ax.shaftwidth = shaft_width
			ax.headwidth = 3 * shaft_width
			ax.headlength = 4 * shaft_width

		vpython.label(
			pos=ax_x.axis, text="X", font="monospace", box=False, opacity=0.2,
			xoffset=0, yoffset=0, space=0, height=14, border=6)

		vpython.label(
			pos=ax_y.axis, text="Y", font="monospace", box=False, opacity=0.2,
			xoffset=0, yoffset=0, space=0, height=14, border=6)

		vpython.label(
			pos=ax_z.axis, text="Z", font="monospace", box=False, opacity=0.2,
			xoffset=0, yoffset=0, space=0, height=14, border=6)

	return scene


def notation(f: float):
	"""
	Function returns nice looking string with number for surface labels

	:param f: input float
	:return: string
	"""
	return format_float_positional(f, precision=3, trim="-")


class Surface:  # superclass with common properties/methods for all surfaces

	def __init__(
			self, name="Surface", trn="", material=MAT_WATER):
		"""
		Define surface

		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param material: material associated with surface
		"""
		self.name = name
		self.trn = trn
		self.material = material

		self.sn = next(surface_counter)
		self.color = ANGEL_COLORS[self.material.color]

		self.opacity = 1.0

	# Overload operators
	# Positive sign
	def __pos__(self):
		return str(self.sn) + " "

	# Negative sign
	def __neg__(self):
		return str(-self.sn) + " "

	# str operator returns sn
	def __str__(self):
		return f"{self.sn}"

	@property
	def name(self):
		"""
		Get surface object name

		:return: string name
		"""
		return self.__name

	@name.setter
	def name(self, name: str):
		"""
		Set surface object name

		:param name: surface object name
		"""
		self.__name = name

	@property
	def sn(self):
		"""
		Get surface object number

		:return: int sn
		"""
		return self.__sn

	@sn.setter
	def sn(self, sn: int):
		"""
		Set surface object number

		:param sn: sn [any number from 1 to 999 999]
		"""
		self.__sn = sn

	@property
	def trn(self):
		"""
		Get transform number n in "trn"

		:return: string 'n' in "trn"
		"""
		return self.__trn

	@trn.setter
	def trn(self, trn: str):
		"""
		Set transform number for object

		:param trn: 'n' in "trn"
		"""
		self.__trn = trn

	@property
	def material(self):
		"""
		Get surface material

		:return: Material object
		"""
		return self.__material

	@material.setter
	def material(self, material: Material):
		"""
		Set surface material

		:param material: material
		"""
		self.__material = material

	@property
	def color(self):
		"""
		Get surface color

		:return: color of surface
		"""
		return self.__color

	@color.setter
	def color(self, color: vector):
		"""
		Set surface color

		:param color: color
		"""
		self.__color = color

	@property
	def opacity(self):
		"""
		Get surface opacity

		:return: opacity of surface
		"""
		return self.__opacity

	@opacity.setter
	def opacity(self, opacity: float):
		"""
		Set surface opacity

		:param opacity: opacity
		"""
		if self.material.gas:
			self.__opacity = 0.2  # Gas should be transparent
		else:
			self.__opacity = opacity

		if self.material.matn == 0:  # For vacuum even more transparent
			self.__opacity = 0.02


class P(Surface):
	symbol_p = "P"
	symbol_px, symbol_py, symbol_pz = "PX", "PY", "PZ"

	def __init__(
			self,
			a=1.0, b=-1.0, c=-1.0, d=4.0, name="P", trn="", vert=""):
		"""
		Define plane surfaces: P (general), PX (vertical to x), PY (vertical to y),
		PZ (vertical to z)

		Equation P: Ax + By + Cz − D = 0

		Equation PX: x = D

		Equation PY: y = D

		Equation PZ: z = D

		:param a: A
		:param b: B
		:param c: C
		:param d: D
		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param vert: axis to which plane is vertical
		"""
		self.a = a
		self.b = b
		self.c = c
		self.d = d

		Surface.__init__(self, name, trn)
		self.vert = vert
		created_surfaces.append(self)

	@property
	def a(self):
		"""
		Get parameter A

		:return: float parameter A
		"""
		return self.__a

	@a.setter
	def a(self, a: float):
		"""
		Set parameter A

		:param a: parameter A
		"""
		self.__a = a

	@property
	def b(self):
		"""
		Get parameter B

		:return: float parameter B
		"""
		return self.__b

	@b.setter
	def b(self, b: float):
		"""
		Set parameter B

		:param b: parameter B
		"""
		self.__b = b

	@property
	def c(self):
		"""
		Get parameter C

		:return: float parameter C
		"""
		return self.__c

	@c.setter
	def c(self, c: float):
		"""
		Set parameter C

		:param c: parameter C
		"""
		self.__c = c

	@property
	def d(self):
		"""
		Get parameter D

		:return: float D parameter
		"""
		return self.__d

	@d.setter
	def d(self, d: float):
		"""
		Set parameter D

		:param d: D parameter
		"""
		self.__d = d

	@property
	def vert(self):
		"""
		Get axis to which plane is vertical

		:return: string axis ("", "x", "y" or "z")
		"""
		return self.__vert

	@vert.setter
	def vert(self, vert: str):
		"""
		Set vertical axis

		:param vert: string with axis ("", "x" "y" or "z")
		"""
		self.__vert = vert

	@property
	def equation_p(self):
		"""
		Get equation of multi-purpose plane

		:return: string with multi-purpose plane equation
		"""
		return f"{self.a}x + {self.b}y + {self.c}z − {self.d} = 0"

	@property
	def equation_pxyz(self):
		"""
		Get equation for vertical plane

		:return: string with vertical plane equation
		"""
		return f"{self.vert} = {self.d}"

	def print_properties(self):
		prefix = f"P '{self.name}' sn={self.sn}"

		print(f"{prefix} A parameter:", self.a)
		print(f"{prefix} B parameter:", self.b)
		print(f"{prefix} C parameter:", self.c)
		print(f"{prefix} D parameter:", self.d)
		print(f"{prefix} trn:", self.trn)
		print(f"{prefix} axis to which plane is vertical:", self.vert)

	def phits_print(self):
		"""
		Prints PHITS surface definition

		:return: string with PHITS surface definition
		"""
		symbol = self.symbol_p
		equation = self.equation_p
		a, b, c = self.a, self.b, self.c

		if self.vert != "":
			a, b, c = "", "", ""
			equation = self.equation_pxyz
			if self.vert == "x":
				symbol = self.symbol_px
			elif self.vert == "y":
				symbol = self.symbol_py
			elif self.vert == "z":
				symbol = self.symbol_pz

		txt = f"    {self.sn} {self.trn}  {symbol}  {a} {b}" + \
			f" {c}  {self.d} $ name: '{self.name}' (Plane) {equation}"

		if self.trn != "":
			txt += f" with tr{self.trn}"
		return txt

	def draw(self, size: float = 10, opacity=0.2, label=True):
		"""
		Draw surface using vpython

		:param size: Plane size (half of total size)
		:param opacity: Set opacity, where 1.0 is fully visible
		:param label: If True create label for object
		:return: vpython.quad and vpython.label objects
		"""
		symbol = self.symbol_p

		if self.a == 1 and self.b == 0 and self.c == 0:
			self.vert = "x"
		elif self.b == 1 and self.a == 0 and self.c == 0:
			self.vert = "y"
		elif self.c == 1 and self.a == 0 and self.b == 0:
			self.vert = "z"

		equation = self.equation_pxyz
		if self.vert == "x":
			symbol = self.symbol_px
			x = [self.d, self.d, self.d, self.d]
			y = [-size, size, size, -size]
			z = [-size, -size, size, size]
			color1, color2, color3, color4 = RED, RED, RED, RED

		elif self.vert == "y":
			symbol = self.symbol_py
			x = [-size, size, size, -size]
			y = [self.d, self.d, self.d, self.d]
			z = [-size, -size, size, size]
			color1, color2, color3, color4 = GREEN, GREEN, GREEN, GREEN

		elif self.vert == "z":
			symbol = self.symbol_pz
			x = [-size, size, size, -size]
			y = [-size, -size, size, size]
			z = [self.d, self.d, self.d, self.d]
			color1, color2, color3, color4 = BLUE, BLUE, BLUE, BLUE

		else:  # TODO: improve this - plane better be square every time!
			equation = self.equation_p
			x = [-size, size, size, -size]
			y = [-size, -size, size, size]

			z = []
			for i in range(4):
				z.append((-self.a * x[i] - self.b * y[i] + self.d)/self.c)

			color1, color2, color3, color4 = CYAN, MAGENTA, YELLOW, WHITE

		# Plane made with 4 vertexes
		dot1 = vertex(
			pos=vector(x[0], y[0], z[0]),
			color=color1, opacity=opacity)
		dot2 = vertex(
			pos=vector(x[1], y[1], z[1]),
			color=color2, opacity=opacity)
		dot3 = vertex(
			pos=vector(x[2], y[2], z[2]),
			color=color3, opacity=opacity)
		dot4 = vertex(
			pos=vector(x[3], y[3], z[3]),
			color=color4, opacity=opacity)
		plane = vpython.quad(vs=[dot1, dot2, dot3, dot4])

		lbl = None
		if label:
			txt = f"{symbol} '{self.name}' sn: {self.sn}\n{equation}"
			lbl = vpython.label(
				pos=dot2.pos, text=txt, font="monospace", box=False, border=6,
				opacity=0.2, xoffset=0, yoffset=0, space=0,	height=12)
		return plane, lbl


class SPH(Surface):

	symbol = "SPH"

	def __init__(
			self, xyz0: list = None, r=1.0,
			name="SPH", trn="", material=MAT_WATER):
		"""
		Define SPH (sphere) surface

		:param xyz0: center coordinate [x0, y0, z0]
		:param r: radius
		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param material: material associated with surface
		"""
		# Default value
		if xyz0 is None:
			xyz0 = [0.0, 0.0, 0.0]

		self.xyz0 = xyz0
		self.r = r

		Surface.__init__(self, name, trn, material)
		created_surfaces.append(self)

	@property
	def xyz0(self):
		"""
		Get list with center coordinate

		:return: list [x0, y0, z0]
		"""
		return self.__xyz0

	@xyz0.setter
	def xyz0(self, xyz0: list):
		"""
		Set list with center coordinate

		:param xyz0: list [x0, y0, z0]
		"""
		self.__xyz0 = xyz0

	@property
	def x0(self):
		"""
		Get x component of center coordinate

		:return: float x0
		"""
		return self.__xyz0[0]

	@x0.setter
	def x0(self, x0: float):
		"""
		Set x component of center coordinate

		:param x0: float x0
		"""
		self.__xyz0[0] = x0

	@property
	def y0(self):
		"""
		Get y component of center coordinate

		:return: float y0
		"""
		return self.__xyz0[1]

	@y0.setter
	def y0(self, y0: float):
		"""
		Set y component of center coordinate

		:param y0: float y0
		"""
		self.__xyz0[1] = y0

	@property
	def z0(self):
		"""
		Get z component of center coordinate

		:return: float z0
		"""
		return self.__xyz0[2]

	@z0.setter
	def z0(self, z0: float):
		"""
		Set z component of center coordinate

		:param z0: float z0
		"""
		self.__xyz0[2] = z0

	@property
	def r(self):
		"""
		Get sphere radius

		:return: float radius
		"""
		return self.__r

	@r.setter
	def r(self, r: float):
		"""
		Set sphere radius

		:param r: radius
		"""
		self.__r = r

	@property
	def diameter(self):
		"""
		Get sphere diameter

		:return: float diameter
		"""
		return self.r*2

	@diameter.setter
	def diameter(self, diameter: float):
		"""
		Set sphere diameter (change radius to make specified diameter)

		:param diameter: diameter
		"""
		self.r = diameter/2

	@property
	def volume(self):
		"""
		Get volume as 4/3 * pi * R^3

		:return: float volume
		"""
		return (4/3) * PI * power(self.r, 3)

	@volume.setter
	def volume(self, volume: float):
		"""
		Set sphere volume (change radius to make specified volume)

		:param volume: float volume
		"""
		self.r = power((3 * volume)/(4 * PI), 1/3)

	@property
	def surface_area(self):
		"""
		Get full surface area as 4 * pi * R^2

		:return: float full surface area
		"""
		return 4 * PI * power(self.r, 2)

	@surface_area.setter
	def surface_area(self, area: float):
		"""
		Set radius according to full surface area as r = sqrt(area/(4*pi))

		:param area: float area
		"""
		self.r = sqrt(area/(4*PI))

	@property
	def cross_section(self):
		"""
		Get the cross section area of sphere as pi * R^2

		:return: float cross section area
		"""
		return PI * power(self.r, 2)

	@cross_section.setter
	def cross_section(self, s: float):
		"""
		Set cross section area of sphere (change radius to make specified area)

		:param s: cross section area
		"""
		self.r = sqrt(s/PI)

	@property
	def circumference(self):
		"""
		Get circumference of sphere

		:return: float circumference
		"""
		return 2 * PI * self.r

	@circumference.setter
	def circumference(self, c: float):
		"""
		Set circumference of sphere (change radius to make specified circumference)

		:param c: circumference
		"""
		self.r = c/(2*PI)

	def print_properties(self):
		prefix = f"SPH '{self.name}' sn={self.sn}"
		print(f"{prefix} material name:", self.material.name)
		print(f"{prefix} xyz0:", self.xyz0)
		print(f"{prefix} radius:", self.r)
		print(f"{prefix} trn:", self.trn)
		print(f"{prefix} diameter:", self.diameter)
		print(f"{prefix} volume:", self.volume)
		print(f"{prefix} surface area:", self.surface_area)
		print(f"{prefix} cross section:", self.cross_section)
		print(f"{prefix} circumference:", self.circumference)

	def phits_print(self):
		"""
		Print PHITS surface definition

		:return: string with PHITS surface definition
		"""
		xyz0 = " ".join(str(i) for i in self.xyz0)
		txt = \
			f"    {self.sn} {self.trn}  " + \
			f"{self.symbol}  {xyz0}  {self.r}" + \
			f" $ name: '{self.name}' (sphere) x0 y0 z0 R"

		if self.trn != "":
			txt += f" with tr{self.trn}"
		return txt

	def draw(self, opacity: float = None, label_center=False, label_base=False):
		"""
		Draw surface using vpython

		:param opacity: set surface opacity, where 1.0 is fully visible
		:param label_center: if True create label for object
		:param label_base: dummy flag, same as label_center for sphere
		:return: vpython.sphere object
		"""
		if opacity is None:
			pass
		else:
			self.opacity = opacity

		sph = vpython.sphere(
			pos=vector(self.x0, self.y0, self.z0),
			color=self.color, opacity=self.opacity,
			radius=self.r)

		lbl = None
		if label_center or label_base:
			xc = notation(self.x0)
			yc = notation(self.y0)
			zc = notation(self.z0)

			txt =\
				f"{self.symbol} '{self.name}' sn: {self.sn}\ncenter: ({xc}, {yc}, {zc})"
			lbl = vpython.label(
				pos=sph.pos, text=txt, font="monospace", box=False, border=6,
				opacity=0.5, space=0, height=14,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random())
		return sph, lbl


class BOX(Surface):

	symbol = "BOX"

	def __init__(
			self,
			xyz0: list = None, a: list = None, b: list = None, c: list = None,
			name="BOX", trn="", material=MAT_WATER):
		"""
		Define BOX surface (all angles are 90deg)

		:param xyz0: base point coordinate [x0, y0, z0]
		:param a: vector from base point to first surface [Ax, Ay, Az]
		:param b: vector from base point to second surface [Bx, By, Bz]
		:param c: vector from base point to third surface [Cx, Cy, Cz]
		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param material: material associated with surface
		"""
		# Default values
		if xyz0 is None:
			xyz0 = [0.0, 0.0, 0.0]
		if a is None:
			a = [1.0, 0.0, 0.0]
		if b is None:
			b = [0.0, 1.0, 0.0]
		if c is None:
			c = [0.0, 0.0, 1.0]

		self.xyz0 = xyz0
		self.a = a
		self.b = b
		self.c = c

		Surface.__init__(self, name, trn, material)
		created_surfaces.append(self)

	@property
	def xyz0(self):
		"""
		Get list of base point coordinate

		:return: list [x0, y0, z0]
		"""
		return self.__xyz0

	@xyz0.setter
	def xyz0(self, xyz0: list):
		"""
		Set list of base point coordinate

		:param xyz0: list [x0, y0, z0]
		"""
		self.__xyz0 = xyz0

	@property
	def x0(self):
		"""
		Get x component of base coordinate

		:return: float x0
		"""
		return self.__xyz0[0]

	@x0.setter
	def x0(self, x0: float):
		"""
		Set x component of base point coordinate

		:param x0: float x0
		"""
		self.__xyz0[0] = x0

	@property
	def y0(self):
		"""
		Get y component of base coordinate

		:return: float y0
		"""
		return self.__xyz0[1]

	@y0.setter
	def y0(self, y0: float):
		"""
		Set y component of base point coordinate

		:param y0: float y0
		"""
		self.__xyz0[1] = y0

	@property
	def z0(self):
		"""
		Get z component of base point coordinate

		:return: float z0
		"""
		return self.__xyz0[2]

	@z0.setter
	def z0(self, z0: float):
		"""
		Set z component of base point coordinate

		:param z0: float z0
		"""
		self.__xyz0[2] = z0

	@property
	def a(self):
		"""
		Get vector from base point to first surface

		:return: list A [Ax, Ay, Az]
		"""
		return self.__a

	@a.setter
	def a(self, a: list):
		"""
		Set vector from base point to first surface

		:param a: list A [Ax, Ay, Az]
		"""
		self.__a = a

	@property
	def b(self):
		"""
		Get vector from base point to second surface

		:return: list B [Bx, By, Bz]
		"""
		return self.__b

	@b.setter
	def b(self, b: list):
		"""
		Set vector from base point to second surface

		:param b: list B [Bx, By, Bz]
		"""
		self.__b = b

	@property
	def c(self):
		"""
		Get vector from base point to third surface

		:return: list C [Cx, Cy, Cz]
		"""
		return self.__c

	@c.setter
	def c(self, c: list):
		"""
		Set vector from base point to third surface

		:param c: list C [Cx, Cy, Cz]
		"""
		self.__c = c

	@property
	def get_center(self):
		"""
		Get center of box as sum of vectors xyz0 and half diagonal

		:return: list [xc, yc, zc]
		"""
		return sum([self.xyz0, self.get_diagonal/2], axis=0)

	@property
	def get_diagonal(self):
		"""
		Get diagonal vector of box as sum of A, B, C vectors

		:return: list diagonal vector of box
		"""
		return sum([self.a, self.b, self.c], axis=0)

	@property
	def get_diagonal_length(self):
		"""
		Get diagonal length of box as module of diagonal vector

		:return: float diagonal length of box
		"""
		return la.norm(self.get_diagonal)

	@property
	def get_len_a(self):
		"""
		Get length of box A vector (along x)

		:return: float length of box A vector
		"""
		return la.norm(self.a)

	@property
	def get_len_b(self):
		"""
		Get length of box B vector (along y)

		:return: float length of box B vector
		"""
		return la.norm(self.b)

	@property
	def get_len_c(self):
		"""
		Get length of box C vector (along z)

		:return: float length of box C vector
		"""
		return la.norm(self.c)

	@property
	def get_volume(self):
		"""
		Get volume of defined box as absolute value of mixed product of vectors
		A, B, C

		:return: volume of defined box
		"""
		return abs(inner(cross(self.a, self.b), self.c))

	@property
	def get_ab_area(self):
		"""
		Get AB box surface area as length of cross of A and B vectors

		:return: AB box surface area
		"""
		return la.norm(cross(self.a, self.b))

	@property
	def get_ac_area(self):
		"""
		Get AC box surface area as length of cross of A and C vectors

		:return: AC surface area
		"""
		return la.norm(cross(self.a, self.c))

	@property
	def get_bc_area(self):
		"""
		Get BC box surface area as length of cross of B and C vectors

		:return: BC surface area
		"""
		return la.norm(cross(self.b, self.c))

	@property
	def get_full_area(self):
		"""
		Get full box surface area

		:return: full box surface area
		"""
		return 2 * (self.get_ab_area + self.get_ac_area + self.get_bc_area)

	def print_properties(self):
		prefix = f"BOX '{self.name}' sn={self.sn}"
		print(f"{prefix} material name:", self.material.name)
		print(f"{prefix} xyz0:", self.xyz0)
		print(f"{prefix} a:", self.a)
		print(f"{prefix} a length:", self.get_len_a)
		print(f"{prefix} b:", self.b)
		print(f"{prefix} b length:", self.get_len_b)
		print(f"{prefix} c:", self.c)
		print(f"{prefix} c length:", self.get_len_c)
		print(f"{prefix} trn:", self.trn)
		print(f"{prefix} center:", self.get_center)
		print(f"{prefix} diagonal:", self.get_diagonal)
		print(f"{prefix} diagonal length:", self.get_diagonal_length)
		print(f"{prefix} volume:", self.get_volume)
		print(f"{prefix} AB area:", self.get_ab_area)
		print(f"{prefix} AC area:", self.get_ac_area)
		print(f"{prefix} BC area:", self.get_bc_area)
		print(f"{prefix} full area:", self.get_full_area)

	def phits_print(self):
		"""
		Print PHITS surface definition

		:return: string with PHITS surface definition
		"""
		xyz0 = " ".join(str(i) for i in self.xyz0)
		a = " ".join(str(i) for i in self.a)
		b = " ".join(str(i) for i in self.b)
		c = " ".join(str(i) for i in self.c)
		txt = \
			f"    {self.sn} {self.trn}  " + \
			f"{self.symbol}  {xyz0}  {a}  {b}  {c}" + \
			f" $ name: '{self.name}' " + \
			"(box, all angles are 90deg) [x0 y0 z0] [Ax Ay Az] [Bx By Bz] [Cx Cy Cz]"

		if self.trn != "":
			txt += f" with tr{self.trn}"
		return txt

	def draw(self, opacity: float = None, label_base=False, label_center=False):
		"""
		Draw surface using vpython

		:param opacity: set surface opacity, where 1.0 - fully visible
		:param label_base: if True create label for object base
		:param label_center: if True create label for object center
		:return: vpython.box and vpython.label objects
		"""
		if opacity is None:
			pass
		else:
			self.opacity = opacity

		x0 = self.get_center[0]
		y0 = self.get_center[1]
		z0 = self.get_center[2]

		# TODO: recheck
		direction = vector(self.c[0], self.c[1], self.c[2])

		box = vpython.box(
			color=self.color, opacity=self.opacity,
			pos=vector(x0, y0, z0),
			length=self.get_len_c,
			height=self.get_len_b,
			width=self.get_len_a,
			axis=direction)

		lbl_c, lbl_b = None, None
		txt = f"{self.symbol} '{self.name}' sn: {self.sn}\n"
		if label_center:
			xc = notation(self.get_center[0])
			yc = notation(self.get_center[1])
			zc = notation(self.get_center[2])

			txt_c = txt + f"center: ({xc}, {yc}, {zc})"
			lbl_c = vpython.label(
				pos=box.pos, text=txt_c, font="monospace", box=False, border=6,
				opacity=0.5,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random(),
				space=0,
				height=14)

		if label_base:
			xb = notation(self.xyz0[0])
			yb = notation(self.xyz0[1])
			zb = notation(self.xyz0[2])

			txt_b = txt + f"base: ({xb}, {yb}, {zb})"
			lbl_b = vpython.label(
				pos=vector(self.xyz0[0], self.xyz0[1], self.xyz0[2]),
				text=txt_b, font="monospace", box=False, opacity=0.5, border=6,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random(),
				space=0,
				height=14)
		return box, lbl_c, lbl_b


class RPP(Surface):

	symbol = "RPP"

	def __init__(
			self,
			x: list = None, y: list = None, z: list = None,
			name="RPP", trn="", material=MAT_WATER):
		"""
		Define RPP (Rectangular solid) similar to BOX, but which each surface is
		vertical with x, y, z axes

		:param x: list with x min and max components [x_min, x_max]
		:param y: list with y min and max components [y_min, y_max]
		:param z: list with z min and max components [z_min, z_max]
		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param material: material associated with surface
		"""
		# Default values
		if x is None:
			x = [-1.0, 1.0]
		if y is None:
			y = [-1.0, 1.0]
		if z is None:
			z = [-1.0, 1.0]

		self.x = x
		self.y = y
		self.z = z

		Surface.__init__(self, name, trn, material)
		created_surfaces.append(self)

	@property
	def x(self):
		"""
		Get list with x min and max components

		:return: list [x_min, x_max]
		"""
		return self.__x

	@x.setter
	def x(self, x: list):
		"""
		Set list with x min and max components

		:param x: [x_min, x_max]
		"""
		self.__x = x

	@property
	def y(self):
		"""
		Get list with y min and max components

		:return: list [y_min, y_max]
		"""
		return self.__y

	@y.setter
	def y(self, y: list):
		"""
		Set list with y min and max components

		:param y: [y_min, y_max]
		"""
		self.__y = y

	@property
	def z(self):
		"""
		Get list with z min and max components

		:return: list [z_min, z_max]
		"""
		return self.__z

	@z.setter
	def z(self, z: list):
		"""
		Set list with z min and max components

		:param z: [z_min, z_max]
		"""
		self.__z = z

	@property
	def get_width(self):
		"""
		Get width along x
		:return: float x_max - x_min
		"""
		return self.x[1] - self.x[0]

	@property
	def get_height(self):
		"""
		Get height along y
		:return: float y_max - y_min
		"""
		return self.y[1] - self.y[0]

	@property
	def get_length(self):
		"""
		Get length along z
		:return: float z_max - z_min
		"""
		return self.z[1] - self.z[0]

	@property
	def get_center(self):
		"""
		Get center of rectangular solid

		:return: list [xc, yc, zc]
		"""
		return [
			self.x[0] + self.get_width/2,
			self.y[0] + self.get_height/2,
			self.z[0] + self.get_length/2]

	@property
	def get_diagonal_length(self):
		"""
		Get diagonal length of RPP as sqrt(width^2+height^2+length^2)

		:return: float diagonal length of RPP
		"""
		a = power(self.get_width, 2)
		b = power(self.get_height, 2)
		c = power(self.get_length, 2)

		return sqrt(a + b + c)

	@property
	def get_volume(self):
		"""
		Get volume

		:return: float volume
		"""
		return self.get_length * self.get_width * self.get_height

	@property
	def get_wh_area(self):
		"""
		Get width*height surface area

		:return: float width*height surface area
		"""
		return self.get_width * self.get_height

	@property
	def get_wl_area(self):
		"""
		Get width*length surface area

		:return: float width*length surface area
		"""
		return self.get_width * self.get_length

	@property
	def get_hl_area(self):
		"""
		Get height*length surface area

		:return: float height*length surface area
		"""
		return self.get_height * self.get_length

	@property
	def get_full_area(self):
		"""
		Get full surface area

		:return: float full surface area
		"""
		return 2 * (self.get_wh_area + self.get_wl_area + self.get_hl_area)

	def print_properties(self):
		prefix = f"RPP '{self.name}' sn={self.sn}"
		print(f"{prefix} material name:", self.material.name)
		print(f"{prefix} x:", self.x)
		print(f"{prefix} y:", self.y)
		print(f"{prefix} z:", self.z)
		print(f"{prefix} trn:", self.trn)
		print(f"{prefix} width:", self.get_width)
		print(f"{prefix} heigth:", self.get_height)
		print(f"{prefix} length:", self.get_length)
		print(f"{prefix} center:", self.get_center)
		print(f"{prefix} diagonal length:", self.get_diagonal_length)
		print(f"{prefix} volume:", self.get_volume)
		print(f"{prefix} width*height area:", self.get_wh_area)
		print(f"{prefix} width*length area:", self.get_wl_area)
		print(f"{prefix} height*length area:", self.get_hl_area)
		print(f"{prefix} full area:", self.get_full_area)

	def phits_print(self):
		"""
		Print PHITS surface definition

		:return: string with PHITS surface definition
		"""
		x = " ".join(str(i) for i in self.x)
		y = " ".join(str(i) for i in self.y)
		z = " ".join(str(i) for i in self.z)
		txt = \
			f"    {self.sn} {self.trn}  " + \
			f"{self.symbol}  {x}  {y}  {z}" + \
			f" $ name: '{self.name}' " + \
			"(Rectangular solid) [x_min x_max] [y_min y_max] [z_min z_max]"

		if self.trn != "":
			txt += f" with tr{self.trn}"
		return txt

	def draw(self, opacity: float = None, label_center=False):
		"""
		Draw surface using vpython

		:param opacity: set surface opacity, where 1.0 - fully visible
		:param label_center: if True create label for object
		:return: vpython.box and vpython.label objects
		"""
		if opacity is None:
			pass
		else:
			self.opacity = opacity

		x0 = self.get_center[0]
		y0 = self.get_center[1]
		z0 = self.get_center[2]

		box = vpython.box(
			color=self.color, opacity=self.opacity,
			pos=vector(x0, y0, z0),
			length=self.get_width,  # x and z swap
			height=self.get_height,
			width=self.get_length)  # x and z swap

		lbl = None
		if label_center:
			xc = notation(self.get_center[0])
			yc = notation(self.get_center[1])
			zc = notation(self.get_center[2])

			txt =\
				f"{self.symbol} '{self.name}' sn: {self.sn}\ncenter: ({xc}, {yc}, {zc})"
			lbl = vpython.label(
				pos=box.pos, text=txt, font="monospace", box=False, border=6,
				opacity=0.5,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random(),
				space=0,
				height=14)
		return box, lbl


class RCC(Surface):

	symbol = "RCC"

	def __init__(
			self,
			xyz0: list = None, h: list = None, r=0.5,
			name="RCC", trn="", material=MAT_WATER):
		"""
		Define RCC (cylinder)

		:param xyz0: center coordinate of bottom face [x0, y0, z0]
		:param h: vector from the bottom to the top [Hx, Hy, Hz]
		:param r: radius of bottom face
		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param material: material associated with surface
		"""
		# Default values
		if xyz0 is None:
			xyz0 = [0.0, 0.0, 0.0]
		if h is None:
			h = [0.0, 1.0, 0.0]

		self.xyz0 = xyz0
		self.h = h
		self.r = r

		Surface.__init__(self, name, trn, material)
		created_surfaces.append(self)

	@property
	def xyz0(self):
		"""
		Get list of center coordinate of bottom face

		:return: list [x0, y0, z0]
		"""
		return self.__xyz0

	@xyz0.setter
	def xyz0(self, xyz0: list):
		"""
		Set list of center coordinate of bottom face

		:param xyz0: [x0, y0, z0]
		"""
		self.__xyz0 = xyz0

	@property
	def x0(self):
		"""
		Get x component of center coordinate of bottom face

		:return: float x0
		"""
		return self.__xyz0[0]

	@x0.setter
	def x0(self, x0: float):
		"""
		Set x component of center coordinate of bottom face

		:param x0: float x0
		"""
		self.__xyz0[0] = x0

	@property
	def y0(self):
		"""
		Get y component of center coordinate of bottom face

		:return: float y0
		"""
		return self.__xyz0[1]

	@y0.setter
	def y0(self, y0: float):
		"""
		Set y component of center coordinate of bottom face

		:param y0: float y0
		"""
		self.__xyz0[1] = y0

	@property
	def z0(self):
		"""
		Get z component of center coordinate of bottom face

		:return: float z0
		"""
		return self.__xyz0[2]

	@z0.setter
	def z0(self, z0: float):
		"""
		Set z component of center coordinate of bottom face

		:param z0: float z0
		"""
		self.__xyz0[2] = z0

	@property
	def h(self):
		"""
		Get height vector from center of bottom face to that of top face

		:return: list [Hx, Hy, Hz]
		"""
		return self.__h

	@h.setter
	def h(self, h: list):
		"""
		Set height vector from center of bottom face to that of top face

		:param h: list [Hx, Hy, Hz]
		"""
		self.__h = h

	@property
	def r(self):
		"""
		Get radius of bottom face

		:return: float radius
		"""
		return self.__r

	@r.setter
	def r(self, r: float):
		"""
		Set bottom face radius

		:param r: radius
		"""
		self.__r = r

	@property
	def diameter(self):
		"""
		Get bottom face diameter

		:return: Float D
		"""
		return self.r * 2

	@diameter.setter
	def diameter(self, diameter: float):
		"""
		Set bottom face diameter (change radius to make specified diameter)

		:param diameter: diameter
		"""
		self.r = diameter/2

	@property
	def circumference(self):
		"""
		Get cylinder bottom face circumference

		:return: float circumference
		"""
		return 2 * PI * self.r

	@circumference.setter
	def circumference(self, c: float):
		"""
		Set circumference of cylinder bottom face
		(change radius to make specified circumference)

		:param c: circumference
		"""
		self.r = c/(2*PI)

	@property
	def bottom_area(self):
		"""
		Get bottom face area of cylinder

		:return: float bottom face area
		"""
		return PI * power(self.r, 2)

	@bottom_area.setter
	def bottom_area(self, b_area: float):
		"""
		Set bottom face area of cylinder (change radius to make specified area)

		:param b_area: bottom face area of cylinder
		"""
		self.r = sqrt(b_area/PI)

	@property
	def get_center(self):
		"""
		Get cylinder center as half height vector

		:return: list [xc, yc, zc]
		"""
		hx = self.h[0]
		hy = self.h[1]
		hz = self.h[2]

		return sum([self.xyz0, [hx/2, hy/2, hz/2]], axis=0)

	@property
	def get_len_h(self):
		"""
		Get length of height vector

		:return: float length of height vector
		"""
		return la.norm(self.h)

	@property
	def get_volume(self):
		"""
		Get volume

		:return: float volume
		"""
		return PI * power(self.r, 2) * self.get_len_h

	@property
	def get_side_area(self):
		"""
		Get side face surface area

		:return: float side face area
		"""
		return PI * self.diameter * self.get_len_h

	@property
	def get_full_area(self):
		"""
		Get full surface area

		:return: float full surface area
		"""
		return 2 * self.bottom_area + self.get_side_area

	def print_properties(self):
		prefix = f"RCC '{self.name}' sn={self.sn}"
		print(f"{prefix} material name:", self.material.name)
		print(f"{prefix} xyz0:", self.xyz0)
		print(f"{prefix} h:", self.h)
		print(f"{prefix} radius:", self.r)
		print(f"{prefix} trn:", self.trn)
		print(f"{prefix} diameter:", self.diameter)
		print(f"{prefix} circumference:", self.circumference)
		print(f"{prefix} bottom area:", self.bottom_area)
		print(f"{prefix} center:", self.get_center)
		print(f"{prefix} H length:", self.get_len_h)
		print(f"{prefix} volume:", self.get_volume)
		print(f"{prefix} side area:", self.get_side_area)
		print(f"{prefix} full area:", self.get_full_area)

	def phits_print(self):
		"""
		Print PHITS surface definition

		:return: string with PHITS surface definition
		"""
		xyz0 = " ".join(str(i) for i in self.xyz0)
		h = " ".join(str(i) for i in self.h)
		txt = \
			f"    {self.sn} {self.trn}  " + \
			f"{self.symbol}  {xyz0}  {h}  {self.r}" + \
			f" $ name: '{self.name}' (cylinder) [x0 y0 z0] [Hx Hy Hz] R"

		if self.trn != "":
			txt += f" with tr{self.trn}"
		return txt

	def draw(self, opacity: float = None, label_base=False, label_center=False):
		"""
		Draw surface using vpython

		:param opacity: set surface opacity, where 1.0 - fully visible
		:param label_base: if True create label for object base
		:param label_center: if True create label for object center
		:return: vpython.cylinder object
		"""
		if opacity is None:
			pass
		else:
			self.opacity = opacity

		x0 = self.xyz0[0]
		y0 = self.xyz0[1]
		z0 = self.xyz0[2]

		direction = vector(self.h[0], self.h[1], self.h[2])

		cyl = vpython.cylinder(
			color=self.color, opacity=self.opacity,
			pos=vector(x0, y0, z0),
			axis=direction,
			radius=self.r)

		lbl_c, lbl_b = None, None
		txt = f"{self.symbol} '{self.name}' sn: {self.sn}\n"
		if label_center:
			xc = notation(self.get_center[0])
			yc = notation(self.get_center[1])
			zc = notation(self.get_center[2])

			txt_c = txt + f"center: ({xc}, {yc}, {zc})"
			lbl_c = vpython.label(
				pos=vector(self.get_center[0], self.get_center[1], self.get_center[2]),
				text=txt_c, font="monospace", box=False, opacity=0.5, border=6,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random(),
				space=0, height=14)

		if label_base:
			xb = notation(cyl.pos.x)
			yb = notation(cyl.pos.y)
			zb = notation(cyl.pos.z)

			txt_b = txt + f"base: ({xb}, {yb}, {zb})"
			lbl_b = vpython.label(
				pos=cyl.pos, font="monospace", box=False, opacity=0.5, border=6,
				text=txt_b,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random(),
				space=0, height=14)
		return cyl, lbl_c, lbl_b


class TRC(Surface):

	symbol = "TRC"

	def __init__(
			self,
			xyz0: list = None, h: list = None, r_1=0.5, r_2=0.1,
			name="RCC", trn="", material=MAT_WATER):
		"""
		Define TRC (truncated right-angle cone) surface

		:param xyz0: center coordinate of bottom face [x0, y0, z0]
		:param h: height vector from center of bottom [Hx, Hy, Hz]
		:param r_1: radius of bottom face
		:param r_2: radius of top face
		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param material: material associated with surface
		"""
		# Default values
		if xyz0 is None:
			xyz0 = [0.0, 0.0, 0.0]
		if h is None:
			h = [0.0, 1.0, 0.0]

		self.xyz0 = xyz0
		self.h = h
		self.r_1 = r_1
		self.r_2 = r_2

		Surface.__init__(self, name, trn, material)
		created_surfaces.append(self)

	@property
	def xyz0(self):
		"""
		Get center coordinate of bottom face

		:return: list [x0, y0, z0]
		"""
		return self.__xyz0

	@xyz0.setter
	def xyz0(self, xyz0: list):
		"""
		Set center coordinate of bottom face

		:param xyz0: [x0, y0, z0]
		"""
		self.__xyz0 = xyz0

	@property
	def x0(self):
		"""
		Get x component of center coordinate of bottom face

		:return: float x0
		"""
		return self.__xyz0[0]

	@x0.setter
	def x0(self, x0: float):
		"""
		Set x component of center coordinate of bottom face

		:param x0: x0
		"""
		self.__xyz0[0] = x0

	@property
	def y0(self):
		"""
		Get y component of center coordinate of bottom face

		:return: float y0
		"""
		return self.__xyz0[1]

	@y0.setter
	def y0(self, y0: float):
		"""
		Set y component of center coordinate of bottom face

		:param y0: y0
		"""
		self.__xyz0[1] = y0

	@property
	def z0(self):
		"""
		Get z component of center coordinate of bottom face

		:return: float z0
		"""
		return self.__xyz0[2]

	@z0.setter
	def z0(self, z0: float):
		"""
		Set z component of center coordinate of bottom face

		:param z0: z0
		"""
		self.__xyz0[2] = z0

	@property
	def h(self):
		"""
		Get height vector from center of bottom face to that of top face

		:return: list [Hx, Hy, Hz]
		"""
		return self.__h

	@h.setter
	def h(self, h: list):
		"""
		Set height vector from center of bottom face to that of top face

		:param h: [Hx, Hy, Hz]
		"""
		self.__h = h

	@property
	def r_1(self):
		"""
		Get radius of bottom face

		:return: float bottom radius
		"""
		return self.__r_1

	@r_1.setter
	def r_1(self, r_1: float):
		"""
		Set bottom face radius

		:param r_1: bottom radius
		"""
		self.__r_1 = r_1

	@property
	def r_2(self):
		"""
		Get top face radius

		:return: float top radius
		"""
		return self.__r_2

	@r_2.setter
	def r_2(self, r_2: float):
		"""
		Set top face radius

		:param r_2: top radius
		"""
		self.__r_2 = r_2

	@property
	def bottom_diameter(self):
		"""
		Get bottom face diameter

		:return: float bottom diameter
		"""
		return self.r_1 * 2

	@bottom_diameter.setter
	def bottom_diameter(self, bottom_diameter: float):
		"""
		Set bottom face diameter (change radius to make specified diameter)

		:param bottom_diameter: bottom face diameter
		"""
		self.r_1 = bottom_diameter/2

	@property
	def top_diameter(self):
		"""
		Get top face diameter

		:return: float top face diameter
		"""
		return self.r_2 * 2

	@top_diameter.setter
	def top_diameter(self, top_diameter: float):
		"""
		Set top face diameter (change radius to make specified diameter)

		:param top_diameter: top face diameter
		"""
		self.r_2 = top_diameter/2

	@property
	def bottom_circumference(self):
		"""
		Get cone bottom face circumference

		:return: float circumference
		"""
		return 2 * PI * self.r_1

	@bottom_circumference.setter
	def bottom_circumference(self, b_c: float):
		"""
		Set circumference of cone bottom face
		(change radius to make specified circumference)

		:param b_c: circumference
		"""
		self.r_1 = b_c/(2*PI)

	@property
	def top_circumference(self):
		"""
		Get cone top face circumference

		:return: float circumference
		"""
		return 2 * PI * self.r_2

	@top_circumference.setter
	def top_circumference(self, t_c: float):
		"""
		Set circumference of cone top face
		(change radius to make specified circumference)

		:param t_c: circumference
		"""
		self.r_2 = t_c/(2*PI)

	@property
	def bottom_area(self):
		"""
		Get bottom face area of cone

		:return: float bottom face area
		"""
		return PI * power(self.r_1, 2)

	@bottom_area.setter
	def bottom_area(self, b_area: float):
		"""
		Set bottom face area of cone (change radius to make specified area)

		:param b_area: bottom face area of cone
		"""
		self.r_1 = sqrt(b_area/PI)

	@property
	def top_area(self):
		"""
		Get top face area of cone

		:return: float bottom face area
		"""
		return PI * power(self.r_2, 2)

	@top_area.setter
	def top_area(self, t_area: float):
		"""
		Set top face area of cone (change radius to make specified area)

		:param t_area: top face area of cone
		"""
		self.r_2 = sqrt(t_area/PI)

	@property
	def get_center(self):
		"""
		Get cone center as half height vector

		:return: list [xc, yc, zc]
		"""
		hx = self.h[0]
		hy = self.h[1]
		hz = self.h[2]

		return sum([self.xyz0, [hx/2, hy/2, hz/2]], axis=0)

	@property
	def get_len_h(self):
		"""
		Get length of height vector

		:return: float height
		"""
		return la.norm(self.h)

	@property
	def get_forming(self):
		"""
		Get cone forming

		:return: float forming
		"""
		return sqrt(power(self.get_len_h, 2) + power(self.r_1-self.r_2, 2))

	@property
	def get_volume(self):
		"""
		Get cone volume as 1/3 * pi * H * (R_1^2 + R_1 * R_2 + R_2^2)

		:return: float volume
		"""
		return\
			(1/3) * PI * self.get_len_h * \
			(power(self.r_1, 2) + self.r_1 * self.r_2 + power(self.r_2, 2))

	@property
	def get_side_area(self):
		"""
		Get cone side face surface area as pi*L*(R+r)

		:return: float side face area
		"""
		return PI * self.get_forming * (self.r_1 + self.r_2)

	@property
	def get_full_area(self):
		"""
		Get full surface area

		:return: float full surface area
		"""
		return self.bottom_area + self.top_area + self.get_side_area

	def print_properties(self):
		prefix = f"TRC '{self.name}' sn={self.sn}"
		print(f"{prefix} material name:", self.material.name)
		print(f"{prefix} xyz0:", self.xyz0)
		print(f"{prefix} h:", self.h)
		print(f"{prefix} radius of bottom face (r_1):", self.r_1)
		print(f"{prefix} radius of top face (r_2):", self.r_2)
		print(f"{prefix} trn:", self.trn)
		print(f"{prefix} bottom diameter:", self.bottom_diameter)
		print(f"{prefix} top diameter:", self.top_diameter)
		print(f"{prefix} bottom area:", self.bottom_area)
		print(f"{prefix} top area:", self.top_area)
		print(f"{prefix} center:", self.get_center)
		print(f"{prefix} H length:", self.get_len_h)
		print(f"{prefix} forming L:", self.get_forming)
		print(f"{prefix} volume:", self.get_volume)
		print(f"{prefix} side area:", self.get_side_area)
		print(f"{prefix} full area:", self.get_full_area)

	def phits_print(self):
		"""
		Print PHITS surface definition

		:return: string with PHITS surface definition
		"""
		xyz0 = " ".join(str(i) for i in self.xyz0)
		h = " ".join(str(i) for i in self.h)
		txt = \
			f"    {self.sn} {self.trn}  " + \
			f"{self.symbol}  {xyz0}  {h}  {self.r_1}  {self.r_2}" + \
			f" $ name: '{self.name}' " + \
			"(truncated right-angle cone) [x0 y0 z0] [Hx Hy Hz] R_b R_t"

		if self.trn != "":
			txt += f" with tr{self.trn}"
		return txt

	def draw(
			self, opacity: float = None,
			label_base=False, label_center=False, truncated=True):
		"""
		Draw surface using vpython

		:param opacity: set surface opacity, where 1.0 - fully visible
		:param label_base: if True create label for object base
		:param label_center: if True create label for object center
		:param truncated: if True draw as truncated, otherwise simple cone
		:return: vpython.cylinder object
		"""
		if opacity is None:
			pass
		else:
			self.opacity = opacity

		color = self.color
		opacity = self.opacity
		position = vector(self.x0, self.y0, self.z0)
		direction = vector(self.h[0], self.h[1], self.h[2])

		if truncated:
			# TODO: should work for every case (truncated or not),
			#  but may be unstable in visualization and takes more time to draw
			#  Sometimes works not as expected!
			r1 = self.r_1
			r2 = self.r_2
			r_min = amin([r1, r2])
			h = self.get_len_h

			s = [[-r1, 0], [-r2, h], [r2, h], [r1, 0], [-r1, 0]]  # Shape
			p = vpython.paths.circle(pos=position, up=direction, radius=r_min/1e3)

			cone = vpython.extrusion(
				path=p, shape=s, opacity=opacity, color=color, up=direction)

		else:  # TODO: works only for not truncated cones
			cone = vpython.cone(
				opacity=opacity, color=color,
				pos=position, axis=direction, radius=self.r_1)

		lbl_c, lbl_b = None, None
		txt = f"{self.symbol} '{self.name}' sn: {self.sn}\n"
		if label_center:
			xc = notation(self.get_center[0])
			yc = notation(self.get_center[1])
			zc = notation(self.get_center[2])

			txt_c = txt + f"center: ({xc}, {yc}, {zc})"
			lbl_c = vpython.label(
				pos=vector(self.get_center[0], self.get_center[1], self.get_center[2]),
				text=txt_c, font="monospace", box=False, opacity=0.5, border=6,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random(),
				space=0, height=14)

		if label_base:
			xb = notation(self.x0)
			yb = notation(self.y0)
			zb = notation(self.z0)

			txt_b = txt + f"base: ({xb}, {yb}, {zb})"
			lbl_b = vpython.label(
				pos=position, space=0, height=14,
				text=txt_b, font="monospace", box=False, opacity=0.5, border=6,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random())
		return cone, lbl_c, lbl_b


class T(Surface):
	symbol_tx, symbol_ty, symbol_tz = "TX", "TY", "TZ"

	def __init__(
			self, xyz0: list = None, r=0.5, b=0.08, c=0.1,
			name="T", trn="", material=MAT_WATER, rot="y"):
		"""
		Define T (torus) surface: TX (with x rotational axis),
		TY (with y rotational axis), TZ (with z rotational axis)

		:param xyz0: the center of the torus surface [x0, y0, z0]
		:param r: distance between xyz0 (rotational axis) and ellipse center
		:param b: semi-minor axis (ellipse half "height")
		:param c: semi-major axis (ellipse half "width")
		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param rot: rotational axis ("x", "y", "z")
		"""
		# Default value
		if xyz0 is None:
			xyz0 = [0.0, 0.0, 0.0]

		self.xyz0 = xyz0
		self.r = r
		self.b = b
		self.c = c

		Surface.__init__(self, name, trn, material)
		self.rot = rot
		created_surfaces.append(self)

	@property
	def xyz0(self):
		"""
		Get center

		:return: list [x0, y0, z0]
		"""
		return self.__xyz0

	@xyz0.setter
	def xyz0(self, xyz0: list):
		"""
		Set center

		:param xyz0: [x0, y0, z0]
		"""
		self.__xyz0 = xyz0

	@property
	def x0(self):
		"""
		Get x component of center

		:return: float x0
		"""
		return self.__xyz0[0]

	@x0.setter
	def x0(self, x0: float):
		"""
		Set x component of center

		:param x0: float x0
		"""
		self.__xyz0[0] = x0

	@property
	def y0(self):
		"""
		Get y component of center

		:return: float y0
		"""
		return self.__xyz0[1]

	@y0.setter
	def y0(self, y0: float):
		"""
		Set y component of center

		:param y0: float y0
		"""
		self.__xyz0[1] = y0

	@property
	def z0(self):
		"""
		Get z component of center

		:return: Float z0
		"""
		return self.__xyz0[2]

	@z0.setter
	def z0(self, z0: float):
		"""
		Set z component of center

		:param z0: float z0
		"""
		self.__xyz0[2] = z0

	@property
	def r(self):
		"""
		Get R parameter: distance between xyz0 and center of the ellipse (radius)

		:return: float radius
		"""
		return self.__r

	@r.setter
	def r(self, r: float):
		"""
		Set R parameter: distance between xyz0 and center of the ellipse (radius)

		:param r: Float R parameter
		"""
		self.__r = r

	@property
	def b(self):
		"""
		Get parameter B: ellipse "height" (half)

		:return: float parameter B
		"""
		return self.__b

	@b.setter
	def b(self, b: float):
		"""
		Set parameter B: ellipse "height" (half)

		:param b: parameter B
		"""
		self.__b = b

	@property
	def c(self):
		"""
		Get parameter C: ellipse "width" (half)

		:return: float parameter C
		"""
		return self.__c

	@c.setter
	def c(self, c: float):
		"""
		Set parameter C: ellipse "width" (half)

		:param c: parameter C
		"""
		self.__c = c

	@property
	def rot(self):
		"""
		Get rotational axis

		:return: string axis ("x", "y", "z")
		"""
		return self.__rot

	@rot.setter
	def rot(self, rot: str):
		"""
		Set rotational axis

		:param rot: string with axis ("x" "y" or "z")
		"""
		self.__rot = rot

	@property
	def circumference(self):
		"""
		Get torus circumference

		:return: float circumference
		"""
		return 2 * PI * self.r

	@circumference.setter
	def circumference(self, circumference: float):
		"""
		Set torus circumference (change radius to make specified circumference)

		:param circumference: circumference
		"""
		self.r = circumference/(2*PI)

	@property
	def symbol(self):
		"""
		Get symbol depending on rot value

		:return: "TX", "TY" or "TZ", depending on rot value
		"""
		if self.rot == "x":
			return self.symbol_tx
		elif self.rot == "z":
			return self.symbol_tz
		else:
			return self.symbol_ty

	@property
	def get_cross_section(self):
		"""
		Get the cross section area of torus as PI * B * C

		:return: float cross section area
		"""
		return PI * self.b * self.c

	@property
	def get_full_area(self):
		"""
		Get full surface area of torus for two cases:
			1) b = c = r: S = 4 * pi^2 * R * r;
			2) general case: 8 * pi * c * R * E(e^2), where
			E(e) - complete elliptic integral of the first kind and
			e = sqrt(1 - (power(self.b, 2)/power(self.c, 2)) )
			the eccentricity of the ellipse cross section
			https://mathworld.wolfram.com/EllipticTorus.html

		:return: float full surface area
		"""
		if self.b == self.c:
			return 4 * power(PI, 2) * self.r * self.b  # or self.c

		else:
			b = self.b
			a = self.c

			if self.b > self.c:  # To avoid negative value in e
				b = self.c
				a = self.b

			e = sqrt(1 - (power(b, 2)/power(a, 2)))
			e2 = power(e, 2)
			return 8 * PI * a * self.r * ellipk(e2)

	@property
	def get_volume(self):
		"""
		Get volume of torus as V = 2 * pi^2 * b * c * R
		:return: float volume
		"""
		return 2 * power(PI, 2) * self.b * self.c * self.r

	def print_properties(self):
		prefix = f"T '{self.name}' sn={self.sn}"
		print(f"{prefix} material name:", self.material.name)
		print(f"{prefix} xyz0:", self.xyz0)
		print(f"{prefix} radius:", self.r)
		print(f"{prefix} semi-minor axis:", self.b)
		print(f"{prefix} semi-major axis:", self.c)
		print(f"{prefix} trn:", self.trn)
		print(f"{prefix} rotational axis:", self.rot)
		print(f"{prefix} circumference:", self.circumference)
		print(f"{prefix} cross section:", self.get_cross_section)
		print(f"{prefix} full area:", self.get_full_area)
		print(f"{prefix} volume:", self.get_volume)

	def phits_print(self):
		"""
		Print PHITS surface definition

		:return: string with PHITS surface definition
		"""
		xyz0 = " ".join(str(i) for i in self.xyz0)

		txt = \
			f"    {self.sn} {self.trn}  " + \
			f"{self.symbol}  {xyz0}  {self.r}  {self.b}  {self.c}" + \
			f" $ name: '{self.name}' " + \
			f"(torus, with {self.rot} rotational axis) " + \
			"[x0 y0 z0] A(R) B C"

		if self.trn != "":
			txt += f" with tr{self.trn}"
		return txt

	def draw(self, opacity: float = None, label_center=False, label_base=False):
		"""
		Draw surface using vpython

		:param opacity: set surface opacity, where 1.0 - fully visible
		:param label_center: If True create label for object
		:param label_base: Dummy, same as label_center
		:return: vpython.ring object
		"""
		if opacity is None:
			pass
		else:
			self.opacity = opacity

		width = self.b
		height = self.c

		rot_axis = vector(0, 1, 0)  # y axis by default
		if self.rot == "x":
			rot_axis = vector(1, 0, 0)  # x axis
		elif self.rot == "z":
			rot_axis = vector(0, 0, 1)  # z axis
		else:
			width = self.c
			height = self.b

		p = vpython.paths.circle(
			pos=vector(self.x0, self.y0, self.z0),
			up=rot_axis, radius=self.r)

		s = vpython.shapes.ellipse(width=width, height=height)
		tor = vpython.extrusion(
			path=p, shape=s, color=self.color, opacity=self.opacity)

		lbl = None
		if label_center or label_base:
			xc = notation(self.x0)
			yc = notation(self.y0)
			zc = notation(self.z0)

			txt =\
				f"{self.symbol} '{self.name}' sn: {self.sn}\ncenter: ({xc}, {yc}, {zc})"
			lbl = vpython.label(
				font="monospace", box=False, space=0, border=6, height=14,
				pos=tor.pos, text=txt, opacity=0.5,
				# for random directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random())
		return tor, lbl


class REC(Surface):
	symbol = "REC"

	def __init__(
			self,
			xyz0: list = None, h: list = None, a: list = None, b: list = None,
			name="REC", trn="", material=MAT_WATER):
		"""
		Define REC (right elliptical cylinder) surface

		:param xyz0: center coordinate of bottom face [x0, y0, z0]
		:param h: height vector from center of bottom face [Hx, Hy, Hz]
		:param a: semi-major axis vector of ellipse orthogonal to H [Ax, Ay, Az]
		:param b: semi-minor axis vector of ellipse orthogonal to H and A [Bx, By, Bz]
		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param material: material associated with surface
		"""
		# Default values
		if xyz0 is None:
			xyz0 = [0.0, 0.0, 0.0]
		if h is None:
			h = [0.0, 1.0, 0.0]
		if a is None:
			a = [0.7, 0.0, 0.0]
		if b is None:
			b = [0.0, 0.0, 1.0]

		self.xyz0 = xyz0
		self.h = h
		self.a = a
		self.b = b

		Surface.__init__(self, name, trn, material)
		created_surfaces.append(self)

	@property
	def xyz0(self):
		"""
		Get list of center coordinate of bottom face

		:return: list [x0, y0, z0]
		"""
		return self.__xyz0

	@xyz0.setter
	def xyz0(self, xyz0: list):
		"""
		Set list of center coordinate of bottom face

		:param xyz0: list [x0, y0, z0]
		"""
		self.__xyz0 = xyz0

	@property
	def x0(self):
		"""
		Get x component of center coordinate of bottom face

		:return: float x0
		"""
		return self.__xyz0[0]

	@x0.setter
	def x0(self, x0: float):
		"""
		Set x component of center coordinate of bottom face

		:param x0: float x0
		"""
		self.__xyz0[0] = x0

	@property
	def y0(self):
		"""
		Get y component of center coordinate of bottom face

		:return: float y0
		"""
		return self.__xyz0[1]

	@y0.setter
	def y0(self, y0: float):
		"""
		Set y component of center coordinate of bottom face

		:param y0: float y0
		"""
		self.__xyz0[1] = y0

	@property
	def z0(self):
		"""
		Get z component of center coordinate of bottom face

		:return: float z0
		"""
		return self.__xyz0[2]

	@z0.setter
	def z0(self, z0: float):
		"""
		Set z component of center coordinate of bottom face

		:param z0: float z0
		"""
		self.__xyz0[2] = z0

	@property
	def h(self):
		"""
		Get height vector from center of bottom face to the top [Hx, Hy, Hz]

		:return: list [Hx, Hy, Hz]
		"""
		return self.__h

	@h.setter
	def h(self, h: list):
		"""
		Set height vector from center of bottom face to the top [Hx, Hy, Hz]

		:param h: [Hx, Hy, Hz]
		"""
		self.__h = h

	@property
	def a(self):
		"""
		Get major axis vector of ellipse orthogonal to H [Ax, Ay, Az]

		:return: list [Ax, Ay, Az]
		"""
		return self.__a

	@a.setter
	def a(self, a: list):
		"""
		Set major axis vector of ellipse orthogonal to H [Ax, Ay, Az]

		:param a: [Ax, Ay, Az]
		"""
		self.__a = a

	@property
	def b(self):
		"""
		Get minor axis vector of ellipse orthogonal to H and A [Bx, By, Bz]

		:return: list [Bx, By, Bz]
		"""
		return self.__b

	@b.setter
	def b(self, b: list):
		"""
		Set minor axis vector of ellipse orthogonal to H and A [Bx, By, Bz]

		:param b: [Bx, By, Bz]
		"""
		self.__b = b

	@property
	def get_center(self):
		"""
		Get elliptical cylinder center as half height vector

		:return: list [xc, yc, zc]
		"""
		hx = self.h[0]
		hy = self.h[1]
		hz = self.h[2]

		return sum([self.xyz0, [hx/2, hy/2, hz/2]], axis=0)

	@property
	def get_len_h(self):
		"""
		Get length of height vector

		:return: float length of height
		"""
		return la.norm(self.h)

	@property
	def get_len_a(self):
		"""
		Get semi-major axis length (vector A)

		:return: float length of major axis A
		"""
		return la.norm(self.a)

	@property
	def get_len_b(self):
		"""
		Get semi-minor axis length (vector B)

		:return: float length of minor axis B
		"""
		return la.norm(self.b)

	@property
	def get_bottom_area(self):
		"""
		Get bottom face area (ellipse) of cylinder as S = pi * a * b

		:return: float bottom face area
		"""
		return PI * self.get_len_a * self.get_len_b

	@property
	def get_side_area(self):
		"""
		Get side face surface area as 4 * a * h * E(m), where
		E(m) - complete elliptic integral of the second kind and m equal to
		(a^2 - b^2)/a^2 (eccentricity squared)

		:return: float side face area
		"""
		a = self.get_len_a
		a2 = power(a, 2)
		b = self.get_len_b
		b2 = power(b, 2)
		h = self.get_len_h
		return 4 * a * h * ellipe((a2 - b2)/a2)

	@property
	def get_full_area(self):
		"""
		Get full surface area as sum of 2 bottom areas and 1 side area

		:return: float full surface area
		"""
		return 2*self.get_bottom_area + self.get_side_area

	@property
	def get_volume(self):
		"""
		Get volume

		:return: float volume
		"""
		return self.get_bottom_area * self.get_len_h

	def print_properties(self):
		prefix = f"REC '{self.name}' sn={self.sn}"
		print(f"{prefix} material name:", self.material.name)
		print(f"{prefix} xyz0:", self.xyz0)
		print(f"{prefix} center:", self.get_center)
		print(f"{prefix} height vector:", self.h)
		print(f"{prefix} height vector length:", self.get_len_h)
		print(f"{prefix} semi-major axis vector of ellipse orthogonal to H:", self.a)
		print(f"{prefix} length of semi-major axis vector A:", self.get_len_a)
		print(
			f"{prefix} semi-minor axis vector of ellipse orthogonal to H and A:", self.b)
		print(f"{prefix} length of semi-minor axis vector B:", self.get_len_b)
		print(f"{prefix} bottom area:", self.get_bottom_area)
		print(f"{prefix} side area:", self.get_side_area)
		print(f"{prefix} full area:", self.get_full_area)
		print(f"{prefix} volume:", self.get_volume)
		print(f"{prefix} trn:", self.trn)

	def phits_print(self):
		"""
		Print PHITS surface definition

		:return: string with PHITS surface definition
		"""
		xyz0 = " ".join(str(i) for i in self.xyz0)
		h = " ".join(str(i) for i in self.h)
		a = " ".join(str(i) for i in self.a)
		b = " ".join(str(i) for i in self.b)
		txt = \
			f"    {self.sn} {self.trn}  " + \
			f"{self.symbol}  {xyz0}  {h}  {a}  {b}" + \
			f" $ name: '{self.name}' " + \
			"(elliptical cylinder) " + \
			"[x0 y0 z0] [Hx Hy Hz] [Ax Ay Az] [Bx By Bz]"

		if self.trn != "":
			txt += f" with tr{self.trn}"
		return txt

	def draw(self, opacity: float = None, label_base=False, label_center=False):
		"""
		Draw surface using vpython

		:param opacity: set surface opacity, where 1.0 - fully visible
		:param label_base: if True create label for object base
		:param label_center: if True create label for object center
		:return: vpython.cylinder object
		"""
		if opacity is None:
			pass
		else:
			self.opacity = opacity

		length = self.get_len_h
		width = self.get_len_a * 2
		height = self.get_len_b * 2

		direction = vector(self.h[0], self.h[1], self.h[2])

		el_cyl = vpython.cylinder(
			pos=vector(self.x0, self.y0, self.z0),
			color=self.color, opacity=self.opacity,
			size=vector(length, width, height), axis=direction)

		lbl_c, lbl_b = None, None
		txt = f"{self.symbol} '{self.name}' sn: {self.sn}\n"
		if label_center:
			xc = notation(self.get_center[0])
			yc = notation(self.get_center[1])
			zc = notation(self.get_center[2])

			txt_c = txt + f"center: ({xc}, {yc}, {zc})"
			lbl_c = vpython.label(
				font="monospace", box=False, opacity=0.5, border=6, space=0,
				pos=vector(self.get_center[0], self.get_center[1], self.get_center[2]),
				text=txt_c, height=14,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random())

		if label_base:
			xb = notation(el_cyl.pos.x)
			yb = notation(el_cyl.pos.y)
			zb = notation(el_cyl.pos.z)

			txt_b = txt + f"base: ({xb}, {yb}, {zb})"
			lbl_b = vpython.label(
				font="monospace", box=False, opacity=0.5, border=6, space=0,
				pos=el_cyl.pos,
				text=txt_b, height=14,
				# for random directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random())
		return el_cyl, lbl_c, lbl_b


class WED(Surface):
	symbol = "WED"

	def __init__(
			self, xyz0: list = None,
			a: list = None, b: list = None, h: list = None,
			name="WED", trn="", material=MAT_WATER):
		"""
		Define WED (wedge) surface, note that only right triangle can be used as
		bottom

		:param xyz0: base vertex coordinate [x0, y0, z0]
		:param a: vector to first side of triangle [Ax, Ay, Az]
		:param b: vector to second side of triangle [Bx, By, Bz]
		:param h: height vector from base vertex [Hx, Hy, Hz]
		:param name: name for object
		:param trn: transform number, specifies the number n of TRn
		:param material: material associated with surface
		"""
		# Default values
		if xyz0 is None:
			xyz0 = [0.0, 0.0, 0.0]
		if a is None:
			a = [1.0, 0.0, 0.0]
		if b is None:
			b = [0.0, 0.0, 1.0]
		if h is None:
			h = [0.0, 1.0, 0.0]

		self.xyz0 = xyz0
		self.a = a
		self.b = b
		self.h = h

		Surface.__init__(self, name, trn, material)
		created_surfaces.append(self)

	@property
	def xyz0(self):
		"""
		Get list of base vertex coordinate

		:return: List [x0, y0, z0]
		"""
		return self.__xyz0

	@xyz0.setter
	def xyz0(self, xyz0: list):
		"""
		Set list of base vertex coordinate

		:param xyz0: list [x0, y0, z0]
		"""
		self.__xyz0 = xyz0

	@property
	def x0(self):
		"""
		Get x component of base vertex coordinate

		:return: Float x0
		"""
		return self.__xyz0[0]

	@x0.setter
	def x0(self, x0: float):
		"""
		Set x component of base vertex coordinate

		:param x0: Float x0
		"""
		self.__xyz0[0] = x0

	@property
	def y0(self):
		"""
		Get y component of base vertex coordinate

		:return: Float y0
		"""
		return self.__xyz0[1]

	@y0.setter
	def y0(self, y0: float):
		"""
		Set y component of base vertex coordinate

		:param y0: Float y0
		"""
		self.__xyz0[1] = y0

	@property
	def z0(self):
		"""
		Get z component of base vertex coordinate

		:return: float z0
		"""
		return self.__xyz0[2]

	@z0.setter
	def z0(self, z0: float):
		"""
		Set z component of base vertex coordinate

		:param z0: float z0
		"""
		self.__xyz0[2] = z0

	@property
	def a(self):
		"""
		Get vector to first side of triangle

		:return: list A [Ax, Ay, Az]
		"""
		return self.__a

	@a.setter
	def a(self, a: list):
		"""
		Set vector to first side of triangle

		:param a: list A [Ax, Ay, Az]
		"""
		self.__a = a

	@property
	def b(self):
		"""
		Get vector to second side of triangle

		:return: list B [Bx, By, Bz]
		"""
		return self.__b

	@b.setter
	def b(self, b: list):
		"""
		Set vector to second side of triangle

		:param b: list B [Bx, By, Bz]
		"""
		self.__b = b

	@property
	def h(self):
		"""
		Get height vector from base vertex

		:return: list H [Hx, Hy, Hz]
		"""
		return self.__h

	@h.setter
	def h(self, h: list):
		"""
		Set height vector from base vertex

		:param h: list H [Hx, Hy, Hz]
		"""
		self.__h = h

	@property
	def get_center(self):
		"""
		Get centroid of wedge as sum of vectors xyz0 AB third and half H vector

		:return: list [xc, yc, zc]
		"""
		sum_ab_third = sum([self.a, self.b], axis=0)/3
		return sum(
			[self.xyz0, sum_ab_third, [self.h[0]/2, self.h[1]/2, self.h[2]/2]],
			axis=0)

	@property
	def get_len_a(self):
		"""
		Get length of wedge A vector (along x)

		:return: float length of wedge A vector
		"""
		return la.norm(self.a)

	@property
	def get_len_b(self):
		"""
		Get length of wedge B vector (along y)

		:return: float length of wedge B vector
		"""
		return la.norm(self.b)

	@property
	def get_len_h(self):
		"""
		Get length of height vector (along z)

		:return: float length of height vector
		"""
		return la.norm(self.h)

	@property
	def get_len_c(self):
		"""
		Get length of hypotenuse C of AB triangle,
		where C = sqrt(|A|^2 + |B|^2)

		:return: float length of hypotenuse C
		"""
		a2 = power(self.get_len_a, 2)
		b2 = power(self.get_len_b, 2)

		return sqrt(a2 + b2)

	@property
	def get_volume(self):
		"""
		Get volume of defined wedge as half of absolute value of mixed product
		of vectors A, B, H

		:return: volume of defined wedge
		"""
		return abs(inner(cross(self.a, self.b), self.h))/2

	@property
	def get_ab_area(self):
		"""
		Get AB base vertex triangle surface area as half length of cross product
		of A and B vectors

		:return: AB base vertex triangle surface area
		"""
		return la.norm(cross(self.a, self.b))/2

	@property
	def get_ah_area(self):
		"""
		Get AH side rectangle surface area as length of cross product
		of A and H vectors

		:return: AH side rectangle surface area
		"""
		return la.norm(cross(self.a, self.h))

	@property
	def get_bh_area(self):
		"""
		Get BH side rectangle surface area as length of cross product
		of B and H vectors

		:return: BH side rectangle surface area
		"""
		return la.norm(cross(self.b, self.h))

	@property
	def get_ch_area(self):
		"""
		Get CH side rectangle surface area (opposite to H)
		as product of H length and C, where C = sqrt(|A|^2 + |B|^2)

		:return: CH face rectangle surface area
		"""

		return self.get_len_h * self.get_len_c

	@property
	def get_full_area(self):
		"""
		Get full wedge surface area

		:return: full wedge surface area
		"""
		return \
			2*self.get_ab_area + \
			self.get_ah_area + self.get_bh_area + self.get_ch_area

	def print_properties(self):
		prefix = f"WED '{self.name}' sn={self.sn}"
		print(f"{prefix} material name:", self.material.name)
		print(f"{prefix} xyz0:", self.xyz0)
		print(f"{prefix} vector A to first side of triangle:", self.a)
		print(f"{prefix} vector A length:", self.get_len_a)
		print(f"{prefix} vector B to second side of triangle:", self.b)
		print(f"{prefix} vector B length:", self.get_len_b)
		print(f"{prefix} height vector H from base vertex:", self.h)
		print(f"{prefix} length of height vector H:", self.get_len_h)
		print(f"{prefix} center:", self.get_center)
		print(f"{prefix} volume:", self.get_volume)
		print(f"{prefix} AB base vertex triangle surface area:", self.get_ab_area)
		print(f"{prefix} AH side rectangle surface area:", self.get_ah_area)
		print(f"{prefix} BH side rectangle surface area:", self.get_bh_area)
		print(f"{prefix} full area:", self.get_full_area)

	def phits_print(self):
		"""
		Print PHITS surface definition

		:return: string with PHITS surface definition
		"""
		xyz0 = " ".join(str(i) for i in self.xyz0)
		a = " ".join(str(i) for i in self.a)
		b = " ".join(str(i) for i in self.b)
		h = " ".join(str(i) for i in self.h)

		txt = \
			f"    {self.sn} {self.trn}  " + \
			f"{self.symbol}  {xyz0}  {a}  {b}  {h}" + \
			f" $ name: '{self.name}' " + \
			"(wedge) [x0 y0 z0] [Ax Ay Az] [Bx By Bz] [Hx Hy Hz]"

		if self.trn != "":
			txt += f" with tr{self.trn}"
		return txt

	def draw(self, opacity: float = None, label_base=False, label_center=False):
		"""
		Draw surface using vpython

		:param opacity: set surface opacity, where 1.0 - fully visible
		:param label_base: if True create label for object base
		:param label_center: if True create label for object center
		:return: vpython.cylinder object
		"""
		if opacity is None:
			opacity = self.opacity
		else:
			pass

		color = self.color

		x0, y0, z0 = self.x0, self.y0, self.z0

		ax, ay, az = self.a[0], self.a[1], self.a[2]
		bx, by, bz = self.b[0], self.b[1], self.b[2]
		hx, hy, hz = self.h[0], self.h[1], self.h[2]

		o = vertex(pos=vector(x0, y0, z0))  # Base vertex
		o_prime = vertex(pos=vector(x0+hx, y0+hy, z0+hz))  # top vertex

		a = vertex(pos=vector(x0+ax, y0+ay, z0+az))
		a_prime = vertex(pos=vector(a.pos.x+hx, a.pos.y+hy, a.pos.z+hz))

		b = vertex(pos=vector(x0+bx, y0+by, z0+bz))
		b_prime = vertex(pos=vector(b.pos.x+hx, b.pos.y+hy, b.pos.z+hz))

		# Defines colors and opacity to vertexes
		for v in [o, o_prime, a, a_prime, b, b_prime]:
			v.color = color
			v.opacity = opacity

		base_tr = vpython.triangle(vs=[o, a, b])
		top_tr = vpython.triangle(vs=[o_prime, a_prime, b_prime])

		side_ah = vpython.quad(vs=[o, a, a_prime, o_prime])
		side_bh = vpython.quad(vs=[o, b, b_prime, o_prime])
		side3 = vpython.quad(vs=[a, a_prime, b_prime, b])

		wedge = vpython.compound([base_tr, top_tr, side_ah, side_bh, side3])

		lbl_c, lbl_b = None, None
		txt = f"{self.symbol} '{self.name}' sn: {self.sn}\n"
		if label_center:
			xc = notation(self.get_center[0])
			yc = notation(self.get_center[1])
			zc = notation(self.get_center[2])

			txt_c = txt + f"center: ({xc}, {yc}, {zc})"
			lbl_c = vpython.label(
				font="monospace", box=False, opacity=0.5, border=6, space=0,
				pos=vector(self.get_center[0], self.get_center[1], self.get_center[2]),
				text=txt_c, height=14,
				# for opposite directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random())

		if label_base:
			xb = notation(o.pos.x)
			yb = notation(o.pos.y)
			zb = notation(o.pos.z)

			txt_b = txt + f"base: ({xb}, {yb}, {zb})"
			lbl_b = vpython.label(
				font="monospace", box=False, opacity=0.5, border=6, space=0,
				pos=o.pos,
				text=txt_b, height=14,
				# for random directions
				xoffset=(-1) ** self.sn * 20 * random.random(),
				yoffset=(-1) ** self.sn * 100 * random.random())
		return wedge, lbl_c, lbl_b


class HEX:
	# TODO: Hexagonal prism
	pass


class ELL:
	# TODO: Ellipsoid of revolution
	pass


if __name__ == "__main__":
	print(
		"--- Welcome to FitsGeo! ---\n" +
		"This is a module for FitsGeo!\nImport FitsGeo to use.")
	list_all_surfaces()
