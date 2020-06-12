.. highlight:: python

============
User's Guide
============

.. rubric:: Guide covers almost all features and FitsGeo capabilities with examples

The guide is intended for users who are familiar with the PHITS code. Therefore, many nuances of working with PHITS go beyond the scope of the FitsGeo documentation. To clarify missing please visit first `PHIST manual <https://phits.jaea.go.jp/rireki-manuale.html>`_. 

Implemented features
====================
.. rubric:: Section describes all current implemented modules with their capabilities

Currently, FitsGeo package have ``material``, ``const``, ``surface``, ``cell`` and ``export`` modules. Each of them responsable for certain tasks:

* ``material`` handles material definitions, materials can be set from pre-defined databases or manually (see `Material module <user_guide.html#id1>`_ section)
* ``const`` consists of constants used in FitsGeo: colors for surfaces as VPython vectors and ANGEL (builtin visualization in PHITS) colors associated to these colors (in Python dictionary), $\pi$ definition from NumPy as math constant (see `Const module <user_guide.html#id2>`_ section)
* ``surface`` consists of classes for defining surfaces (see `Surface module <user_guide.html#id4>`_ section)
* ``cell`` consists of class to define cells (more concrete volumes as combinations of surfaces, see `Cell module <user_guide.html#id5>`_ section)
* ``export`` provides functionality for export of all defined objects to PHITS understandable format (other MC codes can be added in future releases, see `Export module <user_guide.html#id6>`_ section)
  
More modules for other sections of PHITS input will come soon.

Material module
---------------

At first, user need to define materials for future geometry. Material module have a ``Material`` class, which defines materials for PHTIS [ Material ] section. Parameters, which can be provided in the ``Material`` class:

* ``elements: list`` --- elements in [[A1, Z1, Q1], [A2, Z2, Q2], ...] format, where A --- mass number, Z --- atomic number, Q --- quantity of ratio (``"atomic"`` or ``"mass"``)
* ``name: str`` --- name for material object
* ``ratio_type: str = "atomic"`` --- type of ratio: ``"atomic"`` (by default) or ``"mass"``
* ``gas: bool = False`` --- ``True`` if gas (``False`` by default)
* ``color: str`` --- color for material for PHITS with ANGEL visualization
* ``matn: int`` --- material object number, automatically set after every new material initialization, but can be changed manually after initialization

Any material can be defined in two ways:

1. Using pre-defined databases
2. Manually

In first way, user only need to provide name of desirable material and color (optionally)::

	water = fitsgeo.Material.database("MAT_WATER", color="blue") 

All available materials listed in the `Pre-defined Materials <material.html>`_ section.

Following second way, user need to provide ``elements`` list and other parameters from the above list if needed::

	water = fitsgeo.Material([[0, 1, 2], [0, 8, 1]], name="Water", color="blue")

In this particular example we don't need to additionally set ``ratio_type`` and ``gas`` parameters, because these parameters' default values fit to our needs. But if we want this to be water vapor::

	water_vapor = fitsgeo.Material([[0, 1, 2], [0, 8, 1]], name="Water Vapor", gas=True, color="pastelblue")

Gas flag must be provided.

All colors defined through ``color`` parameter and must be taken from ``ANGEL_COLORS`` as keys (see next section).

If user not provides any materials for surfaces or cells, ``MAT_WATER`` material is used by default for surfaces and cells. This material, as well as materials for void and "outer world" are pre-defined in ``material`` module as constants::

	# Pre-defined materials as constants for default surface material
	MAT_OUTER = Material([], matn=-1)  # special material for outer world
	MAT_VOID = Material([], matn=0)  # special material for void
	MAT_WATER = Material.database("MAT_WATER", color="blue")

These materials can be invoked directly from ``fitsgeo``::

	fitsgeo.MAT_OUTER
	fitsgeo.MAT_VOID
	fitsgeo.MAT_WATER

All defined materials should be passed as parameters in surfaces and cells objects. Otherwise, default ``MAT_WATER`` material will be used during export.

*Why do we need to pass materials to surface objects and not only to cells?*

	**The answer is:** if user not defines any cells, [ Cell ] section will be created automatically from all available surfaces (except planes). In this case, FitsGeo uses materials provided through surface objects.

Material module have a global ``created_materials`` value, this value contains all defined materials in a list. This way, all materials could be easily accessed from this list and modified, if needed.

Const module
------------

Const module mainly provides color constants: VPython vectors for VPython surface visualization. ``ANGEL_COLORS`` is a Python dictionary in ``const`` module, this dictionary provides color matching of ANGEL colors to those colors defined through VPython vectors. In that way, we will have similar colors both in FitsGeo and in PHITS visualization based on ANGEL. Table below shows all available for visualization colors.

