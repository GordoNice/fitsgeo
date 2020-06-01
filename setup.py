import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setuptools.setup(
	name="FitsGeo",
	version="0.1.1",
	author="Ivan Gordeev",
	author_email="gordeev@jinr.ru",
	description="FitsGeo: package for PHITS geometry development",
	keywords='VPython PHITS geometry visualization development',
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/GordoNice/fitsgeo",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.6",
		# How mature is this project? Common values are
		#   3 - Alpha
		#   4 - Beta
		#   5 - Production/Stable
		'Development Status :: 3 - Alpha',
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Scientific/Engineering :: Physics',
		'Intended Audience :: Science/Research'],
	python_requires='>=3.6',
	install_requires=[
		'vpython>=7.6.1',
		'numpy>=1.16.2',
		'scipy>=1.2.2']
)
