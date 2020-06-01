# Example2: Spheres with Hats
# Illustrative example of FitsGeo usage
# Shows how to create multiple objects
import fitsgeo

# Create main scene, with axis
scene, ax_x, ax_y, ax_z = fitsgeo.create_scene(
	ax_length=12, background=fitsgeo.WHITE)

balls = []
hats = []

n = 3  # Number of objects along each axis

i = 0
for z in range(n):
	for y in range(n):
		for x in range(n):
			balls.append(
				fitsgeo.SPH(
					[x + (1 * x), y + (1 * y), z + (1 * z)], 0.5, matn=1))

			hat_h = balls[i].r
			hat_r = balls[i].diameter/2

			hat_x0 = balls[i].x0
			hat_y0 = balls[i].y0 + hat_h
			hat_z0 = balls[i].z0

			hats.append(
				fitsgeo.TRC(
					[hat_x0, hat_y0, hat_z0],
					[0, hat_h, 0], hat_r, hat_r/2, matn=2))
			i += 1

for i in range(n**3):

	balls[i].draw(
			color=fitsgeo.rgb_to_vector(255 - 2.04 * i, 0, 2.04 * i))
	hats[i].draw(
			color=fitsgeo.rgb_to_vector(2.04 * i, 255 - 2.04 * i, 0), truncated=True)

# Export all drawn surfaces to PHITS as [ Surface ] section
fitsgeo.phits_export(to_file=True, filename="example2")
