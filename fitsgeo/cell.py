import itertools
from .material import Material, MAT_WATER

# Counter for objects, every new object will have n+1 surface number
cell_counter = itertools.count(100)

created_cells = []  # All objects after initialisation go here


class Cell:  # superclass with common properties/methods for all surfaces

	def __init__(
			self, cell_def: list, name="Cell",
			material=MAT_WATER, volume: float = None):
		"""
		Define cell

		:param cell_def: list with regions and the Boolean operators,
			⊔(blank)(AND), :(OR), and #(NOT). Parentheses ( and ) will be added
			automatically for regions

		:param name: name for object
		:param material: material associated with cell
		:param volume: cell volume in cm^3
		"""
		self.cell_def = cell_def
		self.name = name
		self.material = material
		self.volume = volume

		self.cn = next(cell_counter)
		created_cells.append(self)

	@property
	def cell_def(self):
		"""
		Get cell definition

		:return: list with cell definition
		"""
		return self.__cell_def

	@cell_def.setter
	def cell_def(self, cell_def: list):
		"""
		Set cell definition

		:param cell_def: cell definition
		"""
		self.__cell_def = cell_def

	@property
	def name(self):
		"""
		Get cell object name

		:return: string name
		"""
		return self.__name

	@name.setter
	def name(self, name: str):
		"""
		Set cell object name

		:param name: surface object name
		"""
		self.__name = name

	@property
	def material(self):
		"""
		Get cell material

		:return: Material object
		"""
		return self.__material

	@material.setter
	def material(self, material: Material):
		"""
		Set cell material

		:param material: material
		"""
		self.__material = material

	@property
	def cn(self):
		"""
		Get cell object number

		:return: int cn
		"""
		return self.__cn

	@cn.setter
	def cn(self, cn: int):
		"""
		Set cell object number

		:param cn: cell number [any number from 1 to 999 999]
		"""
		self.__cn = cn

	@property
	def volume(self):
		"""
		Get cell volume

		:return: float volume
		"""
		return self.__volume

	@volume.setter
	def volume(self, volume: float):
		"""
		Set cell object number

		:param volume: volume of cell
		"""
		self.__volume = volume

	def phits_print(self):
		"""
		Print PHITS cell definition

		:return: string with PHITS cell definition
		"""
		# ⊔(blank)(AND), :(OR), and #(NOT) must be used to treat the regions.
		cell_def = ""
		for regions in self.cell_def:
			if regions == " " or regions == ":" or regions == "#":
				cell_def += regions
			elif regions != " " or regions != ":" or regions != "#":
				cell_def += f"({regions[:-1]})"
			else:
				raise ValueError("cell_def incorrect!")

		if self.material.matn < 1:  # For void and outer
			txt = \
				f"    {self.cn} {self.material.matn}  " + \
				f"{cell_def}" + \
				f" $ name: '{self.name}' \n"
			return txt

		if self.volume is None:
			volume = ""
		else:
			volume = f"VOL={self.volume}"

		txt = \
			f"    {self.cn} {self.material.matn}  " + \
			f"{self.material.density}  {cell_def}  {volume}" + \
			f" $ name: '{self.name}' "
		return txt
