# Example 3: Snowman.
# Illustrative example of FitsGeo usage
# Shows general workflow of creating complex geometry
import fitsgeo as fg

# Create main scene, with axis
fg.create_scene(ax_length=5, background=fg.WHITE)

# Define materials
fg.MAT_WATER.color = "lightgray"
ice = fg.MAT_WATER
carbon = fg.Material.database("MAT_CARBON", color="black")
poly = fg.Material.database("MAT_PARAFFIN", color="orange")

# Create all objects for snowman
bottom = fg.SPH([0, 0, 0], 1, material=ice, name="bottom")

middle = fg.SPH(
	[bottom.x0, bottom.y0+bottom.r, bottom.z0],
	bottom.r/1.5, material=ice, name="middle")

top = fg.SPH(
	[
		middle.x0,
		middle.y0+middle.r*1.2,
		middle.z0],
	middle.r/1.5, material=ice, name="top")

carrot = fg.TRC(
	[
		top.x0,
		top.y0+top.r/4,
		top.z0+top.r/2],
	[0, 0, top.diameter*0.8], top.r/6, 1e-3, material=poly)

hat_bottom = fg.RCC(
	[top.x0, top.y0+top.r, top.z0],
	[top.x0, middle.r/7, top.z0],
	top.r/1.5, material=carbon, name="Hat bottom")

hat_top = fg.RCC(
	[
		hat_bottom.get_center[0],
		hat_bottom.get_center[1]+hat_bottom.get_len_h/2,
		hat_bottom.get_center[2]],
	[hat_bottom.get_center[0], hat_bottom.get_len_h*4, hat_bottom.get_center[2]],
	hat_bottom.r/1.5, material=carbon, name="Hat top")

eye_l = fg.SPH(
	[
		top.x0 - top.r*0.3,
		top.y0 + top.r/2,
		top.z0 + top.r*0.8],
	top.r/10, material=carbon, name="Left Eye")

eye_r = fg.SPH(
	[
		top.x0 + top.r*0.3,
		top.y0 + top.r/2,
		top.z0 + top.r*0.8],
	eye_l.r, material=carbon, name="Right Eye")

button1 = fg.SPH(
	[
		middle.x0,
		middle.y0 + middle.r*0.4,
		middle.z0 + middle.r*0.9],
	eye_r.r*1.2, material=carbon, name="Button1")

button2 = fg.SPH(
	[
		middle.x0,
		middle.y0,
		middle.z0 + middle.r],
	button1.r*1.1, material=carbon, name="Button2")

mouth1 = fg.T(
	[
		top.x0,
		top.y0*0.95,
		top.z0 + top.r],
	top.r/30, eye_l.r/7, eye_l.r/5,
	name="Mouth 1", material=carbon, rot="z")

mouth2 = fg.T(
	[
		top.x0 + 3*mouth1.r,
		top.y0*0.95 + 1.1*mouth1.r,
		top.z0 + top.r],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth 2", material=carbon, rot="z")

mouth3 = fg.T(
	[
		top.x0 - 3*mouth1.r,
		top.y0*0.95 + 1.1*mouth1.r,
		top.z0 + top.r],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth 3", material=carbon, rot="z")

mouth4 = fg.T(
	[
		mouth3.x0 - 3*mouth1.r,
		mouth3.y0 + 1.5*mouth1.r,
		mouth3.z0],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth 4", material=carbon, rot="z")

mouth5 = fg.T(
	[
		mouth2.x0 + 3*mouth1.r,
		mouth2.y0 + 1.5*mouth1.r,
		mouth2.z0],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth 5", material=carbon, rot="z")

outer = fg.SPH(r=3, name="Outer edge", material=fg.MAT_VOID)

# Create cells
outer_c = fg.Cell([+outer], "Outer Void", fg.MAT_OUTER)
inner_c = fg.Cell(
	[-outer + +bottom + +middle + +top + +hat_bottom + +hat_top + +carrot +
	 	+eye_l + +eye_r + +button1 + +button2 +
	 	+mouth1 + +mouth2 + +mouth3 + +mouth4 + +mouth5],
	"Inner Cell", fg.MAT_VOID)
bottom_c = fg.Cell([-bottom + +middle], "Bottom Cell", ice)
middle_c = fg.Cell(
	[-middle + +button1 + +button2 + +top], "Middle Cell", ice)
top_c = fg.Cell(
	[-top + +carrot + +eye_l + +eye_r],
	"Top Cell", ice)

buttons = []
for btn in [button1, button2]:
	buttons.append(fg.Cell([-btn], f"{btn.name} Cell", carbon, btn.volume))

mouth = []
for m in [mouth1, mouth2, mouth3, mouth4, mouth5]:
	mouth.append(fg.Cell([-m], f"{m.name} Cell", carbon, m.get_volume))

eyes = []
for eye in [eye_l, eye_r]:
	eyes.append(fg.Cell([-eye], f"{eye.name} Cell", carbon, eye.volume))

carrot_c = fg.Cell([-carrot], "Carrot Cell", poly, carrot.get_volume)

hat = []
for h in [hat_bottom, hat_top]:
	hat.append(fg.Cell([-h], f"{h.name} Cell", carbon, h.get_volume))

# Draw all defined objects
for s in [s for s in fg.created_surfaces if s is not carrot]:
	s.draw()

carrot.draw(truncated=False)

# Export all drawn surfaces to PHITS input sections
fg.phits_export(to_file=True, inp_name="snowman")