.. toggle-header::
	:header: **Table: Dictionary With ANGEL and VPython Vector Colors Match**

		.. tabularcolumns:: |p{2.5cm}|p{4cm}|p{3cm}|

		.. table:: **Dictionary With ANGEL and VPython Vector Colors Match**
			:class: longtable

			+---------------+------------------+-----------------+
			| ANGEL         | constant in      | RGB             |
			| color         | ``const`` module |                 |
			+===============+==================+=================+
			| white         | ``WHITE``        | (255, 255, 255) |
			+---------------+------------------+-----------------+
			| lightgray     | ``LIGHTGRAY``    | (211, 211, 211) |
			+---------------+------------------+-----------------+
			| gray          | ``GRAY``         | (169, 169, 169) |
			+---------------+------------------+-----------------+
			| darkgray      | ``DARKGRAY``     | (128, 128, 128) |
			+---------------+------------------+-----------------+
			| matblack      | ``DIMGRAY``      | (105, 105, 105) |
			+---------------+------------------+-----------------+
			| black         | ``BLACK``        | (0, 0, 0)       |
			+---------------+------------------+-----------------+
			| darkred       | ``DARKRED``      | (139, 0, 0)     |
			+---------------+------------------+-----------------+
			| red           | ``RED``          | (255, 0, 0)     |
			+---------------+------------------+-----------------+
			| pink          | ``PINK``         | (219, 112, 147) |
			+---------------+------------------+-----------------+
			| pastelpink    | ``NAVAJOWHITE``  | (255, 222, 173) |
			+---------------+------------------+-----------------+
			| orange        | ``DARKORANGE``   | (255, 140, 0)   |
			+---------------+------------------+-----------------+
			| brown         | ``SADDLEBROWN``  | (139, 69, 19)   |
			+---------------+------------------+-----------------+
			| darkbrown     | ``DARKBROWN``    | (51, 25, 0)     |
			+---------------+------------------+-----------------+
			| pastelbrown   | ``PASTELBROWN``  | (131, 105, 83)  |
			+---------------+------------------+-----------------+
			| orangeyellow  | ``GOLD``         | (255, 215, 0)   |
			+---------------+------------------+-----------------+
			| camel         | ``OLIVE``        | (128, 128, 0)   |
			+---------------+------------------+-----------------+
			| pastelyellow  | ``PASTELYELLOW`` | (255, 255, 153) |
			+---------------+------------------+-----------------+
			| yellow        | ``YELLOW``       | (255, 255, 0)   |
			+---------------+------------------+-----------------+
			| pastelgreen   | ``PASTELGREEN``  | (204, 255, 153) |
			+---------------+------------------+-----------------+
			| yellowgreen   | ``YELLOWGREEN``  | (178, 255, 102) |
			+---------------+------------------+-----------------+
			| green         | ``GREEN``        | (0, 128, 0)     |
			+---------------+------------------+-----------------+
			| darkgreen     | ``DARKGREEN``    | (0, 102, 0)     |
			+---------------+------------------+-----------------+
			| mossgreen     | ``MOSSGREEN``    | (0, 51, 0)      |
			+---------------+------------------+-----------------+
			| bluegreen     | ``BLUEGREEN``    | (0, 255, 128)   |
			+---------------+------------------+-----------------+
			| pastelcyan    | ``PASTELCYAN``   | (153, 255, 255) |
			+---------------+------------------+-----------------+
			| pastelblue    | ``PASTELBLUE``   | (153, 204, 255) |
			+---------------+------------------+-----------------+
			| cyan          | ``CYAN``         | (0, 255, 255)   |
			+---------------+------------------+-----------------+
			| cyanblue      | ``CYANBLUE``     | (0, 102, 102)   |
			+---------------+------------------+-----------------+
			| blue          | ``BLUE``         | (0, 0, 255)     |
			+---------------+------------------+-----------------+
			| violet        | ``DARKVIOLET``   | (238, 130, 238) |
			+---------------+------------------+-----------------+
			| purple        | ``PURPLE``       | (128, 0, 128)   |
			+---------------+------------------+-----------------+
			| magenta       | ``MAGENTA``      | (255, 0, 255)   |
			+---------------+------------------+-----------------+
			| winered       | ``MAROON``       | (128, 0, 0)     |
			+---------------+------------------+-----------------+
			| pastelmagenta | ``VIOLET``       | (238, 130, 238) |
			+---------------+------------------+-----------------+
			| pastelpurple  | ``INDIGO``       | (75, 0, 130)    |
			+---------------+------------------+-----------------+
			| pastelviolet  | ``PASTELVIOLET`` | (204, 153, 255) |
			+---------------+------------------+-----------------+

These colors in **ANGEL color** column passed as ``color`` parameter for material objects (see `Material module <user_guide.html#id1>`_ section).

Function ``rgb_to_vector`` in ``const`` module translates RGB colors to VPython vectors::

	VIOLET = rgb_to_vector(238, 130, 238)

This returns ``vpython.vector`` object as ``VIOLET`` color constant, which can be used in VPython visualization. Some more pre-defined colors can be found in this module.

.. toggle-header::
	:header: **Table: Pre-defined VPython Vector Colors**

		::

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

Color for surfaces is set automatically from material. Although, it can be set just before ``draw()`` method execution as::

	box = fitsgeo.BOX()  # BOX surface, by default it has MAT_WATER material as parameter, which color is "blue"

	# If we want to change color
	box.color = fitsgeo.YELLOWGREEN

	box.draw()  # This will be YELLOWGREEN, not BLUE

Also, in this module ``PI`` constant defined from NumPy. Another math constants may be defined here in the future.

Surface module
--------------

Firstly, ``surface`` module have ``list_all_surfaces`` function which prints all implemented surfaces::

	fitsgeo.list_all_surfaces()

Function ``create_scene()`` creates default VPython canvas with some settings, which can be specified providing additional parameters to function:

* ``axes: bool = True`` --- add axes to scene (``True`` by default)
* ``width: int = 1200`` --- set width for visualization window in browser in pixels (``1200`` pixels by default)
* ``height: int = 800`` --- set height for visualization window in browser in pixels (``800`` pixels by default)
* ``resizable: bool = True`` --- makes window resizable or not (``True`` by default)
* ``ax_length: float = 2.0`` --- axis length, better set as maximum size of whole geometry (``2.0`` by default)
* ``ax_opacity: float = 0.2`` --- set axis opacity, where ``1.0`` is fully visible and ``0.0`` --- fully transparent (``0.2`` by default)
* ``background: vpython.vector = GRAY_SCALE[1]`` --- set background color for scene (by default pre-defined ``LIGHTGRAY`` color from ``const`` module)
* ``return`` --- ``vpython.canvas`` object and axes if ``axes=True``

