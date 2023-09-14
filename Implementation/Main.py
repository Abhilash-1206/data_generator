import pandas as pd
from datetime import datetime
import json
import Generate_Data
import Save_as_File
import Save_as_Table
import Files_to_Remote_Location


def schemas_as_input():
    path = "7DD"
    with open("Config_Files\\config_7DD.json", "r") as f:
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

                # Creating a separate csv file for each schema
                Save_as_File.save_as_file(formats, df, path, filename)

                # Storing data in a table
                Save_as_Table.save_as_table(db_type, df, filename)

            # storing the generated files in the remote locations
            
            Files_to_Remote_Location.get_path(path)
            print("completed...")

        except json.JSONDecodeError:
            print("Invalid JSON format. Please modify the input.")


if __name__ == "__main__":
    schemas_as_input()
