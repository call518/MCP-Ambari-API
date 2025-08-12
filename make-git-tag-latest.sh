#!/bin/bash

PRE_TAG=$(git tag | tail -n1)

NEW_TAG=$(date +"%Y.%m.%d.%H.%M.%S")
NEW_MSG=$(git log "${PRE_TAG}"..HEAD --pretty=format:"%s (%h)")

git tag -a ${NEW_TAG} -m "${MSG}"
git push origin ${NEW_TAG}
