# Store data as a file in a format specified in the input 

def save_as_file(formats, df, path, filename):
    if formats:
        file_type = formats["type"].lower()
        delimiter = formats.get("delimiter")
        extension = formats.get("extension").lower()

        if file_type == "excel":
            df.to_excel(path + filename + "." + extension, sep=delimiter, index=False)

        elif file_type == "parquet":
            df.to_parquet(path + filename + "." + extension, index=False)

        else:
            df.to_csv(path + filename + "." + extension, sep=delimiter, index=False)
    else:
        df.to_csv(path + filename + ".csv", index=False)
