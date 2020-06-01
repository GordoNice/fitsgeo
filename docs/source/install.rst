.. highlight:: shell

Installation Guide
==================

**FitsGeo** works under any operating system with **Python 3** interpreter and **pip** tool.

If you are familiar with Python and pip tool, simply type following command to install the package::

	$ pip install FitsGeo

or::

	$ pip3 install FitsGeo

If you have both Python 2 and Python 3 versions.

If your are a less advanced user, read the rest of the page.

Installation guide is divided in two parts: prerequisites (mainly Python installation) and main package installation.

Prerequisites --- Python interpreter
------------------------------------

First user need to check if Python interpreter is installed.
Try if one of following commands (printing Python version) works::

    $ python --version
    $ python3 --version

Command ``python`` invokes either Python 2 or 3, while ``python3`` can invoke only Python 3.

**FitsGeo** supports only modern Python 3 versions starting from version 3.6. Please check if interpreter version is supported.

If none of ``python`` and ``python3`` commands are present, then Python interpreter has to be installed. It is better to use the newest available version (starting from 3.6).

Python 3 installation
~~~~~~~~~~~~~~~~~~~~~

The best way to install Python under Linux is to use package manager.

* ``apt-get install python3`` for Debian and Ubuntu
* ``dnf install python3`` for Fedora
* ``yum install python3`` for CentOS and SLC

Under Windows and Mac OS please visit official `Python webpage <https://www.python.org/>`_.

Prerequisites --- pip tool
--------------------------

**pip** is a tool for installing and managing Python packages. It downloads the packages from central Internet repository and installs them.

Try the following commands (printing pip version) in console::

    $ pip --version
    $ pip3 --version

In a similar way to Python interpreter pip is a tool for Python 2 or 3, while pip3 works exclusively for Python 3. If none of these commands are present, then pip has to be installed.

pip installation
~~~~~~~~~~~~~~~~

Follow the package installation for your Linux system.
On some systems instructions mentioned below have to be prefixed with `sudo` command.

* ``apt-get install python3-pip`` (python 3) for Debian and Ubuntu
* ``dnf install python3-pip`` (python 3) for Fedora
* ``yum install python3-pip`` (python 3) for CentOS and SLC

Under Windows and Mac OS please visit official `Python webpage <https://www.python.org/>`_.

Installation FitsGeo via pip
----------------------------

Now it is time to install **FitsGeo** package.
It currently consists of files: ``surface.py`` and ``const.py`` and bunch of examples.

Installation via pip
~~~~~~~~~~~~~~~~~~~~

On some systems commands mentioned below have to be prefixed with `sudo` command::

    $ pip install FitsGeo

To upgrade the **FitsGeo** to newer version, simply type::

    $ pip install --upgrade FitsGeo

To completely remove **FitsGeo** from your system, use following command::

    $ pip uninstall FitsGeo

Now **FitsGeo** package should be installed for all users and can be invoked in Python script by typing::

    $ import fitsgeo

First user be sure to have git and Python 3 interpreter with modules installed, then type in console

Getting FitsGeo via GitHub
--------------------------

**FitsGeo** can be downloaded directly from github webpage using the web browser or via command line::

    $ git clone https://github.com/GordoNice/FitsGeo.git

But first make sure that `git`_ installed.

After downloading, **FitsGeo** can be installed from command line in root directory::

    $ pip install .

or::

    $ pip3 install .

It is recommended to use installation using **pip** tool, described below. It makes easy upgrade and uninstallation procedure.

All scripts with examples located in ``examples`` directory.

.. _git: https://git-scm.com//
