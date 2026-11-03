#!/usr/bin/env bash
# Re-run the counts quoted in part2-process.md at a commit: bash submission/evidence/count_at.sh 9655f1d
set -euo pipefail
H="${1:?commit}"
cd "$(git rev-parse --show-toplevel)"
echo "reviews    $(git ls-tree -r --name-only "$H" submission/prompt-log/reviews/ | wc -l)"
echo "reports    $(git ls-tree --name-only "$H" evals/reports/ | grep -cE '^evals/reports/[0-9]{8}T')"
echo "decisions  $(git show "$H:memory/ORCHESTRATOR_DECISIONS.md" | grep -oE 'D-[0-9]{3}' | sort -u | wc -l)"
echo "lessons    $(git show "$H:memory/LESSONS.md" | grep -cE '^- ')"
echo "debt rows  $(git show "$H:memory/SCOPE_CUTS.md" | grep -ciE '^\| *debt')"
echo "personas   $(git ls-tree --name-only "$H" personas/ | grep -c '\.md$')"
echo "reqs       $(git show "$H:spec/REQUIREMENTS.md" | grep -oE '^\| *R-[A-Z]+-[0-9]+' | sort -u | wc -l)"
