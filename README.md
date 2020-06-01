## FitsGeo

**FitsGeo** is a Python module simplifying time consuming part of work related 
to geometry development in particle transport Monte Carlo code **PHITS** (other
codes can be added in future releases). We assume that user need to create an
input file for PHITS code for his future research. Default way of creation
geometry may be a bit difficult especially with complicated geometry.
Also, visualization of created geometry in PHITS is very limited which makes
process of geometry setup way more difficult. **FitsGeo** simplifies this
process, user can define geometry surfaces as Python objects with all coming
benefits. Visualization based on **VPython**, so all defined surfaces in user
geometry is purely 3D and can be viewed in browser from any point of view.

**FitsGeo** provides the main modules: `surface.py` and `const.py`,
and additional usage examples. Module works under any operating system
(only Python 3 interpreter with additional modules have to be installed).
Very basic skills in programming on Python required.

### Quick installation guide

Install latest Python 3 framework, then type in console:

    pip install FitsGeo

### Requirements

vpython>=7.6.1

numpy>=1.16.2

scipy>=1.2.2
