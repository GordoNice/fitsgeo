# Example 0: column
# Very basic example of how to use FitsGeo
import fitsgeo as fg

# Define materials from pre-defined databases
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

# Draw all surfaces with default settings
for s in fg.created_surfaces:
	s.draw(label_center=True)

# Export to PHITS
fg.phits_export(to_file=True, inp_name="example0")
