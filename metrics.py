import os
import laspy
import glob

def calculate_metrics(las_file, min_height, max_height):
    # Initialize metrics
    total_area_2m = 0.0
    total_area_3m = 0.0
    num_points_2m = 0
    num_points_3m = 0

    for point in las_file.points:
        print(point)
        z_value = 1.0
        if min_height <= z_value <= max_height:
            if z_value <= 2.0:
                total_area_2m += 1
                num_points_2m += 1
            if z_value <= 3.0:
                total_area_3m += 1
                num_points_3m += 1

    # Calculate percentage points below 2m and 3m
    percent_points_2m = (num_points_2m / len(las_file.points)) * 100
    percent_points_3m = (num_points_3m / len(las_file.points)) * 100

    return {
        "total_area_2m": total_area_2m,
        "total_area_3m": total_area_3m,
        "num_points_2m": num_points_2m,
        "num_points_3m": num_points_3m,
        "percent_points_2m": percent_points_2m,
        "percent_points_3m": percent_points_3m,
    }


# Function to create LAS file for specified height range
def create_height_filtered_las(input_las_file, output_las_file, min_height, max_height):
    # Open the input LAS file
    input_las = laspy.file.File(input_las_file)
    output_las = laspy.file.File(output_las_file, mode="w", header=input_las.header)
    for point in input_las.points:
        if min_height <= point.z <= max_height:
            output_las.write(point)

    output_las.close()


# Main program
def process_las_files_in_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    height_ranges = [(0.0, 2.0), (0.0, 3.0)]
    las_files = glob.glob(os.path.join(input_folder, "*.las")) + glob.glob(os.path.join(input_folder, "*.laz"))
    for input_las_file in las_files:
        for min_height, max_height in height_ranges:
            metrics = calculate_metrics(laspy.file.File(input_las_file), min_height, max_height)
            filename = os.path.splitext(os.path.basename(input_las_file))[0]
            output_las_file = os.path.join(
                output_folder, f"{filename}_height_{int(min_height)}_{int(max_height)}.las"
            )
            create_height_filtered_las(input_las_file, output_las_file, min_height, max_height)
            print(f"Metrics for {input_las_file}, {min_height}-{max_height} m height range:")
            print(f"M1 - Area covered: {metrics['total_area_2m']} m^2 / {metrics['total_area_3m']} m^2")
            print(f"M2 - Number of points: {metrics['num_points_2m']} / {metrics['num_points_3m']}")
            print(f"M3 - % of points: {metrics['percent_points_2m']}% / {metrics['percent_points_3m']}%")

    print("LAS files created in the output directory.")

# Main program
if __name__ == "__main__":
    input_folder = "/home/krishnaprasad/Downloads/sample_plots"  # Replace with your input folder
    output_folder = "/home/krishnaprasad/Downloads/sample_plots_all_copy"  # Replace with your output folder

    process_las_files_in_folder(input_folder, output_folder)
