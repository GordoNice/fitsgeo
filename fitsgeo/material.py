# TODO: Improve Material class
import itertools
import pandas as pd

material_counter = itertools.count(1)

created_materials = []  # All objects after drawing go here

df_ptable = pd.read_csv(
	"fitsgeo/data/PeriodicTable.dat",
	sep="\t",
	names=[
		"symbol",
		"name", "atomic_number", "atomic_weight", "density", "description"],
	skiprows=0)


class Material:

	def __init__(self, elements: list, name="", ratio_type="atomic", gas=False):
		"""
		Define material

		:param elements: every element in [[A1, Z1, Q1], [A2, Z2, Q2]] format
		:param name: name for object
		:param ratio_type: type of ratio: "atomic" (by default) or "mass"
		:param gas: True if gas (False by default)
		"""
		self.elements = elements
		self.name = name
		self.ratio_type = ratio_type
		self.gas = gas

		self.matn = next(material_counter)
		created_materials.append(self)

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

	def phits_print(self):
		"""
		Prints PHITS definition

		:return: string with PHITS definition
		"""
		gas = "GAS=0"
		if self.gas:
			gas = "GAS=1"

		text_elrat = ""
		a = []
		el = []
		q = []
		for element in self.elements:
			if element[0] == 0:
				a.append("")
			else:
				a.append(element[0])
			el.append(df_ptable.iloc[element[1]-1]["symbol"])
			q.append(element[2])

		if self.ratio_type == "atomic":
			for i in range(len(self.elements)):
				text_elrat += "".join(f"{a[i]}{el[i]} {q[i]} ")
		else:
			for i in range(len(self.elements)):
				text_elrat += "".join(f"{a[i]}{el[i]} -{round(q[i], ndigits=6)} ")

		txt = f"    mat[{self.matn}] {text_elrat} {gas} $ name: '{self.name}'"

		print(txt)
		return txt
