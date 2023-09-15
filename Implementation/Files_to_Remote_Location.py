# import all the required packages

import pysftp
import os
import boto3
import json


# Returns the number of files in a specified directory
def check_count(dirpath):
    count = 0
    for path in os.scandir(dirpath):
        if path.is_file():
            count += 1
    return count


# Create a sftp connection to the specified host
def sftp_connection(host, username, password):
    try:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        sftp = pysftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
        print("Connected successfully")
        return sftp
    except Exception as error:
        print(error)


# Creating s3 connection using boto3.resource, which allows the implicit closing of connection
def s3_connection(region_name, access_key_id, secret_access_key):
    try:
        s3_conn = boto3.resource(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)
        print('s3 connection established successfully....')
        return s3_conn
    except Exception as error:
        print(error)


# Adding file to sftp server in the specified path
def add_to_sftp(dirpath, file, ftp_conn):
    ftp_conn.put(dirpath + "\\" + file, f"/uploads/Test/{file}")


# Adding file in the S3 bucket in the specified path
def add_to_s3(s3_conn, dirpath, file):
    folder_name = "Test/"
    file_path = dirpath + "/" + file
    s3_conn.Bucket("s3samplebkt").upload_file(file_path, folder_name + file)


# Create connections to sftp, s3 and add files in them respectively
def add_file_to_remote_location(dirpath, host, username, password, region_name, access_key_id, secret_access_key):
    sftp_conn = sftp_connection(host, username, password)
    s3_conn = s3_connection(region_name, access_key_id, secret_access_key)
    if check_count(dirpath) == 10:
        file_count = 0
        for file in os.listdir(dirpath):
            if file_count < 7:
                add_to_s3(s3_conn, dirpath, file)
                # print(file)
                file_count += 1
            else:
                # =print(file)
                add_to_sftp(dirpath, file, sftp_conn)
        sftp_conn.close()
    else:
        exit("In sufficient files")


# Gets all the required inputs from the config file.
def get_inputs(directory_path):
    with open("C:\\Users\\ak1206\\PycharmProjects\\Automated_Data_Generator\\Config_Files\\remote_details.json",
              "r") as f:
        try:
            creds = json.load(f)
            host = creds["sftp_host"]
            port = creds["port"]
            username = creds["username"]
            password = creds["password"]
            region_name = creds["region_name"]
            access_key_id = creds["access_key_id"]
            secret_access_key = creds["secret_access_key"]
            add_file_to_remote_location(directory_path, host, username, password, region_name, access_key_id,
                                        secret_access_key)
        except json.JSONDecodeError:
            print("Invalid JSON format. Please modify the input.")


# Returns the path where the generated files are stored in the local file system
def get_path(directory_path):
    get_inputs(directory_path)