To create empty scene::

	scene = fitsgeo.create_scene()

.. figure:: images/empty_scene.png
	:align: center
	:figclass: align-center

	**Empty scene with axes**

After that, every created surface will be drawn on this scene. Scene automatically opens in browser. For view control:

* **zoom:** mouse wheel
* **rotate:** right mouse button (ctrl+left mouse button)
* **pan:** shift+left mouse button

Scene is a 3D VPython canvas, take a look at `VPython docs <https://www.glowscript.org/docs/VPythonDocs/canvas.html>`_ for more detailed explanation.

To create surfaces, one must create object from corresponding surface class. Table below shows which Python classes for PHITS surfaces are currently implemented. 

.. toggle-header::
	:header: **Table: PHITS Surfaces --- FitsGeo Classes**

		.. tabularcolumns:: |p{3cm}|p{2cm}|p{7cm}|p{2cm}|

		.. table:: **PHITS Surfaces --- FitsGeo Classes**
			:class: longtable

			+----------------------+------------+--------------------------+---------------+
			| PHITS surface symbol |  Type      |      Explanation         | Class         |
			|                      |            |                          |               |
			+======================+============+==========================+===============+
			| P                    |            | multi-purpose            |               |
			+----------------------+            +--------------------------+               |
			| PX                   |            | vertical with X-axis     |               |
			+----------------------+            +--------------------------+               |
			| PY                   | planes     | vertical with Y-axis     |      ``P``    |
			+----------------------+            +--------------------------+               |
			| PZ                   |            | vertical with Z-axis     |               |
			+----------------------+------------+--------------------------+---------------+
			| SO                   |            | origin is center         |               |
			+----------------------+            +--------------------------+               |
			| S                    |            | multi-purpose            |               |
			+----------------------+            +--------------------------+               |
			| SX                   | sphere     | center on X-axis         |               |
			+----------------------+            +--------------------------+               |
			| SY                   |            | center on Y-axis         |     ``SPH``   |
			+----------------------+            +--------------------------+               |
			| SZ                   |            | center on Z-axis         |               |
			+----------------------+------------+--------------------------+               |
			| SPH                  | macro body | same as multi-purpose    |               |
			+----------------------+------------+--------------------------+---------------+
			| BOX                  | macro body | optional BOX             |     ``BOX``   |
			+----------------------+------------+--------------------------+---------------+
			|                      | macro body | rectangular solid similar|               |
			| RPP                  |            | to BOX, but each surface |               |
			|                      |            | is vertical with         |     ``RPP``   |
			|                      |            | x, y, z axes             |               |
			+----------------------+------------+--------------------------+---------------+
			| RCC                  | macro body | cylinder                 |     ``RCC``   |
			|                      |            |                          |               |
			+----------------------+------------+--------------------------+---------------+
			| TRC                  | macro body | truncated right-angle    |     ``TRC``   |
			|                      |            | cone                     |               |
			+----------------------+------------+--------------------------+---------------+
			| TX                   |            | parallel with X-axis     |               |
			+----------------------+            +--------------------------+               |
			| TY                   | ellipse    | parallel with Y-axis     |      ``T``    |
			+----------------------+ torus      +--------------------------+               |
			| TZ                   |            | parallel with Z-axis     |               |
			+----------------------+------------+--------------------------+---------------+
			| REC                  | macro body | right elliptical cylinder|     ``REC``   |
			+----------------------+------------+--------------------------+---------------+
			| WED                  | macro body | wedge                    |     ``WED``   |
			+----------------------+------------+--------------------------+---------------+

Therefore, from each class surface objects can be created. For example, to create box surface object of ``BOX`` class::

	box = fitsgeo.BOX([0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], name="Box")

This line creates box object as BOX class at $P (0, 0, 0)$ (base point) coordinate and $\vec{A} \langle1, 0, 0\rangle$, $\vec{B} \langle0, 1, 0\rangle$, $\vec{C} \langle0, 0, 1\rangle$ vectors from base point with "Box" name.

All classes have default parameters, so, if one needs exactly the object above it can be created simply as::

	box = fitsgeo.BOX()

Other objects can be created in the same manner. All parameters for all implemented classes listed in the table below.

