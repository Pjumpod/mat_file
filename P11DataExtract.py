import os
import zipfile
import pandas as pd
import datetime
import pathlib


# Define the base directory containing subdirectories with common folder
base_dir = r'\\fab2-fs13.luminartech.com\Departments\advmfg\P1-1'
outputpath = r'C:\output'
if not os.path.exists(outputpath):
  os.makedirs(outputpath)
# Create an empty DataFrame to hold the combined data
combined_df = pd.DataFrame()

# Walk through the directory structure to find 'FULL_CALIBRATION' folders
for root, dirs, files in os.walk(base_dir):
    # Only proceed if the current directory contains 'FULL_CALIBRATION'
    if 'FULL_CALIBRATION' in dirs:
        full_calibration_dir = os.path.join(root, 'FULL_CALIBRATION')
        fname = pathlib.Path(full_calibration_dir)
        ctime = datetime.datetime.fromtimestamp(fname.stat().st_ctime, tz=datetime.timezone.utc)
        if ctime.month == 8:
            # Process each ZIP file in the 'FULL_CALIBRATION' directory and created month is August.
            for file in os.listdir(full_calibration_dir):
                if file.endswith('.zip'):
                    zip_path = os.path.join(full_calibration_dir, file)
                    zip_name = os.path.splitext(file)[0]  # Extract ZIP file name without extension
                    print("==> " + zip_path)
                    try:
                        # Extract ZIP file
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            if 'irisDatabaseRecord.csv' in zip_ref.namelist():
                                # Read the CSV file from the ZIP
                                with zip_ref.open('irisDatabaseRecord.csv') as my_file:
                                    df = pd.read_csv(my_file)
                                    
                                    # Add a new column with the ZIP file name
                                    df['ZipFolderName'] = zip_name
                                    
                                    # Append to the combined DataFrame
                                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                    except Exception as e:
                        print(f"Error processing ZIP file {zip_path}: {e}")

# Save the combined data to a new CSV file
output_csv_path = os.path.join(outputpath,"combined_data_P11_august.csv")
combined_df.to_csv(output_csv_path, index=False)

print(f"Combined data saved to {output_csv_path}")
