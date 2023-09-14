import paramiko
import os
import boto3
import json


def check_count(dirpath):
    count = 0
    for path in os.scandir(dirpath):
        if path.is_file():
            count += 1
    return count


def sftp_connection(host, port, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, port=port, username=username, password=password)
        print('sftp connection established successfully....')
        ftp = ssh_client.open_sftp()
        return ftp
    except Exception as err:
        print(err)


def s3_connection(region_name, access_key_id, secret_access_key):
    try:
        s3_conn = boto3.resource(
            service_name='s3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)
        print('s3 connection established successfully....')
        return s3_conn
    except Exception as err:
        print(err)


def add_to_sftp(dirpath, file, ftp_conn):
    ftp_conn.put(dirpath + "\\" + file, f"/uploads/CM/Test/{file}")


def add_to_s3(s3_conn, dirpath, file):
    folder_name = "7DD/Test/"
    file_path = dirpath + "/" + file
    s3_conn.Bucket("s3samplebkt").upload_file(file_path, folder_name + file)


def add_file_to_remote_location(dirpath, host, port, username, password, region_name, access_key_id, secret_access_key):
    ftp_conn = sftp_connection(host, port, username, password)
    s3_conn = s3_connection(region_name, access_key_id, secret_access_key)
    if check_count(dirpath) == 10:
        file_count = 0
        for file in os.listdir(dirpath):
            if file_count < 7:
                add_to_s3(s3_conn, dirpath, file)
                # print(file)
                file_count += 1
            else:
                # print(file)
                add_to_sftp(dirpath, file, ftp_conn)
        ftp_conn.close()
    else:
        exit("In sufficient files")


def get_path(directory_path):
    get_inputs(directory_path)


def get_inputs(directory_path):
    with open("Config_Files\\remote_details.json", "r") as f:
        try:
            creds = json.load(f)
            host = creds["sftp_host"]
            port = creds["port"]
            username = creds["username"]
            password = creds["password"]
            region_name = creds["region_name"]
            access_key_id = creds["access_key_id"]
            secret_access_key = creds["secret_access_key"]
            add_file_to_remote_location(directory_path, host, port, username, password, region_name, access_key_id, secret_access_key)
        except json.JSONDecodeError:
            print("Invalid JSON format. Please modify the input.")




