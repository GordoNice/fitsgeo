import pkg_resources
import itertools
import pandas as pd
from random import choice

from .const import ANGEL_COLORS


# Counter for objects, every new object will have n+1 material number
material_counter = itertools.count(1)

created_materials = []  # All objects after initialisation go here


# Periodic table database
DF_PTABLE = pd.read_csv(
	pkg_resources.resource_filename("fitsgeo", "data/PTABLE.dat"),
	sep="\t", comment="#",
	names=[
		"symbol", "name", "atomic_number",
		"atomic_weight", "density", "description"])

# Database for single materials from Periodic Table
DF_PT = pd.read_csv(
	pkg_resources.resource_filename("fitsgeo", "data/PTDATABASE.dat"),
	sep="\t", comment="#")

# Database adopted from SRIM
DF_S = pd.read_csv(
	pkg_resources.resource_filename("fitsgeo", "data/SDATABASE.dat"),
	sep="\t", comment="#")

# Database adopted from GEANT4
DF_G = pd.read_csv(
	pkg_resources.resource_filename("fitsgeo", "data/GDATABASE.dat"),
	sep="\t", comment="#")

MAT_DB = pd.concat([DF_PT, DF_S, DF_G])
# To avoid duplicates
MAT_DB = MAT_DB.drop_duplicates(subset="Name").reset_index(drop=True)
# print(MAT_DB)


def list_all_materials():
	text = ""
	print("List with all available materials:")
	text += "List with all available materials:\n"
	i = 1
	for name in MAT_DB["Name"].tolist():
		print(f"{i}\t-\t'{name}'")
		text += f"{i}\t-\t'{name}'\n"
		i += 1
	print(
		"To use pre-defined materials:" +
		" mat = fitsgeo.Material.database(\"MAT_NAME\")")
	text += "To use pre-defined materials:" + \
		" mat = fitsgeo.Material.database(\"MAT_NAME\")\n"
	return text


class Material:

	def __init__(
			self, elements: list, name="", ratio_type="atomic", density=1.0,
			gas=False, color="black", matn: int = None):
		"""
		Define material

		:param elements: every element in [[A1, Z1, Q1], [A2, Z2, Q2]] format,
			where A - mass number, Z - atomic number, Q - quantity of ratio

		:param name: name for material object
		:param ratio_type: type of ratio: "atomic" (by default) or "mass"
		:param density: density for material (g/cm^3)
		:param gas: True if gas (False by default)
		:param color: one of colors for material visualization via ANGEL
		:param matn: material number
		"""
		self.elements = elements
		self.name = name
		self.ratio_type = ratio_type
		self.density = density
		self.gas = gas
		self.color = color

		if matn is None:
			self.matn = next(material_counter)
		else:
			self.matn = matn
		created_materials.append(self)

	@classmethod
	def database(
			cls, name, gas=False, color: str = None):
		"""
		Initialize material from databases

		:param name: name of material from databases
		:param gas: True if gas (False by default)
		:param color: one of colors for material visualization via ANGEL
		:return:
		"""
		if color is None:
			color = choice(list(ANGEL_COLORS.keys()))

		row_id = MAT_DB.index[MAT_DB["Name"] == name].tolist()

		if row_id:  # If row_id not empty
			n = int(MAT_DB.iloc[row_id[0]]["N"])
			density = float(MAT_DB.iloc[row_id[0]]["Density(g/cm^3)"])
			formula = MAT_DB.iloc[row_id[0]]["Formula (Z Q)"].split()

			elements =\
				[
					[0,
					 int(formula[i]),
					 float(formula[i+1])] for i in range(0, n*2, 2)]

			# Sum all ratios
			total_sum = 0
			for i in range(n):
				total_sum += elements[i][2]

			# If total will be greater than 1.0 it is atomic
			if total_sum > 1.0 or total_sum == 1.0 and n == 1:
				ratio_type = "atomic"
			else:
				ratio_type = "mass"

			return cls(elements, name, ratio_type, density, gas, color)
		else:
			raise NameError(f"No '{name}' name in database!\nPlease try again!")

	@property
	def elements(self):
		"""
		Get elements list in [[A1, Z1, Q1], [A2, Z2, Q2]] format

		:return: list [[A1, Z1, Q1], [A2, Z2, Q2]]
		"""
		return self.__elements

	@elements.setter
	def elements(self, elements: list):
		"""
		Set elements list in [[A1, Z1, Q1], [A2, Z2, Q2]] format

		:param elements: [[A1, Z1, Q1], [A2, Z2, Q2]]
		"""
		self.__elements = elements

	@property
	def name(self):
		"""
		Get material name

		:return: string name
		"""
		return self.__name

	@name.setter
	def name(self, name: str):
		"""
		Set material name

		:param name: material object name
		"""
		self.__name = name

	@property
	def ratio_type(self):
		"""
		Get ratio type for material

		:return: "atomic" or "mass"
		"""
		return self.__ratio_type

	@ratio_type.setter
	def ratio_type(self, ratio_type: str):
		"""
		Set ratio type for material

		:param ratio_type: "atomic" or "mass" types
		"""
		self.__ratio_type = ratio_type

	@property
	def density(self):
		"""
		Get material density

		:return: float density
		"""
		return self.__density

	@density.setter
	def density(self, density: float):
		"""
		Set material density

		:param density: density for material
		"""
		self.__density = density

	@property
	def gas(self):
		"""
		Get material state

		:return: bool
		"""
		return self.__gas

	@gas.setter
	def gas(self, gas: bool):
		"""
		Set material state

		:param gas: True for gas, False for solid
		"""
		self.__gas = gas

	@property
	def color(self):
		"""
		Get material color

		:return: str with ANGEL color
		"""
		return self.__color

	@color.setter
	def color(self, color: str):
		"""
		Set material color

		:param color: ANGEL color
		"""
		self.__color = color

	def phits_print(self):
		"""
		Prints PHITS definition

		:return: string with PHITS definition
		"""
		if self.matn < 1:
			return ""
		else:
			gas = "GAS=0"
			if self.gas:
				gas = "GAS=1"

			text_elrat = ""
			a, el, q = [], [], []
			for element in self.elements:
				if element[0] == 0:
					a.append("")
				else:
					a.append(element[0])
				el.append(DF_PTABLE.iloc[element[1] - 1]["symbol"])
				q.append(element[2])

			if self.ratio_type == "atomic":
				for i in range(len(self.elements)):
					text_elrat += "".join(f"{a[i]}{el[i]} {q[i]} ")
			else:
				for i in range(len(self.elements)):
					text_elrat += "".join(f"{a[i]}{el[i]} -{q[i]} ")

			txt = f"    mat[{self.matn}] {text_elrat} {gas} $ name: '{self.name}'"
			return txt


# Pre-defined materials as constants for default surface material
MAT_OUTER = Material([], matn=-1)  # Special material for outer void
MAT_VOID = Material([], matn=0, color="gray")  # Special material for void
MAT_WATER = Material.database("MAT_WATER", color="blue")


if __name__ == "__main__":
	print(
		"--- Welcome to FitsGeo! ---\n" +
		"This is a module for FitsGeo!\nImport FitsGeo to use.")
