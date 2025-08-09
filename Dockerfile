FROM rockylinux:9.3

ARG PYTHON_VERSION=3.11

WORKDIR /app

# Base dependencies
RUN dnf install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-pip git && dnf clean all \
        && update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1000 --slave /usr/bin/pip pip /usr/bin/pip${PYTHON_VERSION}

# Install runtime deps first (better layer caching) then copy and install our package
RUN pip install \
                'mcpo>=0.0.17' \
                'mcp>=1.12.3' \
                'fastmcp>=2.11.1' \
                'uv>=0.8.5' \
                'mcp-server-time>=2025.8.4' \
                'mcp-server-fetch>=2025.1.17' \
                'httpx>=0.28.1' \
                'aiohttp>=3.12.0'

# Copy only the necessary build context to leverage Docker layer cache
COPY pyproject.toml README.md ./
COPY src ./src

# Install our package (provides the console script 'mcp-ambari-api')
RUN pip install .

# Copy config after install so changes to config don't invalidate dependency layers
COPY mcp-config.json /app/config/mcp-config.json

# Ensure config directory exists (COPY creates /app/config file path; directory already present now)
RUN mkdir -p /app/config

EXPOSE 8000

# Run mcpo which will invoke the configured MCP servers (including our installed 'mcp-ambari-api')
CMD ["mcpo", "--host", "0.0.0.0", "--port", "8000", "--config", "/app/config/mcp-config.json"]