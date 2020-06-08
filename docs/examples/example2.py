# Example 2: Spheres with Hats
# Illustrative example of FitsGeo usage
# Shows how to easily create multiple (repeating) objects
import fitsgeo

# Create main scene, with axis
scene, ax_x, ax_y, ax_z = fitsgeo.create_scene(ax_length=10)

gold = fitsgeo.Material.database("MAT_AU", color="yellow")
bronze = fitsgeo.Material.database("MAT_BRONZE", color="pastelbrown")

balls, hats = [], []

n = 3  # Number of objects along each axis

i = 0
for z in range(n):
	for y in range(n):
		for x in range(n):
			balls.append(
				fitsgeo.SPH(
					[x + (1 * x), y + (1 * y), z + (1 * z)],
					0.5, material=bronze))

			hat_h = balls[i].r
			hat_r = balls[i].diameter/2

			hat_x0 = balls[i].x0
			hat_y0 = balls[i].y0 + hat_h
			hat_z0 = balls[i].z0

			hats.append(
				fitsgeo.TRC(
					[hat_x0, hat_y0, hat_z0],
					[0, hat_h, 0], hat_r, hat_r/2, material=gold))
			i += 1

for i in range(n**3):

	balls[i].draw()
	hats[i].draw(truncated=True)

# Export all drawn surfaces to PHITS as [ Surface ] section and basic [ Cell ]
fitsgeo.phits_export(to_file=True, inp_name="example2")
