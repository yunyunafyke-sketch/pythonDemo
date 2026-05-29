#!/bin/bash

set -e

echo "==== Git Status ===="
git status

echo ""
echo "==== Git Diff Summary ===="
git diff --stat

MESSAGE=$1

if [ -z "$MESSAGE" ]; then
  echo "Commit message required"
  exit 1
fi

git add .
git commit -m "$MESSAGE"

echo ""
echo "Commit completed successfully"
