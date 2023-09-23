import os
import laspy
import geopandas as gpd
from shapely.geometry import Point
import math

# Define the directory containing the tile LAS files
tile_las_folder = '/home/krishnaprasad/Downloads/output_sample_plots'

# Define the directory containing the SHP file with sample plot data
shp_file_path = '/home/krishnaprasad/Downloads/plots_BPN_2019_selected.shp'

# Define the radius (R) for selecting points
radius = 12.62  # meters

os.environ['SHAPE_RESTORE_SHX'] = 'YES'
# Create a geopandas dataframe from the SHP file

sample_plots = gpd.read_file(shp_file_path)
# Iterate through each sample plot
for index, plot in sample_plots.iterrows():
    plot_geometry = plot['geometry']
    plot_x, plot_y = plot_geometry.x, plot_geometry.y

    # Define a circular buffer around the plot center
    buffer_area = plot_geometry.buffer(radius)

    # Initialize a new LAS file for the sample plot
    new_las_file = laspy.file.File(f"{index}.las", mode='w', header=laspy.header.Header())

    # Iterate through the tile LAS files
    for filename in os.listdir(tile_las_folder):
        if filename.endswith('.las'):
            tile_las_file_path = os.path.join(tile_las_folder, filename)
            with laspy.file.File(tile_las_file_path, mode='r') as tile_las_file:
                # Filter points that fall within the buffer area
                buffer_center = Point(plot_x, plot_y)
                buffer_area = buffer_center.buffer(radius)

                # Select points within the buffer area
                mask = [buffer_area.contains(Point(p)) for p in zip(tile_las_file.x, tile_las_file.y)]
                selected_points = tile_las_file.points[mask]

    # Close the new LAS file
    new_las_file.close()
    # Iterate through the generated LAS files for each sample plot
    for index, plot in sample_plots.iterrows():
        plot_id = plot['geometry']
        plot_area = math.pi * radius ** 2

        # Open the LAS file for the sample plot
        with laspy.file.File(f"{index}.las", mode='r') as plot_las_file:
            num_points = len(plot_las_file.points)
            # Calculate point density
            point_density = num_points / plot_area
            print(f"Plot ID: {plot_id}, Point Density: {point_density} points/square meter")

    # Iterate through the generated LAS files for each sample plot
    for index, plot in sample_plots.iterrows():
        plot_id = plot['geometry']

        # Open the LAS file for the sample plot
        with laspy.file.File(f"{index}.las", mode='r') as plot_las_file:
            # Calculate the minimum height (Z) of all points in the plot
            print(plot_las_file.points)
            min_height = min(plot_las_file.points['point']['Z']) if plot_las_file.points else 1

            # Create a new LAS file for the normalized points
            normalized_las_file = laspy.file.File(f"{index}_normalized.las", mode='w', header=plot_las_file.header)
            plot_points = plot_las_file.points['point']['Z'] if plot_las_file.points else 1
            # Subtract the minimum height from the Z values and save to the new LAS file
            if normalized_las_file.points:
                normalized_las_file.points['point']['Z'] = plot_points - min_height

            # Close the new LAS file
            normalized_las_file.close()
