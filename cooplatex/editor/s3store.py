"""Filestore use to abstract file creatio to allwo for multuiple file store implementations"""
import datetime
import os
import boto3
import uuid
import requests
from tempfile import NamedTemporaryFile

empty_template="""
\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}

\\title{{{}}}
\\author{{{}}}
\\date{{{}}}

\\begin{{document}}

\\maketitle

\\section{{Introduction}}

\\end{{document}}"""

def create_empty_file(file_name, project_name, owner_name):
    """create_empy_file creates a balnck main.tex file"""
    current_date = datetime.datetime.now()
    datestring = current_date.strftime("%B %Y")
    towrite = empty_template.format(project_name, owner_name, datestring)

    s3 = boto3.resource('s3')
    return s3.Bucket(os.environ["BUCKET_NAME"]).put_object(Key=file_name, Body=towrite.encode())

def create_actual_empty_file(file_name):
    """create_actual_empty_file creates a new bib/tex that is actually empty"""    
    s3 = boto3.resource('s3')
    return s3.Bucket(os.environ["BUCKET_NAME"]).put_object(Key=file_name)

def get_file(file_key):
    s3 = boto3.resource('s3')
    f_uuid = uuid.uuid4()
    f_uuid = str(f_uuid)

    with open(f_uuid, "wb") as f:
        s3.Bucket(os.environ["BUCKET_NAME"]).download_fileobj(file_key, f)
        f.close()

    f = open(f_uuid, "r")
    data = f.read()
    f.close()
    os.remove(f_uuid)
    return data

def save_file(file_name, data, dataType='binary/octet-stream', binary=False):
    s3 = boto3.resource('s3')
    print(file_name)
    #print(data)
    if binary:
        return s3.Bucket(os.environ["BUCKET_NAME"]).put_object(Key=file_name, Body=data, ContentType=dataType)
    return s3.Bucket(os.environ["BUCKET_NAME"]).put_object(Key=file_name, Body=data.encode(), ContentType=dataType)

def get_pdf(pdf_key):
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': os.environ["BUCKET_NAME"],
            'Key': pdf_key
        },
        ExpiresIn=15,
    )
    return url
    #response = requests.get(url)
    #return response