FROM rockylinux:9.3

ARG NODE_VERSION=20

COPY Dockerfile /Dockerfile

RUN dnf module install -y nodejs:${NODE_VERSION}

RUN dnf install -y python3.11 python3.11-pip git && dnf clean all

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1000 --slave /usr/bin/pip pip /usr/bin/pip3.11

RUN pip install \
        'mcpo>=0.0.17' \
        'mcp>=1.12.3' \
        'fastmcp>=0.1.0' \
        'uv>=0.8.5' \
        'mcp-server-time>=2025.8.4' \
        'mcp-server-fetch>=2025.1.17' \
        'httpx>=0.28.1' \
        'aiohttp>=3.8.0'

# (Optional) Install Trino MCP Tool (GitHub repository: https://github.com/tuannvm/mcp-trino)
#RUN curl -fsSL https://raw.githubusercontent.com/tuannvm/mcp-trino/main/install.sh -o install.sh && chmod +x install.sh && ./install.sh

RUN mkdir -p /app/config

CMD ["mcpo", "--host", "0.0.0.0", "--port", "8000", "--config", "/app/config/mcp-config.json"]