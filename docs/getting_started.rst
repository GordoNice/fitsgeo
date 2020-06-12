.. image:: images/logo.*

===============
Getting Started
===============

.. rubric:: Brief overview of FitsGeo: how to install and use

Introduction
============

`FitsGeo`_ is a Python package that simplifies the time-consuming part of the work associated with developing geometry in the Monte Carlo (MC) particle transport code `PHITS`_, other codes such as MCNP, FLUKA, may be added in future releases. To start MC calculations user need to create so-called input file for **PHITS** code and default way of creation geometry section in this input file may be a bit difficult especially with complicated geometry cases. Also, visualization of created geometry in PHITS is limited to only 2D non-interactive representation which makes process of geometry construction way more difficult. **FitsGeo** simplifies this process, user can define geometry surfaces as Python objects with all coming benefits of object-oriented programming. Visualization part based on `VPython`_, so all defined surfaces in user geometry is represented in 3D and can be viewed in browser from any side. In addition to surfaces, user can also define objects for other sections (materials and cells).

**FitsGeo** provides bunch of modules dedicated to generation of certain sections of PHITS input files. Being Python package, **FitsGeo** works under any operating system --- only Python 3 interpreter with additional modules have to be installed. Very basic skills in programming with Python required to start. **FitsGeo** package provides bunch of usage examples, therefore, even for the new Python user it will be easy to develop their own geometries for future research.

Quick installation guide
========================

Install latest Python 3 interpreter and pip tool, then type in console::

	$ pip install fitsgeo
    
or::

	$ pip3 install fitsgeo

This command will automatically download package and all dependencies. For more detailed installation guide please look at `Installation Guide <install.html>`_.

Requirements
============

Additional modules for FitsGeo use (automatically installed via pip tool):

* ``vpython>=7.6.1``
* ``numpy>=1.16.2``
* ``scipy>=1.2.2``
* ``pandas>=0.25.1``

List with all modules in `requirements.txt <https://github.com/GordoNice/fitsgeo/blob/master/requirements.txt>`_.

Using FitsGeo
=============

After package is installed, user need to create his own Python file ``example.py`` and import FitsGeo package::

	import fitsgeo

After that, FitsGeo can be used. To create scene for future geometry type::

	scene = fitsgeo.create_scene()

This will create basic VPython canvas with some default settings, these settings may be configured right when function is called::

	scene = fitsgeo.create_scene(background=fitsgeo.GRAY, ax_length=5)

This will configure background to be gray and axes length equal to 5 cm. Look at `User's Guide <user_guide.html>`_ for additional parameters of ``create_scene`` function and for functions and objects below. To create materials from pre-defined databases::

	poly = fitsgeo.Material.database("MAT_POLYETHYLENE", color="purple")
	# ... 

To use pre-defined materials user need to be sure that provided material name is in the list. All pre-defined materials can be listed in console::

	fitsgeo.list_all_materials() 

Also, all pre-defined materials listed in `Pre-defined Materials <material.html>`_ section.
Another way to define material is to create material manually::

	poly = fitsgeo.Material(
		[[0, 6, 2], [0, 1, 4]],
		density=0.94, name="Polyethylene", color="purple")
	# ... similar way to create more materials

To create surface objects::

	default_sphere = fitsgeo.SPH()  # Create sphere with default parameters

	sphere = fitsgeo.SPH(
	[0, 0, 0], 1, name="Ball", material=poly)  # Sphere at (0, 0, 0) with R = 1 and Polyethylene material

	box = fitsgeo.BOX(
	[1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1], name="Box", material=poly)  # Box at (1, 1, 1) base point with side equal to 1 cm and Polyethylene material

	# ...

To create cell objects::

	sphere_c = fitsgeo.Cell([-sphere], name="Sphere Cell", material=poly)
	box_c = fitsgeo.Cell([-box], name="Box Cell", material=poly)
	# ...

Creating cell objects not mandatory, if none specified, default [ Cell ] section will be created (which suits for limited cases and may be wrong and must be additionally revised by user). Draw these objects on scene::

	sphere.draw()
	box.draw(label_center=True)
	# ...

Special drawing parameters (e. g. ``label_center``) could generate label indicating object center or base point.

Export to PHITS::

	fitsgeo.phits_export()  # For output in console

For saving in file::

	fitsgeo.phits_export(to_file=True, filename="example")

Additional flags can be provided to export only certain sections.

That's it! File  ``example_FitsGeo.inp`` is generated in your current directory. Now user can paste created sections from generated file to the PHITS input.

For more detailed instructions with examples please take a look at `User's Guide <user_guide.html>`_.

Features
========

* Great visualization capabilities involving VPython
* Easy geometry setup as Python objects
* Python and the OOP paradigm allow more flexibility while geometry development
* Additional properties for every type of defined surface
* Databases with 500+ pre-defined materials
* Export [ Surface ], [ Cell ] and [ Material ] sections to PHITS input file

Known bugs
==========

- Truncated cone sometimes not stable in visualization, this behaviour will be fixed in the future
- Major and minor axes for REC object have only magnitude meaning

Future development
==================

Current version is still raw and more features will come in the near future:

* Other sections to PHITS export
* Export to other codes (MCNP, FLUKA)
* Transformations for objects

Support
=======

Feel free to submit any bugs or suggestions via `issues on GitHub <https://github.com/GordoNice/fitsgeo/issues>`_.

.. _PHITS: https://phits.jaea.go.jp/
.. _FitsGeo: https://github.com/GordoNice/fitsgeo/
.. _VPython: https://vpython.org/
