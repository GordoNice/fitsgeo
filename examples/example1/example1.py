# Example 1: general illustrative example of FitsGeo
# Illustrative example of FitsGeo usage
# Covers all implemented surfaces and features
import fitsgeo as fg

fg.list_all_surfaces()  # Shows all implemented surfaces

# Create main scene with axes
ax_l = 5  # Specify axes length
scene = fg.create_scene(ax_length=ax_l)
# Change scene background
scene.background = fg.rgb_to_vector(192, 192, 192)

# Define materials from predefined databases
epoxy = fg.Material.database("MAT_EPOXY", color="pastelblue")
glass = fg.Material.database("MAT_GLASS_PB", color="gray")
al = fg.Material.database("MAT_AL", color="brown")
carbon = fg.Material.database("MAT_CARBON", color="purple")
beryllium = fg.Material.database("MAT_BE", color="green")

# Define material manually
poly = fg.Material(
	[[0, 6, 2], [0, 1, 4]], density=0.94, name="Polyethylene", color="yellow")

# Surface definitions
# Plane definition
p1 = fg.P(1, -1, -1, 4)
px1 = fg.P(0, 0, 0, 1, vert="x")
py1 = fg.P(0, 0, 0, -1, vert="y")
pz1 = fg.P(0, 0, 0, -2, vert="z")

# BOX definition
box_l = fg.BOX(
	[-1, -1, -2],
	[1, 0, 0], [0, 1, 0], [0, 0, 1], name="Box_l", material=epoxy)
box_r = fg.BOX(
	[-1, -1, -2],
	[1, 0, 0], [0, 1, 0], [0, 0, 1], name="Box_r", material=epoxy)

# RPP definition
table = fg.RPP(
	[-0.3, 0.3], [-1, 1], [-0.8, 0.8], name="Table", material=al)

# SPH definition
ball = fg.SPH([0, 1.5, 0], 0.5, name="Ball", material=glass)

# RCC definition
cyl = fg.RCC(
	[0, 0, 0], [1, 1, 1], 0.2, name="Cylinder", material=beryllium)

# TRC definition
hat = fg.TRC([0, 2, 0], [0, 0.5, 0], 0.5, 0.2, name="Hat", material=poly)

# TX definition
hoop = fg.T(
	[-3, 0, 0], 1, 0.05, 0.08, name="Hoop", rot="x", material=carbon)

# TY definition
ring = fg.T([-3, 0, 0], 0.03, 0.02, 0.01, name="Ring", material=poly)

# TZ definition
donut = fg.T(
	[0, 3, 0], 0.3, 0.1, 0.1, name="Donut", rot="z", material=carbon)

# REC definition
tabletop = fg.REC(
	[0, 0.9, 0],
	[0, 0.1, 0],
	[1, 0, 0],
	[0, 2, 0], name="Table Top", material=al)

wedge_r = fg.WED(
	[0, 0, 0], [0, -1, 0], [0, 0, 1], [1, 0, 0], name="Wedge R", material=al)
wedge_l = fg.WED(
	[0, 0, 0], [0, -1, 0], [0, 0, 1], [1, 0, 0], name="Wedge L", material=al)

# We need surface which will contain all surfaces
void = fg.RCC([0, -1.5, 0], [0, 5, 0], 3, material=fg.MAT_VOID)

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
	p.draw(size=ax_l)  # Plane will be sized according to axes

# Draw separately if some flags needed
box_l.draw(label_base=True, label_center=False, opacity=0.8)
box_r.draw(label_base=False, label_center=True, opacity=0.8)
ball.draw(label_center=True, opacity=0.6)
hoop.draw(label_center=True)

# Draw through list without additional flags
for s in [table, cyl, hat, ring, donut, tabletop, wedge_l, wedge_r, void]:
	s.draw()

# Create cells
outer_c = fg.Cell([+void], "Outer Void", fg.MAT_OUTER)

# List of surfaces inside void surface
surfaces = [
	box_l, box_r,
	table, tabletop, ball, cyl, hat, hoop, ring, donut, wedge_l, wedge_r]

# String with surfaces for cell definition
inner_surfaces = ""
for s in surfaces:
	inner_surfaces += +s

void_c = fg.Cell([-void, " ", inner_surfaces], "Void", fg.MAT_VOID)

cells = []
for s in surfaces:
	cells.append(fg.Cell([-s], name=f"{s.name} Cell", material=s.material))

# Redefine specific cells
cells[0].cell_def = [-box_l + +cyl]
cells[1].cell_def = [-box_r + +cyl]
cells[4].cell_def = [-ball + +cyl]

# Print all properties of defined surfaces
for s in fg.created_surfaces:
	s.print_properties()
	print()

# Export sections to PHITS input file
fg.phits_export(to_file=True, inp_name="example1")
