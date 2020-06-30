import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
	requirements = f.read().rstrip("\n").split("\n")

setuptools.setup(
	name="FitsGeo",
	version="1.0.0",
	author="Ivan Gordeev",
	author_email="gordeev@jinr.ru",
	description="FitsGeo: Python package for PHITS geometry development",
	keywords="Python VPython PHITS geometry visualization development",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/GordoNice/fitsgeo",
	packages=setuptools.find_packages(),
	package_data={
		'fitsgeo': ['data/*.dat'],
	},
	classifiers=[
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		# How mature is this project? Common values are
		#   3 - Alpha
		#   4 - Beta
		#   5 - Production/Stable
		"Development Status :: 5 - Production/Stable",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Scientific/Engineering :: Physics",
		"Intended Audience :: Science/Research"],
	python_requires=">=3.7",
	install_requires=requirements
)
