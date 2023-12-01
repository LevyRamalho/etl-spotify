import boto3
import logging
from botocore.exceptions import ClientError
import os

def conn_S3():
    """ Cria conexão com o S3
        :return s3: Retorna a conexão com o serviço S3
    """
    s3 = boto3.client(
        service_name='s3',
        region_name = 'sa-east-1',
        aws_access_key_id = os.environ.get('AWS_KEY_ID'),
        aws_secret_access_key = os.environ.get('AWS_ACCESS_KEY')
    )

    return s3

def create_bucket(bucket_name, s3_client):
    """ Cria um bucket no s3
        :param bucket_name: Bucket para criar
        :param s3_client: conexão com o client AWS
        :return: TRUE se o bucket for criado, caso não, retorna FALSE

    """
    region_name = 'sa-east-1'
    try:
        # Definindo a Localização
        location = {'LocationConstraint': region_name}
        # Cria o bucket 
        print(f"Criando o Bucket '{bucket_name}'")
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        print(f'O seguinte erro ocorreu durante a execução: {e}')
        return False
    return True

def upload_files_onS3(s3_client, bucket_name, folder_path, folder_name):
    """ Upload os arquivos no S3
        :param s3_client: conexão com o client AWS
        :param bucket_name: Bucket
        :param folder_path: Caminho para a pasta 
        :param folder_name: Nome da pasta 
    """
    try:
        # Tentar encontrar o bucket no S3
        s3_client.head_bucket(Bucket=bucket_name)
    # Verifica caso ocorra erro (Ou seja o bucket não existe, ele chama a função create_bucket())
    except ClientError:
        create_bucket(bucket_name, s3_client)

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            print(f'Uploading {file_name} para {folder_name}')
            with open(file_path, 'rb') as file_data:
                    s3_client.put_object(
                        Bucket=bucket_name,
                        Key=f'{folder_name}/{file_name}',
                        Body= file_data
                    )

    
# Configurações
bucket_name = 'spotify-data-2023'

# Pegando path da pasta do projeto
folder_name = 'data'
folder_path = f'{os.getcwd()}\{folder_name}'

# Conectar ao S3
s3_client = conn_S3()

upload_files_onS3(s3_client, bucket_name, folder_path, folder_name)

fd