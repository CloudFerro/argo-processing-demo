import time
import logging
import sys
import os
import boto3
import requests
import traceback

try:
    area = sys.argv[1]
    access_key = os.getenv("EODATAACCESSKEY")
    secret_key = os.getenv("EODATASECRETKEY")
    #host="http://data.cloudferro.com"
    host = "https://s3.cloudferro.com"
    bucket_name = "DIAS"
    api_address = "https://finder.creodias.eu/oldresto/api/collections/Sentinel2/search.json"
    #e.g. https://finder.creodias.eu/resto/api/collections/Sentinel2/search.json?maxRecords=10&q=France&processingLevel=LEVEL2A&startDate=2022-07-01T00%3A00%3A00Z&completionDate=2022-07-01T2
    s3_resource = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, endpoint_url=host)
    s3_client = s3_resource.meta.client
    bucket = s3_resource.Bucket(bucket_name)
    volume_path = "/workspace/"

    parameters = {
        'maxRecords': 50,
        'q': area,
        'processingLevel': 'LEVEL2A',
        'platform': 'S2A',
        'startDate': '2022-07-03T00:00:00Z',
        'completionDate': '2022-07-03T23:59:59Z',
        'sortParam': 'startDate',
        'sortOrder': 'descending'
    }

    response = requests.get(api_address, params=parameters)
    features = response.json()["features"]

    logging.warning(features)

    # download SAFE product
    # https://stackoverflow.com/questions/49772151/download-a-folder-from-s3-using-boto3
    def download_s3_folder(bucket, s3_folder, local_dir=None):
        for obj in bucket.objects.filter(Prefix=s3_folder):
            target = obj.key if local_dir is None \
                else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == '/':
                continue
            bucket.download_file(obj.key, target)

    for feature in features:
        product_path = feature["properties"]["productIdentifier"]
        # print(product_path)
        # /eodata/Sentinel-2/MSI/L2A/2022/07/01/S2B_MSIL2A_20220701T103629_N0400_R008_T32UNF_20220701T122344.SAFE
        prefix = product_path[8:]
        safe_folder = product_path[38:]
        download_s3_folder(bucket, prefix, local_dir= volume_path + safe_folder)

except Exception as e:
    logging.warning(traceback.format_exception(*sys.exc_info()))
    time.sleep(90)