.. toggle-header::
	:header: **Table: Parameters Of Surface Classes**

		.. tabularcolumns:: |p{3cm}|p{3cm}|p{9cm}|

		.. table:: **Parameters Of Surface Classes**
			:class: longtable

			+----------------------+----------------+---------------------------------------------+
			| Class                | Parameter      | Explanation                                 |
			+======================+================+=============================================+
			|                      | ``a: float``   |                                             |
			|                      +----------------+                                             |
			|                      | ``b: float``   |                                             |
			|                      +----------------+ parameters in $Ax + By + Cz - D = 0$        |
			|    ``P``             | ``c: float``   | equation                                    |
			|                      +----------------+                                             |
			|                      | ``d: float``   |                                             |
			|                      +----------------+---------------------------------------------+
			|                      | ``vert: str``  | axis to which plane                         |
			|                      |                | is vertical (``"x"``, ``"y"``, ``"z"``)     |
			+----------------------+----------------+---------------------------------------------+
			|                      | ``xyz0: list`` | center coordinate of                        |
			|                      |                | sphere as [x0, y0, z0] list                 |
			|   ``SPH``            +----------------+---------------------------------------------+
			|                      | ``r: float``   | radius of sphere                            |
			+----------------------+----------------+---------------------------------------------+
			|                      | ``xyz0: list`` | base point coordinate                       |
			|                      |                | as [x0, y0, z0] list                        |
			|                      +----------------+---------------------------------------------+
			|   ``BOX``            | ``a: list``    | vector $\vec{A}$ from base point to         |
			|                      |                | first face as [Ax, Ay, Az] list             |
			|                      +----------------+---------------------------------------------+
			|                      | ``b: list``    | vector $\vec{B}$ from base point to second  |
			|                      |                | face as [Bx, By, Bz] list                   |
			|                      +----------------+---------------------------------------------+
			|                      | ``c: list``    | vector $\vec{C}$ from base point to third   |
			|                      |                | face as [Cx, Cy, Cz] list                   |
			+----------------------+----------------+---------------------------------------------+
			|                      | ``x: list``    | list with x min and max components          |
			|                      |                | as [x_min, x_max] list                      |
			|                      +----------------+---------------------------------------------+
			|  ``RPP``             | ``y: list``    | list with y min and max components          |
			|                      |                | as [y_min, y_max] list                      |
			|                      +----------------+---------------------------------------------+
			|                      | ``z: list``    | list with z min and max components          |
			|                      |                | as [z_min, z_max] list                      |
			+----------------------+----------------+---------------------------------------------+
			|                      | ``xyz0: list`` | center coordinate of bottom face            |
			|                      |                | as [x0, y0, z0] list                        |
			|                      +----------------+---------------------------------------------+
			|  ``RCC``             | ``h: list``    | $\vec{H}$ from the bottom face to the top   |
			|                      |                | as [Hx, Hy, Hz] list                        |
			|                      +----------------+---------------------------------------------+
			|                      | ``r: float``   | radius of bottom face                       |
			+----------------------+----------------+---------------------------------------------+
			|                      | ``xyz0: list`` | center coordinate of cone bottom            |
			|                      |                | face as [x0, y0, z0] list                   |
			|                      +----------------+---------------------------------------------+
			|                      | ``h: list``    | height $\vec{H}$ from center of bottom face |
			|  ``TRC``             |                | to the top face as [Hx, Hy, Hz] list        |
			|                      +----------------+---------------------------------------------+
			|                      | ``r_1: float`` | radius of bottom face of                    |
			|                      |                | truncated cone                              |
			|                      +----------------+---------------------------------------------+
			|                      | ``r_2: float`` | radius of top face of truncated cone        |
			+----------------------+----------------+---------------------------------------------+
			|                      | ``xyz0: list`` | center of the torus                         |
			|                      |                | as [x0, y0, z0] list                        |
			|                      +----------------+---------------------------------------------+
			|                      | ``r: float``   | distance between torus center               |
			|                      |                | (rotational axis) and ellipse center        |
			|                      +----------------+---------------------------------------------+
			|  ``T``               | ``b: float``   | semi-minor axis value                       |
			|                      |                | (ellipse half "height")                     |
			|                      +----------------+---------------------------------------------+
			|                      | ``c: float``   | semi-major axis value                       |
			|                      |                | (ellipse half "width")                      |
			|                      +----------------+---------------------------------------------+
			|                      | ``rot: str``   | rotational axis (``"x"``, ``"y"``, ``"z"``) |
			+----------------------+----------------+---------------------------------------------+
			|                      | ``xyz0: list`` | center coordinate of bottom face            |
			|                      |                | as [x0, y0, z0] list                        |
			|                      +----------------+---------------------------------------------+
			|                      | ``h: list``    | height $\vec{H}$ from center of bottom      |
			|                      |                |                                             |
			|                      |                | face as [Hx, Hy, Hz] list                   |
			|   ``REC``            +----------------+---------------------------------------------+
			|                      | ``a: list``    | semi-major axis $\vec{A}$ of ellipse        |
			|                      |                | orthogonal to $\vec{H}$ as [Ax, Ay, Az] list|
			|                      +----------------+---------------------------------------------+
			|                      | ``b: list``    | semi-minor axis $\vec{B}$ of ellipse        |
			|                      |                | orthogonal to $\vec{H}$ and $\vec{A}$ as    |
			|                      |                | [Bx, By, Bz] list                           |
			+----------------------+----------------+---------------------------------------------+
			|                      | ``xyz0: list`` | base vertex coordinate                      |
			|                      |                | as [x0, y0, z0] list                        |
			|                      +----------------+---------------------------------------------+
			|                      | ``a: list``    | $\vec{A}$ to first side of triangle         |
			|                      |                | as [Ax, Ay, Az] list                        |
			|  ``WED``             +----------------+---------------------------------------------+
			|                      | ``b: list``    | $\vec{B}$ to second side of triangle        |
			|                      |                | as [Bx, By, Bz] list                        |
			|                      +----------------+---------------------------------------------+
			|                      | ``h: list``    | height vector $\vec{H}$ from base vertex    |
			|                      |                | as [Hx, Hy, Hz] list                        |
			+----------------------+----------------+---------------------------------------------+

In addition to listed in the table above parameters, each class have common from ``Surface`` super class parameters/properties:

* ``name: str`` --- name for object, for user convenience, appears in commentaries in PHITS input
* ``trn: str`` --- transform number, specifies the number n of TRn in PHTIS [ Transform ] section (in current version transformations not visualizable)
* ``material: fitsgeo.Material`` --- material associated with surface, object from ``Material`` class, by default is pre-defined ``MAT_WATER`` from ``const`` module
* ``sn: int`` --- surface object number, automatically set after every new surface initialization, but can be changed manually after initialization
* ``color: vpython.vector`` --- ``vpython.vector`` object, which defines color for surface (associated with ANGEL color through ``ANGEL_COLORS`` dictionary from ``const`` module by default), not accessible at initialization
* ``opacity: float`` --- surface opacity during visualization, from ``0.0`` (fully transparent) to ``1.0`` (fully visable), not accessible at initialization, may be changed with ``draw()`` method

