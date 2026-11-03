#!/usr/bin/env bash
# Build the PUBLIC SNAPSHOT: a brand-new, single-commit repo made from `git archive HEAD`, redacted and scanned (T-194).
# Publish ONLY from this snapshot, never from the working repo or its history (see deploy/SNAPSHOT.md).
#
#   bash deploy/make_public_snapshot.sh            # snapshot goes to a fresh mktemp dir outside the repo
#   SNAPSHOT_DIR=/some/new/dir bash deploy/make_public_snapshot.sh
#
# Needs the LOCAL, git-ignored deploy/.private_patterns (private values to scan for; never committed). Create it once with
#   python3 deploy/snapshot_tool.py init-patterns .
# The script stops with a clear message if it is missing.
# Prints SNAPSHOT_PATH=<dir> on success; exits nonzero (and says so) if redaction, the strict scan or check_secrets fails.
# Never pushes, never adds a remote, never reads .env, never touches the real repo's history or config.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
AUTHOR_NAME="Chris Borsheim"
AUTHOR_EMAIL="cborsheim@gmail.com"

TOOL="$HERE/snapshot_tool.py"
PATTERNS="${SNAPSHOT_PATTERNS:-$HERE/.private_patterns}"
if [ ! -s "$PATTERNS" ]; then
  python3 -B -I "$TOOL" scan /nonexistent-nothing-built >&2 || exit 2   # prints the "patterns file is missing" explanation, exit 2
fi
if [ -n "$(git -C "$REPO" ls-files -- deploy/.private_patterns)" ] || [ -n "$(git -C "$REPO" ls-files "$PATTERNS" 2>/dev/null)" ]; then
  echo "refusing: the private patterns file is tracked by git; remove it from the index (git rm --cached) first" >&2; exit 2
fi

SNAP="${SNAPSHOT_DIR:-$(mktemp -d "${TMPDIR:-/tmp}/zlayt-public-snapshot.XXXXXX")}"
mkdir -p "$SNAP"
SNAP="$(cd "$SNAP" && pwd -P)"
REPO_REAL="$(cd "$REPO" && pwd -P)"
case "$SNAP/" in "$REPO_REAL"/*) echo "refusing: snapshot dir must be outside the repo ($SNAP)" >&2; exit 2;; esac
if [ -n "$(ls -A "$SNAP")" ]; then echo "refusing: snapshot dir is not empty ($SNAP)" >&2; exit 2; fi

# The snapshot carries only HEAD: uncommitted work is not included (and is not redacted).
if [ -n "$(git -C "$REPO" status --porcelain --untracked-files=no | grep -v '^.. \.claude/agent-memory/' || true)" ]; then
  echo "note: working tree has uncommitted changes; the snapshot is built from HEAD ($(git -C "$REPO" rev-parse --short HEAD)) only" >&2
fi

FAILMSG() { echo "SNAPSHOT FAILED (kept for inspection, do NOT publish): $SNAP" >&2; }
trap FAILMSG ERR

echo "1/6 git archive HEAD ($(git -C "$REPO" rev-parse --short HEAD)) -> $SNAP" >&2
git -C "$REPO" archive HEAD | tar -x -C "$SNAP"

echo "2/6 image allow-list: delete every image/media file outside the allow-list" >&2
python3 -B -I "$TOOL" prune "$SNAP" >&2

echo "2b/6 Chris's own words: drop board/inbox/ and the text of his inbox events (MASTER_PROMPT.md is the one thing kept)" >&2
python3 -B -I "$TOOL" drop-chris "$SNAP" >&2
test -s "$SNAP/MASTER_PROMPT.md" || { echo "refusing: MASTER_PROMPT.md is missing from the snapshot" >&2; exit 2; }

echo "3/6 redaction (generic tailnet shapes + the local private patterns + secret patterns)" >&2
python3 -B -I "$TOOL" redact "$SNAP" >&2

# git: isolated from every user/system config and hook; identity only via env for this one commit.
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME="$AUTHOR_NAME" GIT_AUTHOR_EMAIL="$AUTHOR_EMAIL" GIT_COMMITTER_NAME="$AUTHOR_NAME" GIT_COMMITTER_EMAIL="$AUTHOR_EMAIL"
G=(git -C "$SNAP" -c core.hooksPath=/dev/null -c commit.gpgsign=false -c core.autocrlf=false)

echo "4/6 git init + one commit as $AUTHOR_NAME <$AUTHOR_EMAIL>" >&2
"${G[@]}" init -q -b main
"${G[@]}" add --all
"${G[@]}" commit -q -m "Zlayt PM treatment-timeline prototype: public snapshot" --no-verify

echo "5/6 strict scan + history check" >&2
FAIL=0
test "$("${G[@]}" status --porcelain | wc -l | tr -d ' ')" = "0" || { echo "FAIL: snapshot tree differs from its commit" >&2; FAIL=1; }
python3 -B -I "$TOOL" scan "$SNAP" || FAIL=1
# second, independent normalized scan with QA's tool (T-187 r4): same terms, its own view, so a miss in one is caught by the other
python3 -B -I "$REPO/evals/privacy_tree_scan.py" --dir "$SNAP" || FAIL=1
N="$("${G[@]}" rev-list --count HEAD)"
IDS="$("${G[@]}" log --format='%an <%ae>%n%cn <%ce>' | sort -u)"
if [ "$N" != "1" ] || [ "$IDS" != "$AUTHOR_NAME <$AUTHOR_EMAIL>" ]; then
  echo "FAIL: expected exactly 1 commit by $AUTHOR_NAME <$AUTHOR_EMAIL>; got $N commit(s), identities: $IDS" >&2; FAIL=1
else
  echo "history: 1 commit, author and committer $AUTHOR_NAME <$AUTHOR_EMAIL>; remotes: $("${G[@]}" remote | wc -l | tr -d ' ')"
fi

echo "6/6 tools/check_secrets.py on the snapshot" >&2
python3 -B -I "$SNAP/tools/check_secrets.py" || FAIL=1

if [ "$FAIL" != "0" ]; then
  trap - ERR
  FAILMSG
  exit 1
fi
echo "SNAPSHOT_PATH=$SNAP"
