import laspy
import os

# Define the path to the LASZ file
folder_path = '/home/krishnaprasad/Downloads/sample_plots_all'

# Define the path for the output LAS file (uncompressed)
output_folder = '/home/krishnaprasad/Downloads/sample_plots_all_copy'
laszip_executable = '/home/krishnaprasad/Downloads/LAStools/bin/las2las.exe'
if not os.path.exists(output_folder):
    print(f"The LASZ file '{output_folder}' does not exist.")
else:
    try:
        # Convert LASZ to LAS using the specified laszip executable
        laszip_command = f"{laszip_executable} -i {folder_path} -o {output_folder}"
        print(laszip_command)
        os.system(laszip_command)

        print(f"Conversion successful: {output_folder} -> {output_folder}")

    except Exception as e:
        print(f"An error occurred during conversion: {str(e)}")