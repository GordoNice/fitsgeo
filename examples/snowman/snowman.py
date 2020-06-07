# Snowman (Example3): one more example of how to use FitsGeo module
# Illustrative example of FitsGeo usage
# Shows general workflow
import fitsgeo

# Create main scene, with axis
fitsgeo.create_scene(ax_length=5, background=fitsgeo.WHITE)

# Define materials
fitsgeo.MAT_WATER.color = "white"
ice = fitsgeo.MAT_WATER
carbon = fitsgeo.Material.database("MAT_CARBON", color="black")
poly = fitsgeo.Material.database("MAT_PARAFFIN", color="orange")

# Create all objects for snowman
bottom = fitsgeo.SPH([0, 0, 0], 1, material=ice, name="bottom")

middle = fitsgeo.SPH(
	[bottom.x0, bottom.y0+bottom.r, bottom.z0],
	bottom.r/1.5, material=ice, name="middle")

top = fitsgeo.SPH(
	[
		middle.x0,
		middle.y0+middle.r*1.2,
		middle.z0],
	middle.r/1.5, material=ice, name="top")

carrot = fitsgeo.TRC(
	[
		top.x0,
		top.y0+top.r/4,
		top.z0+top.r/2],
	[0, 0, top.diameter*0.8], top.r/6, 1e-3, material=poly)

hat_bottom = fitsgeo.RCC(
	[top.x0, top.y0+top.r, top.z0],
	[top.x0, middle.r/7, top.z0],
	top.r/1.5, material=carbon, name="hat")

hat_top = fitsgeo.RCC(
	[
		hat_bottom.get_center[0],
		hat_bottom.get_center[1]+hat_bottom.get_len_h/2,
		hat_bottom.get_center[2]],
	[hat_bottom.get_center[0], hat_bottom.get_len_h*4, hat_bottom.get_center[2]],
	hat_bottom.r/1.5, material=carbon, name="hat")

eye_l = fitsgeo.SPH(
	[
		top.x0 - top.r*0.3,
		top.y0 + top.r/2,
		top.z0 + top.r*0.8],
	top.r/10, material=carbon, name="eye")

eye_r = fitsgeo.SPH(
	[
		top.x0 + top.r*0.3,
		top.y0 + top.r/2,
		top.z0 + top.r*0.8],
	eye_l.r, material=carbon, name="eye")

button1 = fitsgeo.SPH(
	[
		middle.x0,
		middle.y0 + middle.r*0.4,
		middle.z0 + middle.r*0.9],
	eye_r.r*1.2, material=carbon, name="Button1")

button2 = fitsgeo.SPH(
	[
		middle.x0,
		middle.y0,
		middle.z0 + middle.r],
	button1.r*1.1, material=carbon, name="Button2")

mouth1 = fitsgeo.T(
	[
		top.x0,
		top.y0*0.95,
		top.z0 + top.r],
	top.r/30, eye_l.r/7, eye_l.r/5,
	name="Mouth", material=carbon, rot="z")

mouth2 = fitsgeo.T(
	[
		top.x0 + 3*mouth1.r,
		top.y0*0.95 + 1.1*mouth1.r,
		top.z0 + top.r],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth", material=carbon, rot="z")

mouth3 = fitsgeo.T(
	[
		top.x0 - 3*mouth1.r,
		top.y0*0.95 + 1.1*mouth1.r,
		top.z0 + top.r],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth", material=carbon, rot="z")

mouth4 = fitsgeo.T(
	[
		mouth3.x0 - 3*mouth1.r,
		mouth3.y0 + 1.5*mouth1.r,
		mouth3.z0],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth", material=carbon, rot="z")

mouth5 = fitsgeo.T(
	[
		mouth2.x0 + 3*mouth1.r,
		mouth2.y0 + 1.5*mouth1.r,
		mouth2.z0],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth", material=carbon, rot="z")

# Draw all defined objects
for s in [bottom, middle, top]:
	s.draw(label_center=True)

carrot.draw(truncated=True)
hat_bottom.draw()
hat_top.draw(label_base=True)

for s in [
	eye_l, eye_r, button1, button2, mouth1, mouth2, mouth3, mouth4, mouth5]:
	s.draw()

# Export all drawn surfaces to PHITS input sections
fitsgeo.phits_export(to_file=True, inp_name="snowman")
