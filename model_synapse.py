import sys
import os

MCELL_PATH = os.environ.get("MCELL_PATH", "")
MCELL_PATH = "/Applications/Blender-2.93-CellBlender/blender.app/Contents/Resources/2.93/scripts/addons/cellblender/extensions/mcell/"
if MCELL_PATH:
    lib_path = os.path.join(MCELL_PATH, "lib")
    sys.path.append(lib_path)
else:
    print(
        "Error: system variable MCELL_PATH that is used to find the mcell "
        "library was not set."
    )
    sys.exit(1)


import mcell as m
import math

D = 2e-6  # cm^2.s
synapse_width = 20e-3  # um
synapse_radius = 200e-3  # um


def define_cylinder(base_number_of_points: int):
    imax = base_number_of_points
    i2max = 2 * imax
    vertices = []
    walls = []

    for i in range(base_number_of_points):
        x = math.cos(2 * math.pi * (i / imax)) * synapse_radius
        y = math.sin(2 * math.pi * (i / imax)) * synapse_radius
        vertices.append([x, y, 0])
        vertices.append([x, y, synapse_width])

    vertices += [[0, 0, 0], [0, 0, synapse_width]]

    for i in range(base_number_of_points):
        walls.append([(2 * i) % i2max, (2 * i + 1) % i2max, (2 * i + 2) % i2max])
        walls.append([(2 * i + 3) % i2max, (2 * i + 1) % i2max, (2 * i + 2) % i2max])
        walls.append([(2 * i) % i2max, (2 * i + 2) % i2max, i2max])
        walls.append([(2 * i + 1) % i2max, (2 * i + 3) % i2max, i2max + 1])

    return vertices, walls


synapse_cylinder_vertex_list, synapse_cylinder_walls_list = define_cylinder(10)


viz_output = m.VizOutput(
    output_files_prefix="./viz_data/consumption_reduced/Scene",
)


model = m.Model()
model.add_viz_output(viz_output)

synapse_cylinder = m.GeometryObject(
    name="synapse_cleft",
    vertex_list=synapse_cylinder_vertex_list,
    wall_list=synapse_cylinder_walls_list,
)
synapse_cylinder.is_bngl_compartment = True

model.add_geometry_object(synapse_cylinder)
model.config.time_step = 1e-9

# model.load_bngl("./neurotransmitter.bngl")

nt = m.Species(name="nt", diffusion_constant_3d=D)

release_site_nt = m.ReleaseSite(
    name="rel_nt",
    complex=nt,
    location=(0, 0, synapse_width / 1000),
    number_to_release=5200,
)

nt_consumption = m.ReactionRule(
    name="nt_consumption", reactants=[nt], products=[], fwd_rate=1e6
)

model.add_species(nt)
model.add_release_site(release_site_nt)
model.add_reaction_rule(nt_consumption)

model.initialize()

model.export_viz_data_model()

model.run_iterations(2000)
model.end_simulation()
