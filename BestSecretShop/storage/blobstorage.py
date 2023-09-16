import logging
import json

import pandas as pd

from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobClient

from BestSecretShop.credentials import CONNECTION_STRING


class AzureBlobStorage:

    logger = logging.getLogger("AzureBlobStorage")
    CONNECTION_STRING = CONNECTION_STRING

    @classmethod
    def list_container(cls, container):
        try:
            container_client = ContainerClient.from_connection_string(cls.CONNECTION_STRING, container)
            blob_list = container_client.list_blobs()
            for blob in blob_list:
                print(f"Name: {blob.name}")
        except BaseException as err:
            cls.logger.error(f'{container} can`t be displayed. Err message: {err}')


    @classmethod
    def delete_blob(cls, container, blob):
        try:
            blob_client = BlobClient.from_connection_string(cls.CONNECTION_STRING, container, blob, snapshot=None)
            blob_client.delete_blob()
            logging.info(f'{blob} Succesfully deleted.')
        except BaseException as err:
            cls.logger.error(f'{blob} can`t delete. Err message: {err}')


    @classmethod
    def get_latest_blob(cls, container):
        try:
            container_client = ContainerClient.from_connection_string(cls.CONNECTION_STRING, container)
            blob_list = container_client.list_blobs()
            blob_name = []
            blob_creation_time = []

            for blob in blob_list:
                blob_name.append(blob.name)
                blob_creation_time.append(blob.creation_time)

            df = pd.DataFrame({"name": blob_name, "date": blob_creation_time})
            df = df.sort_values(by="date")
            blob_name = df["name"][df.last_valid_index()]
            cls.logger.info('Latest Blob: {}'.format(blob_name))
            return blob_name
        
        except BaseException as err:
            cls.logger.error(f'{container} Err message: {err}')
            

    @classmethod
    def download_blob_as_string(cls, container, blob):
        try:
            blob_client = BlobClient.from_connection_string(cls.CONNECTION_STRING, container, blob)

            download_stream = blob_client.download_blob()
            return download_stream.readall().decode('utf-8')
        
        except BaseException as err:
            cls.logger.error(f'{container, blob} can`t be downloaded. Err message: {err}')
            
    
    @classmethod
    def download_blob_to_file(cls, container, blob, path):
        try:
            blob_client = BlobClient.from_connection_string(cls.CONNECTION_STRING, container, blob)

            with open(path, mode="wb") as sample_blob:
                download_stream = blob_client.download_blob()
                sample_blob.write(download_stream.readall())
                logging.info('Download Blob({}) to GTIN.csv succesfully.'.format(blob))
        
        except BaseException as err:
            cls.logger.error(f'{container, blob} can`t be downloaded to {path}. Err message: {err}')


    @classmethod
    def upload_file_to_blobstorage(cls, container, dest_blob, file_path):
        try:
            blob_client = BlobClient.from_connection_string(cls.CONNECTION_STRING, container, dest_blob)
            blob_client.create_append_blob()
            
            #upload 4 MB for each request
            chunk_size = 4 * 1024 * 1024
            with open(file_path, "rb") as stream:
                while True:
                    read_data = stream.read(chunk_size)
                    
                    if not read_data:
                        logging.info('uploaded')
                        break 
                    blob_client.append_block(read_data)

        except BaseException as err:
           cls.logger.error(f' Data can`t be uploaded to {container, dest_blob}. Err message: {err}')


    @classmethod
    def upload_json_object_to_blobstorage(cls, container, dest_blob, json_object):
        
        try:
            blob_client = BlobClient.from_connection_string(cls.CONNECTION_STRING, container, dest_blob)
            blob_client.create_append_blob()
            
            stream = json.dumps(json_object).encode('utf-8')

            #upload 4 MB for each request
            chunk_size = 4 * 1024 * 1024
            while True:
                read_data = stream.read(chunk_size)
                
                if not read_data:
                    logging.info('uploaded')
                    break 
                blob_client.append_block(read_data)

        except BaseException as err:
           cls.logger.error(f' Data can`t be uploaded to {container, dest_blob}. Err message: {err}')
        pass
