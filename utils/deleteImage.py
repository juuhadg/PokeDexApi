import boto3
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from decouple import config
from urllib.parse import urlparse

AWS_ACCESS_KEY_ID=config('AWS_ACCESS_KEY_ID', "")
AWS_SECRET_ACCESS_KEY=config('AWS_SECRET_ACCESS_KEY', "")

def delete_image_from_s3(url:str, bucket_name: str) -> str:
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY) 

        file_name = urlparse(url).path[1:]


        s3.delete_object(Bucket=bucket_name, Key=file_name)

        
        return "success"
    except:
        return "error" 
