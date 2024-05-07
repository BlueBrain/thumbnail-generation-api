"""NeuroMorphoVis soma reconstruction module."""

import os
import sys

import bpy

import nmv.builders
import nmv.consts
import nmv.enums
import nmv.file
import nmv.interface
import nmv.options
import nmv.rendering
import nmv.scene
from api.utils import logger

# Append the internal modules into the system paths to avoid Blender importing conflicts
import_paths = ["neuromorphovis"]
for import_path in import_paths:
    path = "%s/../../.." % (os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(path)


def render_soma_two_dimensional_profile(morphology_object, options):
    """Reconstruct the skeleton of the two-dimensional soma profile and render it.

    :param morphology_object:
        A given morphology object.
    :param options:
        NeuroMorphoVis options
    """

    # Clear the scene
    nmv.scene.ops.clear_scene()


def reconstruct_soma_three_dimensional_profile_mesh(cli_morphology, cli_options):
    """Reconstructs a three-dimensional profile of the soma and renders it.

    :param cli_morphology:
        The morphology loaded from the command line interface (CLI).
    :param cli_options:
        System options parsed from the command line interface (CLI).
    :return
        A mesh that represents the reconstructed three-dimensional profile of the morphology.
    """

    # Clear the scene
    nmv.scene.ops.clear_scene()

    # Create a soma builder object
    soma_builder = nmv.builders.SomaSoftBodyBuilder(cli_morphology, cli_options)

    # Reconstruct the three-dimensional profile of the soma mesh
    soma_mesh = soma_builder.reconstruct_soma_mesh()

    # Soma mesh file prefix
    soma_mesh_file_name = "SOMA_MESH_%s" % cli_options.morphology.label

    # Export the mesh

    nmv.scene.ops.deselect_all()
    nmv.scene.ops.set_active_object(soma_mesh)

    output_file_path = "%s/%s%s" % (
        cli_options.io.meshes_directory,
        str(soma_mesh_file_name),
        ".glb",
    )

    print("Exporting .glb to", output_file_path)

    bpy.ops.export_scene.gltf(
        filepath=output_file_path,
        check_existing=False,
        export_format="GLB",
        export_image_format="NONE",
        export_texcoords=False,
        export_normals=False,
        export_draco_mesh_compression_level=6,
        export_materials="NONE",
        export_attributes=False,
        use_selection=True,
        export_yup=True,
        export_animations=False,
        export_lights=False,
    )

    # Render a static frame of the reconstructed soma mesh
    if cli_options.rendering.render_soma_static_frame:
        # Image name (for a front view only)
        image_name = "SOMA_MESH_%s_%s" % (
            nmv.enums.Camera.View.FRONT,
            cli_options.morphology.label,
        )

        # Render the image
        nmv.rendering.SomaRenderer.render(
            view_extent=cli_options.soma.rendering_extent,
            camera_view=cli_options.soma.camera_view,
            image_resolution=cli_options.soma.rendering_resolution,
            image_name=image_name,
            image_directory=cli_options.io.images_directory,
        )

    # Render a 360 sequence of the soma mesh
    if cli_options.rendering.render_soma_360:
        # Create the sequences directory if it does not exist
        if not nmv.file.ops.path_exists(cli_options.io.sequences_directory):
            nmv.file.ops.clean_and_create_directory(cli_options.io.sequences_directory)

        # Create a specific directory for this mesh
        output_directory = "%s/SOMA_MESH_360_%s" % (
            cli_options.io.sequences_directory,
            cli_options.morphology.label,
        )
        nmv.file.ops.clean_and_create_directory(output_directory)

        # Render the frames
        for i in range(360):
            # Set the frame name
            image_name = "%s/%s" % (output_directory, "{0:05d}".format(i))

            # Render a frame
            nmv.rendering.SomaRenderer.render_at_angle(
                soma_mesh=soma_mesh,
                angle=i,
                view_extent=cli_options.soma.rendering_extent,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=cli_options.soma.rendering_resolution,
                image_name=image_name,
            )

    # Render a progressive reconstruction of the soma
    if cli_options.rendering.render_soma_progressive:
        # Clear the scene to do the reconstruction again while rendering the frames
        nmv.scene.ops.clear_scene()

        # Create a specific directory for this mesh
        output_directory = "%s/SOMA_MESH_PROGRESSIVE_%s" % (
            cli_options.io.sequences_directory,
            cli_options.morphology.label,
        )
        nmv.file.ops.clean_and_create_directory(output_directory)

        # Simulation
        for i in range(nmv.consts.Simulation.MIN_FRAME, nmv.consts.Simulation.MAX_FRAME):
            # Update the frame based on the soft body simulation
            bpy.context.scene.frame_set(i)

            # Set the frame name
            image_name = "%s/%s" % (output_directory, "{0:05d}".format(i))

            # Render a frame
            nmv.rendering.SomaRenderer.render_at_angle(
                soma_mesh=soma_mesh,
                angle=i,
                view_extent=cli_options.soma.rendering_extent,
                camera_view=nmv.enums.Camera.View.FRONT,
                image_resolution=cli_options.soma.rendering_resolution,
                image_name=image_name,
            )

        # Clear the scene again
        nmv.scene.ops.clear_scene()


# Run the main function if invoked from the command line.
if __name__ == "__main__":
    # Ignore blender extra arguments required to launch blender given to the command line interface
    args = sys.argv
    sys.argv = args[args.index("--") + 1 :]

    # Parse the command line arguments, filter them and report the errors
    arguments = nmv.interface.cli.parse_command_line_arguments()

    # Verify the output directory before screwing things !
    if not nmv.file.ops.path_exists(arguments.output_directory):
        logger.error("Please set the output directory to a valid path")
        exit(0)
    else:
        print("Output: [%s]" % arguments.output_directory)

    # Get the options from the arguments
    cli_options = nmv.options.NeuroMorphoVisOptions()

    # Convert the CLI arguments to system options
    cli_options.consume_arguments(arguments=arguments)

    # Read the morphology
    cli_morphology = None

    # If the input is a GID, then open the circuit and read it
    if arguments.input == "gid":
        # Load the morphology from the file
        loading_flag, cli_morphology = nmv.file.BBPReader.load_morphology_from_circuit(
            blue_config=cli_options.morphology.blue_config,
            gid=cli_options.morphology.gid,
        )

        if not loading_flag:
            logger.error(
                "Cannot load the GID [%s] from the circuit [%s]",
                cli_options.morphology.blue_config,
                cli_options.morphology.gid,
            )
            exit(0)

    # If the input is a morphology file, then use the parser to load it directly
    elif arguments.input == "file":
        # Read the morphology file
        cli_morphology = nmv.file.read_morphology_from_file(options=cli_options)

        if cli_morphology is None:
            logger.error(
                "Cannot load the morphology file [%s]",
                cli_options.morphology.morphology_file_path,
            )
            exit(0)

    else:
        logger.error("Invalid input option")
        exit(0)

    # Soma mesh reconstruction and visualization
    reconstruct_soma_three_dimensional_profile_mesh(cli_morphology=cli_morphology, cli_options=cli_options)
    logger.info("NMV Done")
