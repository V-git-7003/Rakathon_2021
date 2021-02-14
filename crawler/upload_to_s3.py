import logging
import boto3
import os,fnmatch
from botocore.exceptions import ClientError


def upload_file(bucket):
    cwd = os.getcwd()
    path_of_dir = format(cwd)
    get_all_file = find("*.json",path_of_dir.replace("/src","/files"))
    s3_client = boto3.client('s3')
    try:
        for file_name in get_all_file:
            length = len(file_name.split("/"))
            object_name = str(file_name.split("/")[length-1])
            response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result
