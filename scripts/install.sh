#!/usr/bin/env bash
# Install the Unity CLI (beta) and, optionally, add the pipeline package to a project.
#
#   ./scripts/install.sh                 # install the CLI only
#   ./scripts/install.sh <project-path>  # install the CLI and add com.unity.pipeline to the project
#
# The CLI and the com.unity.pipeline package are experimental; expect churn between versions.

set -euo pipefail

echo "==> Installing the Unity CLI (beta channel)"
curl -fsSL https://public-cdn.cloud.unity3d.com/hub/prod/cli/install.sh | UNITY_CLI_CHANNEL=beta bash

if ! command -v unity >/dev/null 2>&1; then
  echo "!! 'unity' is not on PATH yet. Open a new shell (or source your profile), then re-run." >&2
  exit 1
fi

echo "==> Unity CLI version:"
unity --version

PROJECT="${1:-}"
if [[ -n "$PROJECT" ]]; then
  echo "==> Adding com.unity.pipeline to: $PROJECT"
  unity pipeline install --project-path "$PROJECT"
  echo "==> Done. Launch a headless editor with:"
  echo "    Unity -batchmode -projectpath \"$PROJECT\" -logFile editor.log"
  echo "    (no -quit; leave it running, then use 'unity command --project-path \"$PROJECT\"')"
else
  echo "==> CLI installed. To wire a project up, re-run with its path:"
  echo "    ./scripts/install.sh /path/to/your/project"
fi
