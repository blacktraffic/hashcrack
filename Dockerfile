FROM nvidia/cuda:11.7.0-runtime-ubuntu22.04
WORKDIR /opt/hashcrack
COPY ./rules/ ./rules/
COPY ./tests/ ./tests/
COPY ./scripts/ ./scripts/
COPY ./test.sh .
COPY ./john-bleeding-jumbo/ ./john/
COPY ./hashcat-6.2.5/ ./hashcat-6.2.5/
COPY regmap.cfg .
COPY quickmap.cfg .
COPY map.cfg .
COPY requirements.txt .
COPY ./hashcrack-docker.cfg ./hashcrack.cfg
COPY setup-docker.py .
COPY hashcrack.py .
ENV DEBIAN_FRONTEND=noninteractive TZ=Europe/London 
RUN echo "Europe/London" > /etc/timezone \
  && apt-get update \
  && apt-get install -y nvidia-cuda-dev nvidia-opencl-dev clinfo nano python3-impacket openssh-server python3 python3-pip p7zip-full nvidia-headless-510 \
  && python3 -m pip install -r requirements.txt \
  && python3 ./setup-docker.py 
#Define default port
ENTRYPOINT [ "/bin/bash" ]