Each class have number of getter/setter methods. They define unique for each class properties in addition to parameters from table above: area surfaces, volumes, diameters etc. All methods are listed in the table below.

.. toggle-header::
	:header: **Table: All Methods For Surface Classes**

		.. tabularcolumns:: |p{1cm}|p{5cm}|p{3cm}|p{6cm}|

		.. table:: **All Methods For Surface Classes**
			:class: longtable

			+----------------------+-------------------------+------------------+-----------------------------------------------+
			| Class                | Method                  | Type             | Explanation                                   |
			+======================+=========================+==================+===============================================+
			|                      | ``diameter``            | Getter & Setter  | Get/set sphere diameter (float)               |
			|   ``SPH``            +-------------------------+------------------+-----------------------------------------------+
			|                      | ``volume``              | Getter & Setter  | Get/set sphere volume (float)                 |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``surface_area``        | Getter & Setter  | Get/set full surface area (float)             |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``cross_section``       | Getter & Setter  | Get/set cross section area: circle (float)    |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``circumference``       | Getter & Setter  | Get/set circumference of cross section (float)|
			+----------------------+-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_center``          | Getter           | Get center of ``BOX`` object as [xc, yc, zc]  |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_diagonal``        | Getter           | Get diagonal $\vec{D}$ [xd, yd, zd] as list   |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_diagonal_length`` | Getter           | Get diagonal length $|\vec{D}|$ (float)       |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|     ``BOX``          | ``get_len_a``           | Getter           | Get length of $\vec{A}$ (float)               |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_len_b``           | Getter           | Get length of $\vec{B}$ (float)               |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_len_c``           | Getter           | Get length of $\vec{C}$ (float)               |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_volume``          | Getter           | Get volume of ``BOX`` object (float)          |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_ab_area``         | Getter           | Get $|\vec{A}\times\vec{B}|$ area (float)     |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_ac_area``         | Getter           | Get $|\vec{A}\times\vec{C}|$ area (float)     |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_bc_area``         | Getter           | Get $|\vec{B}\times\vec{C}|$ area (float)     |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_full_area``       | Getter           | Get full surface area (float)                 |
			+----------------------+-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_width``           | Getter           | Get width of ``RPP`` object (float)           |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_height``          | Getter           | Get height of ``RPP`` object (float)          |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|     ``RPP``          | ``get_length``          | Getter           | Get length of ``RPP`` object (float)          |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_center``          | Getter           | Get center as [xc, yc, zc] list               |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_diagonal_length`` | Getter           | Get diagonal length (float)                   |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_volume``          | Getter           | Get volume of ``RPP`` object (float)          |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_wh_area``         | Getter           | Get width $\times$ height face area (float)   |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_wl_area``         | Getter           | Get width $\times$ length face area (float)   |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_hl_area``         | Getter           | Get height $\times$ length face area (float)  |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_full_area``       | Getter           | Get full surface area (float)                 |
			+----------------------+-------------------------+------------------+-----------------------------------------------+
			|                      | ``diameter``            | Getter & Setter  | Get/set bottom/top faces diameter (float)     |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``circumference``       | Getter & Setter  | Get/set bottom/top faces circumference (float)|
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``bottom_area``         | Getter & Setter  | Get/set bottom area of cylinder (float)       |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_center``          | Getter           | Get center of cylinder as [xc, yc, zc] list   |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|     ``RCC``          | ``get_len_h``           | Getter           | Get height length $|\vec{H}|$ (float)         |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_volume``          | Getter           | Get volume of ``RCC`` object (float)          |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_side_area``       | Getter           | Get side surface area (float)                 |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_full_area``       | Getter           | Get full surface area (float)                 |
			+----------------------+-------------------------+------------------+-----------------------------------------------+
			|                      | ``bottom_diameter``     | Getter & Setter  | Get/set bottom face diameter (float)          |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``top_diameter``        | Getter & Setter  | Get/set top face diameter (float)             |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``bottom_circumference``| Getter & Setter  | Get/set bottom face circumference (float)     |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|     ``TRC``          | ``top_circumference``   | Getter & Setter  | Get/set top face circumference (float)        |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``bottom_area``         | Getter & Setter  | Get/set bottom face area (float)              |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``top_area``            | Getter & Setter  | Get/set top face area (float)                 |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_center``          | Getter           | Get center as [xc, yc, zc] list               |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_len_h``           | Getter           | Get height $|\vec{H}|$ (float)                |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_forming``         | Getter           | Get cone forming (float)                      |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_volume``          | Getter           | Get volume of ``TRC`` object (float)          |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_side_area``       | Getter           | Get side surface area (float)                 |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_full_area``       | Getter           | Get full surface area of cone (float)         |
			+----------------------+-------------------------+------------------+-----------------------------------------------+
			|                      | ``circumference``       | Getter & Setter  | Get/set torus circumference (float)           |
			|     ``T``            +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_cross_section``   | Getter           | Get cross section area of torus (float)       |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_full_area``       | Getter           | Get full surface area of torus (float)        |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_volume``          | Getter           | Get volume of torus (float)                   |
			+----------------------+-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_center``          | Getter           | Get center of elliptical cylinder             |
			|                      |                         |                  | as [xc, yc, zc] list                          |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|     ``REC``          | ``get_len_h``           | Getter           | Get height $|\vec{H}|$ (float)                |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_len_a``           | Getter           | Get semi-major axis length $|\vec{A}|$ (float)|
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_len_b``           | Getter           | Get semi-minor axis length $|\vec{B}|$ (float)|
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_bottom_area``     | Getter           | Get bottom (top) face area                    |
			|                      |                         |                  | of elliptical cylinder (float)                |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_side_area``       | Getter           | Get side surface area (float)                 |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_full_area``       | Getter           | Get full surface area (float)                 |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_volume``          | Getter           | Get volume of elliptical cylinder (float)     |
			+----------------------+-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_center``          | Getter           | Get wedge centroid as [xc, yc, zc] list       |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_len_a``           | Getter           | Get $|\vec{A}|$ (float)                       |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_len_b``           | Getter           | Get $|\vec{B}|$ (float)                       |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|     ``WED``          | ``get_len_h``           | Getter           | Get $|\vec{H}|$ (float)                       |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_len_c``           | Getter           | Get $\sqrt{a^2 + b^2}$ (float),               |
			|                      |                         |                  | where a = $|\vec{A}|$, b = $|\vec{B}|$        |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_volume``          | Getter           | Get wedge volume (float)                      |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_ab_area``         | Getter           | Get $|\vec{A}\times\vec{B}|/2$                |
			|                      |                         |                  | bottom/top triangle face area (float)         |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_ah_area``         | Getter           | Get $|\vec{A}\times\vec{H}|$ face area (float)|
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_bh_area``         | Getter           | Get $|\vec{B}\times\vec{H}|$ face area (float)|
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_ch_area``         | Getter           | Get opposite to $\vec{H}$                     |
			|                      |                         |                  | rectangle face area (float)                   |
			|                      +-------------------------+------------------+-----------------------------------------------+
			|                      | ``get_full_area``       | Getter           | Get full surface area (float)                 |
			+----------------------+-------------------------+------------------+-----------------------------------------------+

