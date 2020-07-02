# Example 2b: Snake!
# Illustrative example of FitsGeo usage
# Shows how to easily create multiple (repeating) objects with some math laws
import fitsgeo as fg
from numpy import sin, exp, linspace  # To use math functions

# Create laws for positions of snakes parts
x = linspace(0, 5, 50)  # Create 50 evenly spaced x values from 0 to 5
# Law for z coordinate
z_p = [5 * sin(3 * x_i) * 0.3 * exp(-0.4 * x_i) for x_i in x]
r = [0.02 * exp(0.2 * x_i) for x_i in x]  # Law for radius of spheres

# Define materials for snake and hat
snake_mat = fg.Material.database("MAT_SKIN_ICRP", color="green")
hat_mat = fg.Material.database("MAT_POLYETHYLENE", color="blue")

snake = []  # List with all parts of snake
for i in range(16, len(x)):  # Take x values starting from i=16
	snake.append(
		fg.SPH(xyz0=[x[i] - 3, 0, z_p[i]], r=r[i], material=snake_mat))

last_part = snake[len(snake)-1]
hat = fg.TRC(
	xyz0=[
		last_part.x0,
		last_part.y0 + last_part.r,
		last_part.z0],
	h=[0, last_part.diameter/1.5, 0],
	r_1=last_part.r/1.5,
	r_2=1e-9, material=hat_mat)

void = fg.RCC(
	xyz0=[
		snake[0].x0-0.1,
		snake[0].y0,
		snake[0].z0], h=[4, 0, 0], r=3, material=fg.MAT_VOID)

# Define cells
outer_void = fg.Cell([+void], material=fg.MAT_OUTER)
cells = []
for i in range(len(snake)):
	cells.append(
		fg.Cell([-snake[i]], name=f"Snake Part {i}", material=snake_mat))
# Add a nice hat on head =)
hat_cell = fg.Cell([-hat], name="Hat!", material=hat_mat)

text = ""
for s in snake:
	text += +s

void_cell = fg.Cell(
	[-void, " ", text + +hat], name="Vacuum", material=fg.MAT_VOID)

fg.create_scene(ax_length=5)  # Create scene before draw

# Draw snake
for s in snake:
	s.draw()
hat.draw(truncated=False)  # Difficulties with truncated cone =(
void.draw()

fg.phits_export(to_file=True, inp_name="snake")  # Export sections
