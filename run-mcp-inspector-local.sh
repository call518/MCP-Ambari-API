#!/bin/bash

# (NOTE) 로컬 개발 소스로 기동됨 (uv run 사용).

# 현재 스크립트 위치로 이동하여 올바른 작업 디렉토리 설정
cd "$(dirname "$0")"

npx -y @modelcontextprotocol/inspector \
	-e AMBARI_HOST='127.0.0.1' \
	-e AMBARI_PORT=8080 \
	-e AMBARI_USER='admin' \
	-e AMBARI_PASS='admin' \
	-e AMBARI_CLUSTER_NAME='TEST-AMBARI' \
	-e AMBARI_LOG_LEVEL='INFO' \
	-e PYTHONPATH='./src' \
	-- uv run python -m mcp_ambari_api.ambari_api