Each getter method starts with ``get_`` prefix. If method doesn't have this prefix, then method also has setter.

In addition to listed in the table above methods, each class have common methods:

* ``print_properties()`` --- prints all properties of object in console
* ``phits_print()`` --- returns string with PHITS definition of object
* ``draw()`` --- draws VPython representation of defined object on current scene, additional parameters may be provided to this method:

		* ``size: float`` --- defines size of plane (only for ``P`` class)
		* ``opacity: float`` --- defines surface opacity during visualization, from ``0.0`` (fully transparent) to ``1.0`` (fully visible), **note that** if material parameter ``gas=True``, then opacity will be set to ``0.1`` automatically
		* ``label: bool`` --- defines whether to show label (text with some description) on plane surface during visualization or not
		* ``label_center: bool`` --- defines whether to show label of object's center (except planes) during visualization or not
		* ``label_base: bool`` --- defines whether to show label of object's base point (if object has it) during visualization or not

For example, to print all properties of object in console::

	box.print_properties()

To get PHITS definition of object::

	export_line = box.phits_print()
	print(export_line)   # Print definition in console

To draw box object on scene with labels pointing on box's base point and center::

	box.draw(label_base=True, label_center=True)

.. figure:: images/scene_box.png
	:align: center
	:figclass: align-center

	**Box surface drawn on scene with center and base point labels**

To get full surface area of box object::

	area = box.get_full_area

Or, to get volume of box object::

	volume = box.get_volume

To redefine ``xyz0`` parameter of box object::

	box.xyz0 = [1, 2, 3]

To redefine only x component from ``xyz0``::

	box.xyz0[0] = 1

or::

	box.x0 = 1

Similar can be applied to other components and other objects.

In ``SPH`` class all methods represented both as getter and setter methods. This means, that user can define or get any property. For example::

	sphere = fitsgeo.SPH([0, 0, 0], 1)  # Create sphere object from SPH class
	sphere.volume = 1  # Set volume to 1

Last line will make ``r`` (radius) parameter of ``sphere`` correspond to defined volume. Same works for all other methods in ``SPH`` class. And to get value of property::

	volume = sphere.volume  # Get volume of sphere

Similarly, user can redefine radius of sphere according to any other defined property. 

Surface module have a global ``created_surfaces`` value, this value contains all defined surfaces in a list. This way, all surfaces could be easily accessed from this list and modified, or, drawn all together::

	for surface in created_surfaces:
		surface.draw()

This command will draw all created surfaces.

Cell module
-----------

This module provides ``Cell`` class for cells definition. Example of basic cell::

	box_cell = fitsgeo.Cell([-box], name="Box Cell", material=fitsgeo.MAT_WATER))

Parameters in ``Cell`` class:

* ``cell_def: list`` --- list with regions and the Boolean operators, ``" "`` (blank)(AND), ``":"`` (OR), and ``"#"`` (NOT). Parentheses ``"("`` and ``")"`` will be added automatically for regions
* ``name: str = "Cell"`` --- name for cell object
* ``material: fitsgeo.Material = MAT_WATER`` --- material associated with cell
* ``volume: float = None`` --- volume [cm$^3$] of the cell

Cells are defined by treating regions divided by surfaces. Surface classes have overloaded ``"+"`` (``__pos__``) and ``"-"`` (``__neg__``) operators, it is provides capability to define "surface sense" (see `PHITS manual <https://phits.jaea.go.jp/rireki-manuale.html>`_). These operators return surface numbers of surface objects.
Example::

	region1 = [-box]  # Defines negative sense of box object (inner part)
	region2 = [+box]  # Defines positive sense of box object (outer part)

