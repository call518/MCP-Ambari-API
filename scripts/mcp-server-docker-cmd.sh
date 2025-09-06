#!/bin/bash
set -euo pipefail

# 어디서 실행하든지, 스크립트 위치의 상위 경로에 있는 .env 파일 export 로드
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd -P)"
env_file="${script_dir%/*}/.env"
if [[ -f "$env_file" ]]; then
  set -o allexport
  . "$env_file"
  set +o allexport
else
  echo "error: .env not found: $env_file" >&2
  return 1 2>/dev/null || exit 1
fi

echo "Starting MCP server with:"
echo "  PYTHONPATH: ${PYTHONPATH}"
echo "  FASTMCP_TYPE: ${FASTMCP_TYPE}"
echo "  FASTMCP_HOST: ${FASTMCP_HOST}"
echo "  FASTMCP_PORT: ${FASTMCP_PORT}"
echo "  MCP_LOG_LEVEL: ${MCP_LOG_LEVEL}"
echo "  REMOTE_AUTH_ENABLE: ${REMOTE_AUTH_ENABLE}"
echo "  AMBARI_HOST: ${AMBARI_HOST}"
echo "  AMBARI_PORT: ${AMBARI_PORT}"

python -m mcp_ambari_api --type ${FASTMCP_TYPE} --host ${FASTMCP_HOST} --port ${FASTMCP_PORT}
