import os
import io
import boto3
import json
import base64
from cgi import parse_header, parse_multipart
from io import BytesIO

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
    data = json.loads(json.dumps(event))
    payload = data['body']
    raw_form_data = base64.b64decode(payload)

    c_type, c_data = parse_header(event['headers']['content-type'])
    assert c_type == 'multipart/form-data'
    decoded_string = base64.b64decode(event['body'])
    
    #For Python 3: these two lines of bugfixing are mandatory
    #see also: https://stackoverflow.com/questions/31486618/cgi-parse-multipart-function-throws-typeerror-in-python-3
    c_data['boundary'] = bytes(c_data['boundary'], "utf-8")
    c_data['CONTENT-LENGTH'] = event['headers']['content-length']
    form_data = parse_multipart(BytesIO(decoded_string), c_data)
    
    img = form_data.get('body')
    img_bytes = bytes(img[0])
    
    try:
        response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,ContentType='image/jpeg',Body=img_bytes)
        print(response)
        r = response["Body"].read()
        print(r)
        return r
    except Exception as e:
        print("Inference Error:")
        print(e)
        return []
    