The symbols ``" "`` (blank), ``":"``, and ``"#"`` denote the intersection (AND), union (OR), and complement (NOT), operators, respectively. Let's say that we have multiple objects (``box`` and ``sphere``) and we want to make cell with union of these surfaces::

	import fitsgeo

	fitsgeo.create_scene()

	box = fitsgeo.BOX()  # box surface
	sphere = fitsgeo.SPH()  # sphere surface

	outer_cell = fitsgeo.Cell([+box, ":", +sphere], material=fitsgeo.MAT_OUTER, name="Outer World")  # Define outer world
	cell = fitsgeo.Cell([-box, ":", -sphere], name="Union")  # Define union of objects

	sphere.color = fitsgeo.YELLOW  # Just to make different colors

	# Draw half transparent
	box.draw(opacity=0.5)
	sphere.draw(opacity=0.5)

	fitsgeo.phits_export()  # Export sections

The result on the image below.

.. figure:: images/fitsgeo_union.png
	:align: center
	:figclass: align-center

	**Example of cell definitions**

In the FitsGeo visualization we will always see our surfaces, not cells, but after export of generated sections to PHITS and visualization using ANGEL, this will be like on the image below.

.. figure:: images/cell_union.png
	:align: center
	:figclass: align-center

	**Cell as the Union of box and sphere**

Exported sections to PHITS, as well as the full input file are presented below.

.. toggle-header::
	:header: **Exported from FitsGeo PHITS Sections**

		.. code-block:: none

			[ Material ]
			    mat[1] H 2.0 O 1.0  GAS=0 $ name: 'MAT_WATER'

			[ Mat Name Color ]
			        mat     name    size    color
			        1       {MAT\_WATER}    1.00    blue

			[ Surface ]
			    1   BOX  0.0 0.0 0.0  1.0 0.0 0.0  0.0 1.0 0.0  0.0 0.0 1.0 $ name: 'BOX' (box, all angles are 90deg) [x0 y0 z0] [Ax Ay Az] [Bx By Bz] [Cx Cy Cz]
			    2   SPH  0.0 0.0 0.0  1.0 $ name: 'SPH' (sphere) x0 y0 z0 R

			[ Cell ]
			    1 -1  (1):(2) $ name: 'Outer World' 

			    3 1  -1.0  (-1):(-2)   $ name: 'Union' 

.. toggle-header::
	:header: **Full PHITS Input File**

		.. code-block:: none

			[ Parameters ]
				icntl = 11		# (D=0) 3:ECH 5:ALL VOID 6:SRC 7,8:GSH 11:DSH 12:DUMP

			[ Source ]
				s-type = 2		# mono-energetic rectangular source
				e0 = 1			# energy of beam [MeV]
				proj = proton	# kind of incident particle

			[ Material ]
			    mat[1] H 2.0 O 1.0  GAS=0 $ name: 'MAT_WATER'

			[ Mat Name Color ]
			        mat     name    size    color
			        1       {MAT\_WATER}    1.00    blue

			[ Surface ]
			    1   BOX  0.0 0.0 0.0  1.0 0.0 0.0  0.0 1.0 0.0  0.0 0.0 1.0 $ name: 'BOX' (box, all angles are 90deg) [x0 y0 z0] [Ax Ay Az] [Bx By Bz] [Cx Cy Cz]
			    2   SPH  0.0 0.0 0.0  1.0 $ name: 'SPH' (sphere) x0 y0 z0 R

			[ Cell ]
			    1 -1  (1):(2) $ name: 'Outer World' 

			    3 1  -1.0  (-1):(-2)   $ name: 'Union' 

			[ T-3Dshow ]
				title = Geometry 3D
				x0 = 0
				y0 = 0
				z0 = 0

				w-wdt = 3
				w-hgt = 3
				w-dst = 10

				w-mnw = 400			# Number of meshes in horizontal direction.
				w-mnh = 400			# Number of meshes in vertical direction.
				w-ang = 0

				e-the = -45
				e-phi = 24
				e-dst = 100

				l-the = 80
				l-phi = 140
				l-dst = 200*100

				file = example1_3D
				output = 3			# (D=3) Region boundary + color
				width = 0.5			# (D=0.5) The option defines the line thickness.
				epsout = 1

			[ E n d ]

Or, we can define cells as::

	import fitsgeo

	fitsgeo.create_scene()

	box = fitsgeo.BOX()
	sphere = fitsgeo.SPH()


	cell_box = fitsgeo.Cell([-box + +sphere], name="Intersection")  # Intersection of inner part of box and outer part of sphere
	cell_sphere = fitsgeo.Cell([-sphere], name="Inner Sphere")  # Inner part of sphere

	sphere.color = fitsgeo.YELLOW

	box.draw(opacity=0.5)
	sphere.draw(opacity=0.5)

	fitsgeo.phits_export()  # Export sections

Two cells are defined: first as the intersection of the inner part of box and outer part of sphere, second as the inner part of sphere. Note that outer cell are defined automatically, this is due to not providing outer cell manually: in this case we are fine with the default outer world definition. See PHITS sections below.

.. toggle-header::
	:header: **Exported from FitsGeo PHITS Sections**

		.. code-block:: none

			[ Material ]
			    mat[1] H 2.0 O 1.0  GAS=0 $ name: 'MAT_WATER'

			[ Mat Name Color ]
			        mat     name    size    color
			        1       {MAT\_WATER}    1.00    blue

			[ Surface ]
			    1   BOX  0.0 0.0 0.0  1.0 0.0 0.0  0.0 1.0 0.0  0.0 0.0 1.0 $ name: 'BOX' (box, all angles are 90deg) [x0 y0 z0] [Ax Ay Az] [Bx By Bz] [Cx Cy Cz]
			    2   SPH  0.0 0.0 0.0  1.0 $ name: 'SPH' (sphere) x0 y0 z0 R

			[ Cell ]
			    1    -1    (1 2)    $ 'OUTER WORLD'

			    2 1  -1.0  (-1) (2)   $ name: 'Intersection' 
			    3 1  -1.0  (-2)   $ name: 'Inner Sphere' 

