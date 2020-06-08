from .surface import created_surfaces, P
from .material import created_materials
from .cell import created_cells


def phits_export(
		to_file=False, inp_name="example",
		export_surfaces=True, export_materials=True, export_cells=True):
	# TODO: improve export to file
	"""
	Function for printing defined sections in PHITS format, uses created_surfaces,
	created_materials lists which contain all defined objects

	:param export_surfaces: True for export [ Surface ] section in file
	:param export_materials: True for export [ Material ] section in file
	:param export_cells: True for export [ Cell ] section in file
	:param to_file: if True, input file with PHTIS sections will be created
	:param inp_name: name for PHITS input file
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
	# TODO: better export of [ Cell ] section
	text_cells = "\n[ Cell ]\n"

	flag_out = False  # Flag for outer cell
	for c in created_cells:
		if c.material.matn == -1:  # Check if outer defined by user
			flag_out = True

	if not flag_out:
		text = ""
		for s in created_surfaces:
			if not isinstance(s, P):  # Add if not plane
				text += f"{s.sn} "
		text_cells += f"    1    -1    ({text[:-1]})	$ 'OUTER WORLD'\n\n"

	if not created_cells:  # By default
		for s in created_surfaces:
			if not isinstance(s, P):  # Add if not plane
				text_cells +=\
					f"    {s.sn+1}    {s.material.matn}    {-s.material.density}" + \
					f"    ({-s.sn})		$ name: '{s.name}'\n"
	else:
		for c in created_cells:
			text_cells += c.phits_print() + "\n"
# ------------------------------------------------------------------------------
	print(text_materials+text_surfaces+text_cells)

	if to_file:
		with open(f"{inp_name}_FitsGeo.inp", "w", encoding="utf-8") as f:
			if export_materials:
				f.write(text_materials)
			if export_cells:
				f.write(text_cells)
			if export_surfaces:
				f.write(text_surfaces)


if __name__ == "__main__":
	print(
		"--- Welcome to FitsGeo! ---\n" +
		"This is a module for FitsGeo!\nImport FitsGeo to use.")
