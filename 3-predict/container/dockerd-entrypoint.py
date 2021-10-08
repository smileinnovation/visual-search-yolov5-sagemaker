# https://sagemaker-workshop.com/custom/containers.html

import os
import shlex
import subprocess
import sys
from subprocess import CalledProcessError

from retrying import retry
from sagemaker_inference import model_server


def _retry_if_error(exception):
    return isinstance(exception, CalledProcessError or OSError)


@retry(stop_max_delay=1000 * 50, retry_on_exception=_retry_if_error)
def _start_inference_server():
    # by default the number of workers per model is 1, but we can configure it through the
    # environment variable below if desired.
    # os.environ['SAGEMAKER_MODEL_SERVER_WORKERS'] = '2'
    model_server.start_model_server(handler_service="/opt/ml/model/code/model_handler:handle")


def main():
    if len(sys.argv) < 2:
        print("Please specify a command")
    else:
        if sys.argv[1] == "serve":
            _start_inference_server()
        else:
            subprocess.check_call(shlex.split(" ".join(sys.argv[1:])))

        # prevent docker exit
        subprocess.call(["tail", "-f", "/dev/null"])

main()