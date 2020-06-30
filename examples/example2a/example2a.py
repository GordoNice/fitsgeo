# Example 2(a): Spheres with Hats
# Illustrative example of FitsGeo usage
# Shows how to easily create multiple (repeating) objects
import fitsgeo as fg

# Create main scene, with axes
fg.create_scene(ax_length=10)

# Define materials
gold = fg.Material.database("MAT_AU", color="yellow")
bronze = fg.Material.database("MAT_BRONZE", color="pastelbrown")

spheres, hats = [], []  # Lists for surfaces

n = 3  # Number of objects along each axis

cells = []  # List for cells
i = 0
for z in range(n):
	for y in range(n):
		for x in range(n):
			s = fg.SPH(
					[x + (1 * x), y + (1 * y), z + (1 * z)],
					0.5, material=bronze)
			spheres.append(s)
			cells.append(fg.Cell([-s], f"Cell SPH {i}", s.material, s.volume))

			# Parameters for hat
			hat_h = spheres[i].r
			hat_r = spheres[i].diameter / 2
			hat_x0 = spheres[i].x0
			hat_y0 = spheres[i].y0 + hat_h
			hat_z0 = spheres[i].z0

			s = fg.TRC(
					[hat_x0, hat_y0, hat_z0],
					[0, hat_h, 0], hat_r, hat_r/2, material=gold)
			hats.append(s)
			cells.append(fg.Cell([-s], f"Cell TRC {i}", s.material, s.get_volume))
			i += 1

# Void definition
inner_surfaces = ""
for s in fg.created_surfaces:
	inner_surfaces += +s

void_s = fg.RPP(
	[-1, 6], [-1, 6], [-1, 6], "Void Surface", material=fg.MAT_VOID)

outer_c = fg.Cell(
	[+void_s], "Outer Cell", fg.MAT_OUTER)

void_c = fg.Cell(
	[-void_s, " ", inner_surfaces], "Void Cell", void_s.material)

# Draw surfaces
for i in range(n**3):
	spheres[i].draw()
	hats[i].draw(truncated=True)
void_s.draw()

fg.phits_export(to_file=True, inp_name="example2a")
