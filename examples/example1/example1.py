# Example 1: General illustrative example of FitsGeo use
# Covers almost all implemented features
import fitsgeo

fitsgeo.list_all_surfaces()  # Shows all implemented surfaces

# Create main scene with axis
ax_l = 5  # Specify axis length
scene, ax_x, ax_y, ax_z = fitsgeo.create_scene(ax_length=ax_l)
# Change scene background
scene.background = fitsgeo.rgb_to_vector(192, 192, 192)

# Define materials from pre-defined database
epoxy = fitsgeo.Material.database("MAT_EPOXY", color="pastelblue")
al = fitsgeo.Material.database("MAT_AL", color="brown")
carbon = fitsgeo.Material.database("MAT_CARBON", color="purple")

# Define material by hand
beryllium = fitsgeo.Material.database("MAT_BE", color="green")
poly = fitsgeo.Material(
	[[0, 6, 2], [0, 1, 4]], density=0.94, name="Polyethylene", color="yellow")

# Surface definitions
# Plane definition
p1 = fitsgeo.P(1, -1, -1, 4)
px1 = fitsgeo.P(0, 0, 0, 1, vert="x")
py1 = fitsgeo.P(0, 0, 0, -1, vert="y")
pz1 = fitsgeo.P(0, 0, 0, -2, vert="z")

# BOX definition
box_l = fitsgeo.BOX(
	[-1, -1, -2],
	[1, 0, 0], [0, 1, 0], [0, 0, 1], name="Box_l", material=epoxy)
box_r = fitsgeo.BOX(
	[-1, -1, -2],
	[1, 0, 0], [0, 1, 0], [0, 0, 1], name="Box_r", material=epoxy)

# RPP definition
table = fitsgeo.RPP(
	[-0.3, 0.3], [-1, 1], [-0.8, 0.8], name="Table", material=al)

# SPH definition
ball = fitsgeo.SPH([0, 1.5, 0], 0.5, name="Ball", material=fitsgeo.MAT_WATER)

# RCC definition
cyl = fitsgeo.RCC(
	[0, 0, 0], [1, 1, 1], 0.2, name="Cylinder", material=beryllium)

# TRC definition
cone = fitsgeo.TRC([0, 2, 0], [0, 0.5, 0], 0.5, 0.2, name="Hat", material=poly)

# TX definition
hoop = fitsgeo.T(
	[-3, 0, 0], 1, 0.05, 0.08, name="Hoop", rot="x", material=carbon)

# TY definition
ring = fitsgeo.T([-3, 0, 0], 0.03, 0.02, 0.01, name="Ring", material=poly)

# TZ definition
donut = fitsgeo.T(
	[0, 3, 0], 0.3, 0.1, 0.1, name="Donut", rot="z", material=carbon)

# REC definition
tabletop = fitsgeo.REC(
	[0, 0.9, 0],
	[0, 0.1, 0],
	[1, 0, 0],
	[0, 2, 0], name="Table Top", material=al)

wedge_r = fitsgeo.WED(
	[0, 0, 0], [0, -1, 0], [0, 0, 1], [1, 0, 0], name="Wedge R", material=al)
wedge_l = fitsgeo.WED(
	[0, 0, 0], [0, -1, 0], [0, 0, 1], [1, 0, 0], name="Wedge L", material=al)

# Redefine properties
box_l.xyz0 = [box_l.x0+0.5, box_l.y0+2, box_l.z0+0.1]
box_r.xyz0 = [box_r.x0+0.5, box_r.y0+2, box_r.z0+0.1]
box_r.z0 = box_r.z0+2.8

cyl.xyz0 = box_r.get_center
cyl.h = box_l.get_center - box_r.get_center

ring.xyz0 = [
	tabletop.x0 - tabletop.get_len_b/3,
	tabletop.y0 + tabletop.get_len_h + ring.b,
	tabletop.z0 - tabletop.get_len_b/3]

donut.xyz0 = [
	cyl.get_center[0], cyl.get_center[1], cyl.get_center[2] + cyl.get_len_h/4]
donut.r = cyl.r + donut.b

hoop.r = hoop.r * 0.7
hoop.x0 = -table.get_width/2 - hoop.b

table.y[1] = table.y[1] - tabletop.get_len_h

wedge_r.xyz0 = [
	table.get_center[0]-table.get_width/2,
	table.get_center[1]+table.get_height/2,
	table.get_center[2]+table.get_length/2]

wedge_r.h[0] = table.get_width

wedge_l.xyz0 = [
	table.get_center[0]+table.get_width/2,
	table.get_center[1]+table.get_height/2,
	table.get_center[2]-table.get_length/2]

wedge_l.h[0] = -table.get_width
wedge_l.b[2] = -wedge_l.b[2]

# Draw objects on scene
for p in [p1, px1, py1, pz1]:
	p.draw(size=ax_l)  # Plane will be sized according to axis

box_l.draw(label_base=True, label_center=True)
box_r.draw(label_base=False, label_center=False)
table.draw(label_center=True)
ball.draw(label_center=True)
cyl.draw(label_base=True, label_center=True)
cone.draw(label_base=True, label_center=True)

hoop.draw(label_center=True)
ring.draw(label_center=True)
donut.draw(label_center=True)

tabletop.draw(label_center=True)

wedge_l.draw(label_base=True, label_center=True)
wedge_r.draw(label_base=True, label_center=True)

# Export sections to PHITS input file
fitsgeo.phits_export(to_file=True, inp_name="example1")

# Print all properties of defined surfaces
for s in [box_l, box_r, table, ball, cyl, cone, hoop, tabletop]:
	s.print_properties()
	print()
