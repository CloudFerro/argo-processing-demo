import os
import fnmatch
import boto3
from datetime import datetime
import logging
import time
import traceback
import sys

logging.basicConfig(level=logging.INFO)

try:
    volume_path = '/workspace/'
    area = sys.argv[1]

    access_key = os.getenv('PRIVATEACCESSKEY')
    secret_key = os.getenv('PRIVATESECRETKEY')

    host = 'https://s3.waw3-1.cloudferro.com'
    s3_resource = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, endpoint_url=host)
    s3_client = s3_resource.meta.client

    # Modify bucket name patter (!). Buckets on WAW3-1 cloud need to have unique names across all users. 
    private_bucket_name = 'argoprocessing_CF_' + area + "_" + datetime.now().strftime('%Y-%m-%d')
    s3_client.create_bucket(Bucket=private_bucket_name)

    for safe_folder in os.listdir(volume_path):
        if safe_folder.endswith(".SAFE"):
            safe_path = volume_path + safe_folder
            granule_path = safe_path + '/GRANULE/'
            logging.warning(granule_path)
            granule_child_folder_name = list(os.walk(granule_path))[0][1][0]
            R10m_folder_path = os.path.join(granule_path, granule_child_folder_name, 'IMG_DATA', 'R10m/')
            band_paths = []
            for file in os.listdir(R10m_folder_path):
                if (fnmatch.fnmatch(file, '*B02_10m.jp2') | fnmatch.fnmatch(file, '*B03_10m.jp2') | fnmatch.fnmatch(file, '*B04_10m.jp2')):
                    band_paths.append(R10m_folder_path + file)
            merged_file_name = safe_folder[:-5] + '_RGB.tif'
            merged_file_path = volume_path + merged_file_name
            gdal_command = 'gdal_merge.py -separate -o ' + merged_file_path + ' -co PHOTOMETRIC=MINISBLACK ' + band_paths[0] + ' ' + band_paths[1] + ' ' + band_paths[2]
            os.system(gdal_command)
            s3_client.upload_file(merged_file_path, private_bucket_name, merged_file_name)
            
except Exception as e:
    logging.error(traceback.format_exception(*sys.exc_info()))
    time.sleep(90)