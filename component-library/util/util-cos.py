"""
COS utility functions
"""

# pip install aiobotocore botocore s3fs claimed-c3 tqdm

import os
import s3fs
import logging
import tqdm
from c3.operator_utils import explode_connection_string

# cos_connection in format: [cos|s3]://access_key_id:secret_access_key@endpoint/bucket/path
cos_connection = os.environ.get('cos_connection', None)

# access key id (if cos_connection is not provided)
access_key_id = os.environ.get('access_key_id', None)

# secret access key (if cos_connection is not provided)
secret_access_key = os.environ.get('secret_access_key', None)

# cos/s3 endpoint (if cos_connection is not provided)
endpoint = os.environ.get('endpoint', None)

# cos bucket name (if cos_connection is not provided)
bucket_name = os.environ.get('bucket_name', None)

# cos path (if cos_connection is not provided)
cos_path = os.environ.get('cos_path', None)

# local path
local_path = os.environ.get('local_path')

# recursive
recursive = bool(os.environ.get('recursive', 'True'))

# operation (mkdir|ls|find|download|upload|rm|sync_to_cos|sync_to_local|glob)
operation = os.environ.get('operation')

# Extract values from connection string
if cos_connection is not None:
    (access_key_id, secret_access_key, endpoint, cos_path) = explode_connection_string(cos_connection)
else:
    cos_path = os.path.join(bucket_name, cos_path)

assert access_key_id is not None and secret_access_key is not None and endpoint is not None and cos_path is not None, \
    "Provide a cos_connection (s3://access_key_id:secret_access_key@endpoint/bucket/path) or each value separatly."


def main():
    def print_list(l):
        for file in l:
            print(file)
    
    s3 = s3fs.S3FileSystem(
        anon=False,
        key=access_key_id,
        secret=secret_access_key,
        client_kwargs={'endpoint_url': endpoint}
    )
    
    if operation == 'mkdir':
        logging.info('Make directory ' + cos_path)
        s3.mkdir(cos_path)
    elif operation == 'ls':
        logging.info('List path ' + cos_path)
        print_list(s3.ls(cos_path))
    elif operation == 'find':
        logging.info('Find path ' + cos_path)
        print_list(s3.find(cos_path))
    elif operation == 'upload' and not recursive:
        logging.info('Put path ' + cos_path)
        print(s3.put(local_path,cos_path))
    elif operation == 'download' and not recursive:
        logging.info('Get path ' + cos_path)
        s3.get(cos_path, local_path)
    elif operation == 'rm':
        logging.info('Remove path ' + cos_path)
        s3.rm(cos_path, recursive=recursive)
    elif operation == 'glob':
        logging.info('Glob path ' + cos_path)
        print_list(s3.glob(cos_path))
    elif operation == 'sync_to_cos' or operation == 'upload':
        logging.info(f'{operation} {local_path} to {cos_path}')
        for root, dirs, files in os.walk(local_path, topdown=False):
            # Sync files in current folder
            for name in tqdm.tqdm(files, desc=root):
                file = os.path.join(root, name)
                logging.debug(f'processing {file}')
                cos_file = os.path.join(bucket_name, cos_path,
                                        os.path.relpath(root, local_path), name).replace('/./', '/')
                if operation == 'sync_to_cos' and s3.exists(cos_file):
                    logging.debug(f'exists {cos_file}')
                    logging.debug(f's3.info {s3.info(cos_file)}')
                    if s3.info(cos_file)['size'] != os.path.getsize(file):
                        logging.debug(f'uploading {file} to {cos_file}')
                        s3.put(file, cos_file)
                    else:
                        logging.debug(f'skipping {file}')
                else:
                    logging.debug(f'uploading {file} to {cos_file}')
                    s3.put(file, cos_file)
    elif operation == 'sync_to_local' or operation == 'download':
        logging.info(f'{operation} {cos_path} to {local_path}')
        for root, dirs, files in s3.walk(cos_path):
            # Sync directories in current folder
            for name in dirs:
                local_dir = os.path.join(local_path, os.path.relpath(root, cos_path),
                                         name).replace('/./', '/')
                if not os.path.isdir(local_dir):
                    logging.debug(f'create dir {local_dir}')
                    os.makedirs(local_dir, exist_ok=True, parents=True)
            # Sync files in current folder
            for name in tqdm.tqdm(files, desc=root):
                cos_file = os.path.join(root, name)
                local_file = os.path.join(local_path, os.path.relpath(root, cos_path),
                                          name).replace('/./', '/')
                logging.debug(f'processing {cos_file}')
                if operation == 'sync_to_local' and os.path.isfile(local_file):
                    logging.debug(f'exists {local_file}')
                    logging.debug(f's3.info {s3.info(cos_file)}')
                    if s3.info(cos_file)['size'] != os.path.getsize(local_file):
                        logging.debug(f'downloading {cos_file} to {local_file}')
                        s3.get(cos_file, local_file)
                    else:
                        logging.info(f'Skipping {cos_file}')
                else:
                    logging.debug(f'downloading {cos_file} to {local_file}')
                    s3.get(cos_file, local_file)
    else:
        logging.error(f'Operation unkonwn {operation}')


if __name__ == '__main__':
    main()
