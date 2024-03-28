# Base image
FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

# apt update
RUN apt-get update && apt-get dist-upgrade -y

# install package
RUN apt-get install -y build-essential
RUN apt-get install -y wget
RUN apt-get install -y git
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libxrender1
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y libglib2.0-0

# install conda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh
ENV PATH="/opt/miniconda/bin:$PATH"

WORKDIR /root

# Git 클론
RUN git clone https://oauth2:glpat-nHx17XP1jrgxhD4dDu7C@gitlab.surromind.ai/model-card-staging/pointpillars-lidar_road.git

RUN aws s3 cp s3://model-repository/computer-vision/object-detection/pointpillars/36_3_checkpoint_epoch_150.pth /root/pointpillars-lidar_road/output/custom_models/pointpillar_custom_3/36_3/ckpt/36_3_checkpoint_epoch_150.pth --endpoint-url http://10.10.30.41:32295