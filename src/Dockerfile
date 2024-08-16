FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend .
RUN yarn install && yarn build


FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04 AS backend-build
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:${PATH}"
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app/core
COPY core/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu118


FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:${PATH}"
ENV NODE_VERSION=20.x
RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=backend-build /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY core ./core
COPY --from=frontend-build /app/frontend ./frontend
COPY frontend/package.json frontend/yarn.lock ./frontend/
WORKDIR /app/frontend
RUN yarn install --production
WORKDIR /app
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
EXPOSE 3000 8080
ENTRYPOINT ["./entrypoint.sh"]