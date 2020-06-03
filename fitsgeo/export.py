from fitsgeo.surface import created_surfaces, P
from fitsgeo.material import created_materials


def phits_export(
		to_file=False, inp_name="example",
		export_surfaces=True, export_materials=True, export_cells=True):
	# TODO: improve export to file
	"""
	Function for printing defined sections in PHITS format, uses created_surfaces,
	created_materials lists which contain all defined objects

	:param export_surfaces: True for export [ Surface ] section
	:param export_materials: True for export [ Material ] section
	:param export_cells: True for export [ Cell ] section
	:param to_file: if True, input file with PHTIS sections will be created
	:param inp_name: name for PHITS input file
	"""
	if not created_materials:
		print("No materials defined!\ncreated_materials list is empty!")
		export_materials = False
	text_materials = "\n[ Material ]\n"
	for mat in created_materials:
		text_materials += mat.phits_print() + "\n"
	text_materials += "\n[ Mat Name Color ]\n\tmat\tname\tsize\tcolor\n"
	for mat in created_materials:
		text_materials += f"\t{mat.matn}\t{mat.name}\t1.00\t{mat.color}\n"

	# TODO: better export of [ Cell ] section
	text_cells = "\n[ Cell ]\n"
	text = ""
	for s in created_surfaces:
		if not isinstance(s, P):  # Add if not plane
			text += f"{s.sn} "
	text_cells += f"    1    -1    ({text[:-1]})	$ 'outer world'\n\n"
	for s in created_surfaces:
		if not isinstance(s, P):  # Add if not plane
			text_cells +=\
				f"    {s.sn+1}    {s.matn}    -1.0" + \
				f"    ({-s.sn})		$ name: '{s.name}'\n"

	if not created_surfaces:
		print("No materials defined!\ncreated_materials list is empty!")
		export_surfaces = False
	text_surfaces = "\n[ Surface ]\n"
	for s in created_surfaces:
		text_surfaces += s.phits_print() + "\n"

	print(text_materials+text_cells+text_surfaces)

	if to_file:
		with open(f"{inp_name}_FitsGeo.inp", "w", encoding="utf-8") as f:
			if export_materials:
				f.write(text_materials)
			if export_cells:
				f.write(text_cells)
			if export_surfaces:
				f.write(text_surfaces)
