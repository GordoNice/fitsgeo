.. highlight:: python

===============
Getting Started
===============

.. rubric:: Brief overview of FitsGeo and how to install it

Introduction
============

`FitsGeo`_ is a Python package simplifying time consuming part of work related to geometry development in particle transport Monte Carlo code `PHITS`_ (other codes can be added in future releases). Assume that user need to create an input file for PHITS code for his future research, default way of creation geometry section may be a bit difficult, especially with complicated geometries. Also, visualization of created geometry in PHITS is very limited (eps creation) which makes process of geometry setup way more difficult. **FitsGeo** simplifies this process, user can define geometry surfaces as Python objects with all coming benefits. Visualization based on `VPython`_, so all defined surfaces in user geometry is purely 3D and can be viewed in browser from any point of view.

**FitsGeo** currently consist of the main files: ``fitsgeo.py`` and ``const.py``, and additional usage examples. Module works under any operating system (only Python 3 interpreter with additional modules have to be installed). Very basic skills in programming on Python required.

Quick installation guide
========================

Install latest Python 3 framework, then type in console::

	git clone https://github.com/GordoNice/FitsGeo.git

This command will automatically download directory with all code of **FitsGeo**.

For more detailed instruction of installation and requirements, see `installation guide <install.html>`_.

Using FitsGeo
=============

.. todo:: This section is not done yet



	import fitsgeo



Features
========

* Great visualization capabilities involving VPython
* Easy geometry setup as Python objects
* Additional properties for every type of object
* Export [ Surface ] and basic [ Cell ] sections to PHITS
* Work with Python allows more flexibility while geometry development

Bugs
====

- Truncated cones sometimes not stable in visualization
- Major and minor axes for REC object have only magnitude meaning 

Future development
==================

* Transformations for objects
* Export to other codes (MCNP, FLUKA)
* More detailed cell definition
* Source object

Support
=======

Feel free to submit any bugs or suggestions via `issues on github <https://github.com/GordoNice/fitsgeo/issues>`_.

License
=======

FitsGeo is licensed under `GPLv3 <https://github.com/GordoNice/fitsgeo/blob/master/LICENSE.txt>`_.

.. _PHITS: https://phits.jaea.go.jp/
.. _FitsGeo: https://github.com/GordoNice/fitsgeo/
.. _VPython: https://vpython.org/