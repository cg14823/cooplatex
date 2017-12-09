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
    
    reqUrl = os.environ['COMPILER_HOST']+"/compile/"
    payload = json.dumps({"uid":ownerID, "projectName":projectName})
    headers ={"X-Compiler-Token":str(os.environ['COMPILER_SECRET_KEY'])}
    res = requests.post(reqUrl, headers=headers, payload=payload)
    print(res)
    print(res.status_code)
    json_data = json.loads(res.text)
    print(json_data)
    if res.status_code == 200:
        return True, json_data['FileName']
    else:
        return False ,{"status": res.status_code}
    
    return False, ""