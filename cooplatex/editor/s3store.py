"""Filestore use to abstract file creatio to allwo for multuiple file store implementations"""
import datetime
import os
import boto3

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
