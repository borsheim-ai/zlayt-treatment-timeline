#!/bin/sh
# Publish the demo to a Hugging Face Docker Space as a clean one-commit snapshot (no board, memory, reviews, .claude or history).
#   deploy/hf_push.sh <hf-username>/<space-name>
# Prerequisites: the Space already exists (SDK: Docker) and git can authenticate to huggingface.co
# (username + a write-scoped access token as the password, or `hf auth login` / a git credential helper).
# This script never reads, takes or prints a token. It force-pushes the snapshot to the Space's main branch.
set -eu
[ $# -eq 1 ] || { echo "usage: deploy/hf_push.sh <hf-username>/<space-name>" >&2; exit 2; }
SPACE="$1"
cd "$(dirname "$0")/.."
git diff --quiet HEAD -- Dockerfile .dockerignore README.md requirements.txt app evals tests/fixtures/llm || { echo "Uncommitted changes in shipped paths; commit first (the snapshot is taken from HEAD)." >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
# Same allow-list as .dockerignore, taken from HEAD so untracked/ignored files (.env, databases) can never ride along.
git archive HEAD Dockerfile .dockerignore requirements.txt app evals/golden evals/library evals/reports/calibration.json tests/fixtures/llm | tar -x -C "$TMP"
rm -f "$TMP/app/llm/backends/claude_cli.py"     # .dockerignore excludes it too: the shipped image never contains the CLI backend (CONTRACT section 10)
cat deploy/hf_space_frontmatter.yml README.md > "$TMP/README.md"

# Refuse to publish if anything key-shaped slipped in.
if grep -rIlE 'sk-ant-[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{30,}' "$TMP" >/dev/null 2>&1; then
  echo "Refusing to push: a key-shaped string is in the snapshot." >&2; exit 1
fi

cd "$TMP"
git init -q -b main
git add -A
git -c user.name="release" -c user.email="release@example.invalid" commit -q -m "Deploy demo snapshot"
git remote add space "https://huggingface.co/spaces/$SPACE"
git push --force space main
echo "Pushed. Build logs: https://huggingface.co/spaces/$SPACE (Logs tab). Live at https://huggingface.co/spaces/$SPACE"
