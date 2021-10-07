#!/bin/bash
image=$1
if [ "$image" == "" ]
then
    echo "Usage: $0 <image-name>"
    exit 1
fi
account=$(aws sts get-caller-identity --query Account --output text)
region=$(aws configure get region)
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"

aws ecr describe-repositories --repository-names "${image}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${image}" > /dev/null
fi

# Get the login command from ECR and execute it directly (for our own registry and for the base image registry)
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${account}.dkr.ecr.${region}.amazonaws.com

base_img='pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime'
echo 'base_img:'$base_img

# Build the docker image locally and then push it to ECR with the full name.
cd container
echo "Building image with name ${image}"
docker build --no-cache -t ${image} -f Dockerfile --build-arg BASE_IMG=$base_img .
docker tag ${image} ${fullname}

echo "Pushing image to ECR ${fullname}"
docker push ${fullname}

# Writing the image name to let the calling process extract it without manual intervention:
echo "${fullname}" > ecr_image_fullname.txt
