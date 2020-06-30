from .surface import created_surfaces
from .material import created_materials
from .cell import created_cells


def phits_export(
		to_file=False, inp_name="example",
		export_surfaces=True, export_materials=True, export_cells=True):
	# TODO: improve export to file
	"""
	Function for printing defined sections in PHITS format, uses created_surfaces,
	created_materials lists which contain all defined objects

	:param to_file: flag to export sections in input file
	:param inp_name: name for input file export
	:param export_surfaces: flag for [ Surface ] section export
	:param export_materials: flag for [ Material ] section export
	:param export_cells: flag for [ Cell ] section export
	"""
	text_materials = ""
	if not created_materials:
		print("No material is defined!\ncreated_materials list is empty!")
		export_materials = False
	else:
		text_materials = "\n[ Material ]\n"
		for mat in created_materials:
			if mat.phits_print() != "":
				text_materials += mat.phits_print() + "\n"
		# For colors
		text_materials += "\n[ Mat Name Color ]\n\tmat\tname\tsize\tcolor\n"
		for mat in created_materials:
			if mat.matn > 0:  # To avoid outer and void
				mat_name = "{"+mat.name.replace('_', '\\_')+"}"
				text_materials += \
					f"\t{mat.matn}\t{mat_name}\t1.00\t{mat.color}\n"
# ------------------------------------------------------------------------------
	text_surfaces = ""
	if not created_surfaces:
		print("No surface is defined!\ncreated_surfaces list is empty!")
		export_surfaces = False
	else:
		text_surfaces = "\n[ Surface ]\n"
		for s in created_surfaces:
			text_surfaces += s.phits_print() + "\n"
# ------------------------------------------------------------------------------
	text_cells = ""
	if not created_cells:
		print("No cell is defined!\ncreated_cells list is empty!")
		export_cells = False
	else:
		text_cells = "\n[ Cell ]\n"
		for c in created_cells:
			text_cells += c.phits_print() + "\n"
# ------------------------------------------------------------------------------
	print(text_materials+text_surfaces+text_cells)

	if to_file:
		with open(f"{inp_name}_FitsGeo.inp", "w", encoding="utf-8") as f:
			if export_materials:
				f.write(text_materials)
			if export_surfaces:
				f.write(text_surfaces)
			if export_cells:
				f.write(text_cells)


if __name__ == "__main__":
	print(
		"--- Welcome to FitsGeo! ---\n" +
		"This is a module for FitsGeo!\nImport FitsGeo to use.")
