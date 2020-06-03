# Example 1: General illustrative example of FitsGeo use
# Covers almost all implemented features
import fitsgeo

fitsgeo.list_all_surfaces()  # Shows all implemented surfaces

# Create main scene with axis
ax_l = 5  # Specify axis length
scene, ax_x, ax_y, ax_z = fitsgeo.create_scene(ax_length=ax_l)
# Change scene background
scene.background = fitsgeo.rgb_to_vector(192, 192, 192)

# Define materials
water1 = fitsgeo.Material([[0, 1, 2], [0, 8, 1]], name="Water", color="blue")
vapor = fitsgeo.Material(
	[[0, 1, 2/18], [0, 8, 16/18]],
	gas=True, name="Vapor", ratio_type="mass", color="pastelblue")
metal = fitsgeo.Material([[56, 26, 1]], name="Metal", color="brown")
carbon = fitsgeo.Material([[0, 6, 1]], name="Carbon", color="black")
beryllium = fitsgeo.Material([[0, 4, 1]], name="Beryllium", color="green")

# Surface definitions
# Plane definition
p1 = fitsgeo.P(1, -1, -1, 4)
px1 = fitsgeo.P(0, 0, 0, 1, vert="x")
py1 = fitsgeo.P(0, 0, 0, -1, vert="y")
pz1 = fitsgeo.P(0, 0, 0, -2, vert="z")

# BOX definition
box_l = fitsgeo.BOX(
	[-1, -1, -2], [1, 0, 0], [0, 1, 0], [0, 0, 1], name="Box_l", matn=metal.matn)
box_r = fitsgeo.BOX(
	[-1, -1, -2], [1, 0, 0], [0, 1, 0], [0, 0, 1], name="Box_r", matn=metal.matn)

# RPP definition
table = fitsgeo.RPP([-0.3, 0.3], [-1, 1], [-0.8, 0.8], name="Table", matn=metal.matn)

# SPH definition
ball = fitsgeo.SPH([0, 1.5, 0], 0.5, name="Ball", matn=carbon.matn)

# RCC definition
cyl = fitsgeo.RCC([0, 0, 0], [1, 1, 1], 0.2, name="Cylinder", matn=beryllium.matn)

# TRC definition
cone = fitsgeo.TRC([0, 2, 0], [0, 0.5, 0], 0.5, 0.2, name="Hat")

# TX definition
hoop = fitsgeo.T([-3, 0, 0], 1, 0.05, 0.08, name="Hoop", rot="x")

# TY definition
ring = fitsgeo.T([-3, 0, 0], 0.03, 0.02, 0.01, name="Ring")

# TZ definition
donut = fitsgeo.T([0, 3, 0], 0.3, 0.1, 0.1, name="Donut", rot="z")

# REC definition
tabletop = fitsgeo.REC(
	[0, 0.9, 0],
	[0, 0.1, 0],
	[1, 0, 0],
	[0, 2, 0], name="Table Top")

wedge_r = fitsgeo.WED(
	[0, 0, 0], [0, -1, 0], [0, 0, 1], [1, 0, 0], name="Wedge R")
wedge_l = fitsgeo.WED(
	[0, 0, 0], [0, -1, 0], [0, 0, 1], [1, 0, 0], name="Wedge L")

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
p1.draw(size=ax_l)  # Plane will be sized according to axis
px1.draw(size=ax_l)
py1.draw(size=ax_l)
pz1.draw(size=ax_l)

box_l.draw(opacity=0.5, label_base=True, label_center=True)
box_r.draw(opacity=0.5, label_base=True, label_center=True)
table.draw(color=fitsgeo.BROWN, label_center=True)
ball.draw(opacity=0.5, label_center=True)
cyl.draw(label_base=True, label_center=True)
cone.draw(label_base=True, label_center=True)

hoop.draw(label_center=True)
ring.draw(color=fitsgeo.GOLD, label_center=True)
donut.draw(color=fitsgeo.PURPLE, label_center=True)

tabletop.draw(color=fitsgeo.BROWN, label_center=True)

wedge_l.draw(color=fitsgeo.BROWN, label_base=True, label_center=True)
wedge_r.draw(color=fitsgeo.BROWN, label_base=True, label_center=True)

# Export all drawn surfaces to PHITS as [ Surface ] section
fitsgeo.phits_export(to_file=True, inp_name="example1")

# Properties of BOX
print()
print(f"BOX Area ab: {box_l.get_ab_area}")
print(f"BOX Area bc: {box_l.get_bc_area}")
print(f"BOX Area ac: {box_l.get_ac_area}")
print(f"BOX Length a: {box_l.get_len_a}")
print(f"BOX Length b: {box_l.get_len_b}")
print(f"BOX Length c: {box_l.get_len_c}")
print(f"BOX Volume: {box_l.get_volume}")
print(f"BOX Center: {box_l.get_center}")
print(f"BOX Diagonal vector: {box_l.get_diagonal}")
print(f"BOX Diagonal length: {box_l.get_diagonal_length}")
print()

# Properties of RPP
print()
print(f"RPP Center: {table.get_center}")
print(f"RPP Area wl: {table.get_wl_area}")
print(f"RPP Area hl: {table.get_hl_area}")
print(f"RPP Area wh: {table.get_wh_area}")
print(f"RPP Full Area: {table.get_full_area}")
print(f"RPP Height: {table.get_height}")
print(f"RPP Width: {table.get_width}")
print(f"RPP Length: {table.get_length}")
print(f"RPP Volume: {table.get_volume}")
print()

# Properties of sphere
print()
print(f"SPH Center: {ball.xyz0}")
print(f"SPH Diameter: {ball.diameter}")
print(f"SPH Area: {ball.get_surface_area}")
print(f"SPH Cross section area: {ball.cross_section}")
print(f"SPH Volume: {ball.volume}")
print()

# Properties of cylinder
print()
print(f"RCC Height: {cyl.get_len_h}")
print(f"RCC Diameter: {cyl.diameter}")
print(f"RCC Center: {cyl.get_center}")
print(f"RCC Full Area: {cyl.get_full_area}")
print(f"RCC Side Area: {cyl.get_side_area}")
print(f"RCC Bottom Area: {cyl.bottom_area}")
print(f"RCC Volume: {cyl.get_volume}")
print()

# Properties of cone
print()
print(f"TRC Center: {cone.get_center}")
print(f"TRC Forming: {cone.get_forming}")
print(f"TRC Height: {cone.get_len_h}")
print(f"TRC Bottom Diameter: {cone.bottom_diameter}")
print(f"TRC Center: {cone.top_diameter}")
print(f"TRC Full Area: {cone.get_full_area}")
print(f"TRC Side Area: {cone.get_side_area}")
print(f"TRC Bottom Area: {cone.bottom_area}")
print(f"TRC Top Area: {cone.top_area}")
print(f"TRC Volume: {cone.get_volume}")
print()

# Properties of torus
print()
print(f"TX Center: {hoop.xyz0}")
print(f"TX Circumference: {hoop.circumference}")
print(f"TX Full Area: {hoop.get_full_area}")
print(f"TX Volume: {hoop.get_volume}")
print()

# Properties of elliptical cylinder
print()
print(f"REC Height: {tabletop.get_len_h}")
print(f"REC Major axis: {tabletop.get_len_a}")
print(f"REC Minor axis: {tabletop.get_len_b}")
print(f"REC Center: {tabletop.get_center}")
print(f"REC Bottom Area: {tabletop.get_bottom_area}")
print()
