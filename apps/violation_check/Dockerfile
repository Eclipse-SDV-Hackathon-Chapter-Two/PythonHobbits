FROM ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/ecal_base:5.12

# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install \
#     # add your packages here
#     # Cleanup
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY ecal.ini /etc/ecal/

COPY requirements.txt ./
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

COPY violation_app.py ./
COPY config.json ./

CMD [ "python3", "-u", "./violation_app.py" ]
