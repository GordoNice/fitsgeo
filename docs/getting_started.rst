.. highlight:: python

===============
Getting Started
===============

.. rubric:: Brief overview of FitsGeo, how to install and use

Introduction
============

`FitsGeo`_ is a Python package simplifying time consuming part of work related to geometry development in particle transport Monte Carlo code `PHITS`_ (other codes can be added in future releases). We assume that user need to create an input file for **PHITS** code for his future research and default way of creation geometry may be a bit difficult especially with complicated geometry cases. Also, visualization of created geometry in PHITS is very limited which makes process of geometry construction way more difficult. **FitsGeo** simplifies this process, user can define geometry surfaces as Python objects with all coming benefits. Visualization based on `VPython`_, so all defined surfaces in user geometry is represented in 3D and can be viewed in browser from any point.

**FitsGeo** provides bunch of modules dedicated to generation of certain sections of input files for PHITS. **FitsGeo** works under any operating system (only Python 3 interpreter with additional modules have to be installed). Very basic skills in programming with Python required. **FitsGeo** package provides bunch of usage examples, therefore, even for the new Python user it will be easy to develop their own geometries for future research.

Quick installation guide
========================

Install latest Python 3 interpreter and pip tool, then type in console::

	pip install FitsGeo
    
or::

	pip3 install FitsGeo

This command will automatically download package and all dependencies. For more detailed installation guide please look at `installation guide <install.html>`_.

Requirements
============

Additional modules for FitsGeo use (automatically installed via pip tool):

* ``vpython>=7.6.1``
* ``numpy>=1.16.2``
* ``scipy>=1.2.2``
* ``pandas>=0.25.1``

All modules listed in `requirements.txt` in root of github project.

Using FitsGeo
=============

After package is installed, user need to create his own Python file ``example.py`` and import FitsGeo package::

	import fitsgeo

After that, FitsGeo can be used. To create scene for future geometry please type::

	scene = fitsgeo.create_scene()

This will create basic VPython canvas with some default settings, these settings can be configured right when method is called::

	scene = fitsgeo.create_scene(background=fitsgeo.GRAY, ax_length=5)

This will configure background to be gray and axes length. To create surface objects::

	sphere = fitsgeo.SPH([0, 0, 0], 1)  # Sphere at (0, 0, 0) with R = 1
	# ...

Draw these objects on scene::

	sphere.draw()
	# ...

Export to PHITS (only after every object will be drawn!)::

	fitsgeo.phits_export()  # For output in console

for saving in file::

	fitsgeo.phits_export(to_file=True, filename="example1")

That's it! File with all drawn surfaces (only sphere for this example) ``example1_FitsGeo.inp`` is generated in your current directory. Now user can paste created [ Surface ], [ Cell ] and [ Material ] sections in PHITS input. [ Cell ] section as well as [ Material ] one in current version provide only basic functionality (under development), must be revised and corrected accordingly, though, these parts not changes often.

For more detailed instructions with examples see `user's guide <user_guide.html>`_.

Features
========

* Great visualization capabilities involving VPython
* Easy geometry setup as Python objects
* Work with Python allows more flexibility while geometry development
* Additional properties for every type of surface
* Export [ Surface ] and basic [ Cell ] and [ Material ] sections to PHITS

Known bugs
==========

- Truncated cones sometimes not stable in visualization
- Major and minor axes for REC object have only magnitude meaning 

Future development
==================
Current version is very raw and more features will come in the near future:

* More detailed cell and material definition
* Adding other sections to PHITS export
* Export to other codes (MCNP, FLUKA)
* Transformations for objects

Support
=======

Feel free to submit any bugs or suggestions via `issues on github <https://github.com/GordoNice/fitsgeo/issues>`_.

License
=======

FitsGeo is licensed under `MIT License <https://github.com/GordoNice/fitsgeo/blob/master/LICENSE.txt>`_.

FitsGeo includes part of software developed by Members of the `Geant4 Collaboration <http://cern.ch/geant4>`_. `GDATABASE.dat <https://github.com/GordoNice/fitsgeo/blob/master/fitsgeo/data/GDATABASE.dat>`_ material database was adopted from `Geant4 Material Database <http://geant4-userdoc.web.cern.ch/geant4-userdoc/UsersGuides/ForApplicationDeveloper/html/Appendix/materialNames.html>`_ list.

Another material database `SDATABASE.dat <https://github.com/GordoNice/fitsgeo/blob/master/fitsgeo/data/SDATABASE.dat>`_ was adopted from `SRIM software <http://srim.org/>`_.

All required disclaimers/licenses listed at the beginning of these databases.

.. _PHITS: https://phits.jaea.go.jp/
.. _FitsGeo: https://github.com/GordoNice/fitsgeo/
.. _VPython: https://vpython.org/
