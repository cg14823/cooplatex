import requests
import os
import json

def compile_1_tex_file(ownerID, projectName):
    """ sends a compile request for projects only composed of one tex file.
        this function should return (BOOLEAN, STRING) where the boolean represents
        success of compilation anf the string is the file key in s3
    """

    if (not 'COMPILER_HOST' in os.environ) or (not 'COMPILER_SECRET_KEY' in os.environ):
        return False, ""
    
    reqUrl = os.environ['COMPILER_HOST']+"/compile"
    payload = json.dumps({"uid":str(ownerID), "projectName":projectName})
    headers ={"X-Compiler-Token":str(os.environ['COMPILER_SECRET_KEY']), 'Content-type': 'application/json'}
    res = requests.post(reqUrl, headers=headers, data=payload)
    
    if res.status_code == 200:
        json_data= json.loads(res.text)
        return True, json_data['Filename']
    else:
        return False ,{"status": res.status_code}
    
    return False, ""