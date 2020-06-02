from fitsgeo.surface import drawn_surfaces, P
from fitsgeo.material import created_materials


def phits_export(to_file=False, filename="example"):
	# TODO: improve export to file
	"""
	Function for printing all drawn surfaces in PHITS format, uses drawn_surfaces
	list which contains all surfaces after draw method execution

	:param to_file: if True, file with PHTIS sections [ Surface ] and [ Cell ]
	will be created
	:param filename: name for output file
	"""
	if not drawn_surfaces:
		print("drawn_surfaces list is empty! Draw any surface first!")
		return

	text_material = "\n[ Material ]\n"
	for mat in created_materials:
		text_material += mat.phits_print() + "\n"

	text_cell = "\n[ Cell ]\n"
	text = ""
	for s in drawn_surfaces:
		if not isinstance(s, P):  # Add if not plane
			text += f"{s.sn} "
	text_cell += f"    1    -1    ({text[:-1]})	$ 'outer world'\n\n"
	for s in drawn_surfaces:
		if not isinstance(s, P):  # Add if not plane
			text_cell +=\
				f"    {s.sn+1}    {s.matn}    -1.0" + \
				f"    ({-s.sn})		$ name: '{s.name}'\n"

	text_s = "\n[ Surface ]\n"
	for s in drawn_surfaces:
		text_s += s.phits_print() + "\n"

	if to_file:
		with open(f"{filename}_FitsGeo.inp", "w", encoding="utf-8") as f:
			f.write(text_material)
			f.write(text_cell)
			f.write(text_s)
