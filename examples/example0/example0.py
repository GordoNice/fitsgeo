# Example 0: The Column
# Very basic example of how to use FitsGeo
import fitsgeo as fg  # Alias to make it shorter

# Define materials from predefined databases
concrete = fg.Material.database("MAT_CONCRETE", color="gray")
bronze = fg.Material.database("MAT_BRONZE", color="pastelbrown")

fg.create_scene(ax_length=5)  # Create scene with default settings

base = fg.RCC([0, 0, 0], [0, 2, 0], name="Base", material=concrete)
cone = fg.TRC(
	base.h,
	[base.h[0]/4, base.h[1]/4, base.h[2]/4],
	r_1=base.r, r_2=base.r*2, name="Cone", material=concrete)
platform = fg.RPP(
	[-cone.r_2, cone.r_2],
	[cone.y0+cone.h[1], cone.y0+cone.h[1]+cone.get_len_h/2],
	[-cone.r_2, cone.r_2], name="Platform", material=concrete)
ball = fg.SPH(
	[platform.get_center[0],
	 platform.get_center[1]+cone.r_2/1.4+platform.get_height/2,
	 platform.get_center[2]], r=cone.r_2/1.4, material=bronze)

outer_c = fg.Cell(
	[+base + +cone + +platform + +ball], "Outer Void", fg.MAT_OUTER)
base_c = fg.Cell([-base], "Base Cell", base.material, base.get_volume)
cone_c = fg.Cell([-cone], "Cone Cell", cone.material, cone.get_volume)
platform_c = fg.Cell(
	[-platform], "Platform Cell", platform.material, platform.get_volume)
ball_c = fg.Cell([-ball], "Ball Cell", ball.material, ball.volume)

# Draw all surfaces with labels on centers
for s in fg.created_surfaces:
	s.draw(label_center=True)

# Export to PHITS
fg.phits_export(to_file=True, inp_name="example0")
