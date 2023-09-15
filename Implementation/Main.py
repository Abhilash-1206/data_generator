# import all the packages

import pandas as pd
import json
import Generate_Data
import Save_as_File
import Save_as_Table
import Files_to_Remote_Location


# Reads the config file and gets the required inputs
def schemas_as_input():
    path_to_store_files = "Test_Files\\"
    with open("Config_Files\\config.json", "r") as f:
        try:
            files_data = json.load(f)
            for file_info in files_data:
                filename = file_info["filename"]
                num_rows = file_info["num_rows"]
                schema = file_info["schema"]
                formats = file_info.get("format")
                db_type = file_info.get("db_type")

                # Generate Data for each schema
                df = pd.DataFrame(Generate_Data.generate_random_data(schema, num_rows))

                # Storing data as a file in the specified format
                Save_as_File.save_as_file(formats, df, path_to_store_files, filename)

                # Storing data in a table
                Save_as_Table.save_as_table(db_type, df, filename)

            # storing the generated files in the remote locations
            Files_to_Remote_Location.get_path(path_to_store_files)
            print("completed...")

        except json.JSONDecodeError:
            print("Invalid JSON format. Please modify the input.")


if __name__ == "__main__":
    schemas_as_input()
