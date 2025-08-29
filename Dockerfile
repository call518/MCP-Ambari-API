# This Dockerfile is exclusively for smithery.ai.

FROM rockylinux:9.3

ARG PYTHON_VERSION=3.11

# Base dependencies
RUN dnf install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-pip git && dnf clean all \
        && update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1000 --slave /usr/bin/pip pip /usr/bin/pip${PYTHON_VERSION}

WORKDIR /app

RUN pip install mcp-ambari-api

#EXPOSE 8000

#CMD ["mcp-ambari-api", "--type", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]

CMD ["sh","-lc","exec mcp-ambari-api --type streamable-http --host 0.0.0.0 --port ${PORT:-8000}"]
