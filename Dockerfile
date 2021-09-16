FROM nvidia/cuda:11.0-runtime-ubuntu20.04
WORKDIR /opt/hashcrack
COPY ./rules/ ./rules/
COPY ./tests/ ./tests/
COPY ./scripts/ ./scripts/
COPY ./test.sh .
COPY ./john/ ./john/
COPY ./hashcat-6.2.2/ ./hashcat-6.2.2/
COPY regmap.cfg .
COPY quickmap.cfg .
COPY map.cfg .
COPY requirements.txt .
COPY ./hashcrack-docker.cfg ./hashcrack.cfg
COPY setup-docker.py .
COPY hashcrack.py .
#Install python
ENV DEBIAN_FRONTEND=noninteractive TZ=Europe/London 
RUN echo "Europe/London" > /etc/timezone \
  && apt-get update \
  && apt-get install -y nvidia-cuda-dev nvidia-opencl-dev clinfo nano python3-impacket openssh-server python3 python3-pip p7zip-full nvidia-headless-470 \
  && python3 -m pip install -r requirements.txt \
  && python3 ./setup-docker.py 
#Define default port
ENTRYPOINT [ "/bin/bash" ]
