FROM ghcr.io/eclipse-sdv-hackathon-chapter-two/shift2sdv/ecal_base:5.12

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    protobuf-compiler \
    net-tools \
    # add your packages here
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

COPY ecal.ini /etc/ecal/

COPY requirements.txt ./
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

COPY main.py /web_ivi/main.py
COPY static /web_ivi/static

WORKDIR /web_ivi
EXPOSE 5500

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5500"]
