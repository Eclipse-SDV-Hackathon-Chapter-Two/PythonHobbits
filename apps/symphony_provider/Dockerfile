FROM python:3.12-slim-bookworm

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install \
    git \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY symphony_provider.py ./

CMD [ "python", "-u", "./symphony_provider.py" ]
