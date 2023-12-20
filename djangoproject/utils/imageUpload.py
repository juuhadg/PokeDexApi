# image_utils.py

import boto3
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from decouple import config

AWS_ACCESS_KEY_ID=config('AWS_ACCESS_KEY_ID', "")
AWS_SECRET_ACCESS_KEY=config('AWS_SECRET_ACCESS_KEY', "")

def upload_image_to_s3(image: InMemoryUploadedFile, bucket_name: str, folder_path: str) -> str: 
    # Configuração do cliente S3
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Nome do arquivo
    file_name = image.name

    # Caminho no bucket S3 onde a imagem será armazenada
    s3_path = f'{folder_path}/{file_name}'

    # Upload da imagem para o S3
    s3.upload_fileobj(BytesIO(image.read()), bucket_name, s3_path)

    # Retorne a URL da imagem no S3
    return f'https://{bucket_name}.s3.amazonaws.com/{s3_path}'