.. toggle-header::
	:header: **Full PHITS Input File**

		.. code-block:: none

			[ Parameters ]
				icntl = 11		# (D=0) 3:ECH 5:ALL VOID 6:SRC 7,8:GSH 11:DSH 12:DUMP

			[ Source ]
				s-type = 2		# mono-energetic rectangular source
				e0 = 1			# energy of beam [MeV]
				proj = proton	# kind of incident particle

			[ Material ]
			    mat[1] H 2.0 O 1.0  GAS=0 $ name: 'MAT_WATER'

			[ Mat Name Color ]
			        mat     name    size    color
			        1       {MAT\_WATER}    1.00    blue

			[ Surface ]
			    1   BOX  0.0 0.0 0.0  1.0 0.0 0.0  0.0 1.0 0.0  0.0 0.0 1.0 $ name: 'BOX' (box, all angles are 90deg) [x0 y0 z0] [Ax Ay Az] [Bx By Bz] [Cx Cy Cz]
			    2   SPH  0.0 0.0 0.0  1.0 $ name: 'SPH' (sphere) x0 y0 z0 R

			[ Cell ]
			    1    -1    (1 2)    $ 'OUTER WORLD'

			    2 1  -1.0  (-1 2)   $ name: 'Intersection' 
			    3 1  -1.0  (-2)   $ name: 'Inner Sphere' 

			[ T-3Dshow ]
				title = Geometry 3D
				x0 = 0
				y0 = 0
				z0 = 0

				w-wdt = 3
				w-hgt = 3
				w-dst = 10

				w-mnw = 400			# Number of meshes in horizontal direction.
				w-mnh = 400			# Number of meshes in vertical direction.
				w-ang = 0

				e-the = -45
				e-phi = 24
				e-dst = 100

				l-the = 80
				l-phi = 140
				l-dst = 200*100

				file = example1_3D
				output = 3			# (D=3) Region boundary + color
				width = 0.5			# (D=0.5) The option defines the line thickness.
				epsout = 1

			[ E n d ]

.. figure:: images/cell_example.png
	:align: center
	:figclass: align-center

	**Another cells definition**

Finally, just like ``surface`` and ``material`` modules, ``cell`` module provides ``created_cells`` list with all initialized cells in it. This list can be obtained through::

	fitsgeo.created_cells

Export module
-------------

Module provides functions for export of all defined objects to MC code understandable format (only export to PHTIS for now). Example::

	fitsgeo.phits_export()

This will print [ Surface ], [ Cell ] and [ Material ] sections in console (other sections may be exported in future releases). By default all sections are exported in console, but this behaviour may be configured by providing parameters:

* ``to_file: bool = False`` --- flag to export sections to the input file
* ``inp_name: str = "example"`` --- name for input file export
* ``export_surfaces: bool = True`` --- flag for [ Surface ] section export
* ``export_materials: bool = True`` --- flag for [ Material ] section export
* ``export_cells: bool = True`` --- flag for [ Cell ] section export

Example of exporting sections to input file::

	fitsgeo.phits_export(to_file=True, inp_name="example")

This will export all defined sections in one ``example_FitsGeo.inp`` file. Some sections may be excluded from export::

	fitsgeo.phits_export(to_file=True, inp_name="example", export_materials=False)

This will export only [ Surface ] and [ Cell ] sections.

Example 0: column
=================

.. rubric:: Illustrative example of FitsGeo usage. Very basic example of how to use FitsGeo

.. figure:: images/example0_3D.png
	:align: center
	:figclass: align-center

	**Example 0: PHITS visualization**

.. toggle-header::
	:header: **Example 0**

	.. literalinclude:: examples/example0.py
		:linenos:
		:language: python		

.. figure:: images/example0_fg.png
	:align: center
	:figclass: align-center

	**Example 0: FitsGeo visualization**

Example 1: general illustrative example of FitsGeo use
======================================================

.. rubric:: Illustrative example of FitsGeo usage. Covers all implemented surfaces and features

.. figure:: images/example1_3D.png
	:align: center
	:figclass: align-center

	**Example 1: PHITS visualization**

.. toggle-header::
	:header: **Example 1**

	.. literalinclude:: examples/example1.py
		:linenos:
		:language: python

Example 2: spheres with hats
============================

.. rubric:: Illustrative example of FitsGeo usage. Shows how to easily create multiple (repeating) objects

.. figure:: images/example2_3D.png
	:align: center
	:figclass: align-center

	**Example 2: PHITS visualization**

.. toggle-header::
	:header: **Example 2**

	.. literalinclude:: examples/example2.py
		:linenos:
		:language: python

Example 3: Snowman
==================

.. rubric:: Illustrative example of FitsGeo usage. Show general workflow for creating complex geometry

.. figure:: images/snowman_3D.png
	:align: center
	:figclass: align-center

	**Example 3: PHITS visualization**

.. toggle-header::
	:header: **Example 3**

	.. literalinclude:: examples/snowman.py
		:linenos:
		:language: python

Advanced
========

.. .. literalinclude:: examples/example1.py
.. 	:linenos:
.. 	:lineno-start: 3
.. 	:emphasize-lines: 1, 2
.. 	:lines: 3-5
.. 	:language: python			