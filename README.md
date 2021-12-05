# What's in there?

The data for each simulation is available in `viz_data/`.

The code to generate these simulations is in `model_synapse.py`, and the notebook to analyze the results is `analysis_synapse_diffusion.ipynb`.

# Visualizing results

You can use CellBlender to visualize the trajectory.

To do this:

- Make sure you have CellBlender installed (see this [tutorial](https://mcell.org/mcell4_documentation/installation.html))
- start CellBlender with ./my_blender or blender.exe,
- In Blender: File -> Import -> Cellblender Model and Geometry: and select a `Scene.data_model.0000000.json` in one of the simulations folders.
- In View -> Toggle the sidebar.
- In the sidebar, select Cellblender, and select panel Visualization Settings.
- click on Read Viz Data and navigate to directory of the simulation you want to visualize
- click on Play Animation button (Triangle aiming to the right) on the middle bottom of the Blender window.

You should see the animation!
