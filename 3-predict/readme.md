## SageMaker Endpoint

A sagemaker endpoint is not a REST API. It allows to invoke inference task from AWS SageMaker SDK/CLI

The endpoint creation/deployment can be reviewed in the deploy notebook, but then if you want to have a REST API to call your endpoint from a 3rd party software, you need to add something that will be a proxy of the invokation.

Here you have an example of an AWS Lambda that expose a simple HTTP POST service, and will invoke the SageMaker endpoint with the desired payload (image file/bytes), and will return the inference result.

The AWS Lambda will also require extra configuration to be available from the external world (with AWS API Gateway with Lambda integration)


Then a simple curl request can call this endpoint remotely : 

    curl -v -X POST -F "body=@/path/to/test/image.jpg" https://xxxxxx.execute-api.xxxxx.amazonaws.com/visualsearch-invoker
