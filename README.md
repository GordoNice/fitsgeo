## FitsGeo

**FitsGeo** is a Python package simplifying time consuming part of work related 
to geometry development in particle transport Monte Carlo code **PHITS** (other
codes can be added in future releases). We assume that user need to create an
input file for PHITS code for his future research and default way of creation
geometry may be a bit difficult especially with complicated geometry cases.
Also, visualization of created geometry in PHITS is very limited which makes
process of geometry construction way more difficult. **FitsGeo** simplifies this
process, user can define geometry surfaces as Python objects with all coming
benefits. Visualization based on **VPython**, so all defined surfaces in user
geometry is purely 3D and can be viewed in browser from any point of view.

**FitsGeo** works under any operating system: only Python 3 interpreter with
additional modules (listed below) have to be installed. Very basic skills in
programming with Python required. **FitsGeo** provides bunch of usage examples,
which demonstrate basic workflow.

### Quick installation guide

Install latest Python 3 interpreter and pip tool, then type in console:

    pip install FitsGeo
    
or:

    pip3 install FitsGeo

### Requirements

Additional modules for FitsGeo use (automatically install via pip tool):

* vpython>=7.6.1
* numpy>=1.16.2
* scipy>=1.2.2
* pandas>=0.25.1

All modules listed in `requirements.txt`.

### Documentation

Please visit https://fitsgeo.readthedocs.io/ for documentation.
