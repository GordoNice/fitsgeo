# Snowman (Example3): one more example of how to use FitsGeo module
# Illustrative example of FitsGeo usage
# Shows general workflow
import fitsgeo

# Create main scene, with axis
scene, ax_x, ax_y, ax_z = fitsgeo.create_scene(
	ax_length=10, background=fitsgeo.WHITE)

# Create all objects for snowman
bottom = fitsgeo.SPH([0, 0, 0], 1, name="bottom")

middle = fitsgeo.SPH(
	[bottom.x0, bottom.y0+bottom.r, bottom.z0],
	bottom.r/1.5, name="middle")

top = fitsgeo.SPH(
	[
		middle.x0,
		middle.y0+middle.r*1.2,
		middle.z0],
	middle.r/1.5, name="top")

carrot = fitsgeo.TRC(
	[
		top.x0,
		top.y0+top.r/4,
		top.z0+top.r/2],

	[0, 0, top.diameter*0.8], top.r/6, 1e-3)

hat_bottom = fitsgeo.RCC(
	[top.x0, top.y0+top.r, top.z0],
	[top.x0, middle.r/7, top.z0],
	top.r/1.5, name="hat")

hat_top = fitsgeo.RCC(
	[
		hat_bottom.get_center[0],
		hat_bottom.get_center[1]+hat_bottom.get_len_h/2,
		hat_bottom.get_center[2]],
	[hat_bottom.get_center[0], hat_bottom.get_len_h*4, hat_bottom.get_center[2]],
	hat_bottom.r/1.5, name="hat")

eye_l = fitsgeo.SPH(
	[
		top.x0 - top.r*0.3,
		top.y0 + top.r/2,
		top.z0 + top.r*0.8],
	top.r/10, name="eye")

eye_r = fitsgeo.SPH(
	[
		top.x0 + top.r*0.3,
		top.y0 + top.r/2,
		top.z0 + top.r*0.8],
	eye_l.r, name="eye")

button1 = fitsgeo.SPH(
	[
		middle.x0,
		middle.y0 + middle.r*0.4,
		middle.z0 + middle.r*0.9],
	eye_r.r*1.2, name="Button1")

button2 = fitsgeo.SPH(
	[
		middle.x0,
		middle.y0,
		middle.z0 + middle.r],
	button1.r*1.1, name="Button2")

mouth1 = fitsgeo.T(
	[
		top.x0,
		top.y0*0.95,
		top.z0 + top.r],
	top.r/30, eye_l.r/7, eye_l.r/5,
	name="Mouth", rot="z")

mouth2 = fitsgeo.T(
	[
		top.x0 + 3*mouth1.r,
		top.y0*0.95 + 1.1*mouth1.r,
		top.z0 + top.r],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth", rot="z")

mouth3 = fitsgeo.T(
	[
		top.x0 - 3*mouth1.r,
		top.y0*0.95 + 1.1*mouth1.r,
		top.z0 + top.r],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth", rot="z")

mouth4 = fitsgeo.T(
	[
		mouth3.x0 - 3*mouth1.r,
		mouth3.y0 + 1.5*mouth1.r,
		mouth3.z0],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth", rot="z")

mouth5 = fitsgeo.T(
	[
		mouth2.x0 + 3*mouth1.r,
		mouth2.y0 + 1.5*mouth1.r,
		mouth2.z0],
	mouth1.r, eye_l.r/7, eye_l.r/5,
	name="Mouth", rot="z")

# Draw all defined objects
for s in [bottom, middle, top]:
	s.draw(color=fitsgeo.WHITE, label_center=True)

carrot.draw(color=fitsgeo.ORANGE, truncated=True)
hat_bottom.draw(color=fitsgeo.PURPLE, label_base=False)
hat_top.draw(color=fitsgeo.PURPLE, label_base=True)

for s in [
	eye_l, eye_r, button1, button2, mouth1, mouth2, mouth3, mouth4, mouth5]:
	s.draw(color=fitsgeo.BLACK)

# Export all drawn surfaces to PHITS input sections
fitsgeo.surface.phits_export(to_file=True, filename="")
