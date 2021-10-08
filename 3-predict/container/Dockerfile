ARG BASE_IMG=${BASE_IMG}
FROM ${BASE_IMG}

# Set a docker label to advertise multi-model support on the container
LABEL com.amazonaws.sagemaker.capabilities.multi-models=true
# Set a docker label to enable container to use SAGEMAKER_BIND_TO_PORT environment variable if present
LABEL com.amazonaws.sagemaker.capabilities.accept-bind-to-port=true

RUN apt-get update \
 && apt-get install -y --no-install-recommends --allow-unauthenticated \
    build-essential \
    ca-certificates \
    openjdk-8-jdk-headless \
    python3-dev \
    curl \
    vim \
    jq git gcc libgl1-mesa-dev libglib2.0-0 wget \
    && rm -rf /var/lib/apt/lists/* \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py    

RUN ldconfig -v
RUN pip install --upgrade pip
RUN pip install --no-cache torch==1.9.0+cu111 torchvision==0.10.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html

# Install MMS, and SageMaker Inference Toolkit to set up MMS
RUN pip --no-cache-dir install multi-model-server \
                                sagemaker-inference \
                                retrying

# Copy entrypoint script to the image
COPY dockerd-entrypoint.py /usr/local/bin/dockerd-entrypoint.py
RUN chmod +x /usr/local/bin/dockerd-entrypoint.py

RUN mkdir -p /home/model-server/

RUN cd /home/model-server && git clone https://github.com/ultralytics/yolov5
RUN pip install -r /home/model-server/yolov5/requirements.txt

# Define an entrypoint script for the docker image
ENTRYPOINT ["python", "/usr/local/bin/dockerd-entrypoint.py"]

# Define command to be passed to the entrypoint
CMD ["serve"]