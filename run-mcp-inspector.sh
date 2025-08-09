#!/bin/bash

# (NOTE) 로컬 소스가 아닌 Pypi에 배포된  패키지로 기동됨.

npx -y @modelcontextprotocol/inspector \
	-e AMBARI_HOST='127.0.0.1' \
	-e AMBARI_PORT=8080 \
	-e AMBARI_USER='admin' \
	-e AMBARI_PASS='admin' \
	-e AMBARI_CLUSTER_NAME='TEST-AMBARI' \
	-- uvx mcp-ambari-api
