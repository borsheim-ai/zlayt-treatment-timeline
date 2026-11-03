"""Held-out status of the J3 controls, DERIVED from git and the current prompt (T-113 r2, staff-engineer F1).

A control file can say `split: held_out`, but the label is only a claim. Two controls were called held-out although the judge_conflict_v6 prompt, committed with
them, names their words. The status is therefore computed, from three facts that can be checked:

  written_with_prompt  the control's first commit is also the commit that added a judge_conflict_v<N>.md: it was written with the prompt in view.
  term_in_prompt       a distinguishing word of the control (HELD_TERMS in j3_controls.py) appears in the current judge_conflict prompt text: a hit would measure
                       keyword matching, not generalisation.
  seen_before_edit     the control appeared in an eval report (a run) and a prompt version was added AFTER that report: the prompt could have been tuned with it in view.
  uncommitted          the control is not in git history yet; it becomes `clean` only once committed (commit the controls BEFORE running them).
  clean                none of the above: written separately, its words are not in the prompt, and no prompt edit has followed its first run.

A control committed AFTER the current prompt but before any run of it is `clean` for that prompt: it cannot have shaped it. The next prompt version turns every control that
was run before it into `seen_before_edit`; fresh held-out controls are then written for that version first. CLI: `python -m evals.heldout_audit` prints the table."""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HELD_FILE = "evals/golden/judge_controls_heldout.jsonl"
PROMPTS = "app/llm/prompts"
REPORTS = "evals/reports"
CLEAN, WITH_PROMPT, TERM, SEEN, UNCOMMITTED = "clean", "written_with_prompt", "term_in_prompt", "seen_before_edit", "uncommitted"


def _git(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "git failed")
    return r.stdout


def available() -> bool:
    try:
        _git("rev-parse", "--git-dir")
        return True
    except (RuntimeError, OSError):
        return False


def _first(path, needle):
    """Oldest commit whose diff changes the number of occurrences of `needle` in `path` (git -S), or None."""
    out = _git("log", "--reverse", "--format=%H", "-S", needle, "--", path).split()
    return out[0] if out else None


def current_prompt_name() -> str:
    names = sorted(p.name for p in (ROOT / PROMPTS).glob("judge_conflict_v*.md"))
    return max(names, key=lambda n: int(re.search(r"_v(\d+)", n).group(1)))


def classify(control_commit, report_commit, prompt_add_commits, terms, prompt_text, order):
    """(status, reason). `order` maps commit sha -> position in history (smaller = older). Pure: no git."""
    if control_commit is None:
        return UNCOMMITTED, "not in git history yet: commit the controls before running anything"
    if control_commit in prompt_add_commits:
        return WITH_PROMPT, f"first committed in {control_commit[:9]}, the commit that added a judge_conflict prompt version"
    low = prompt_text.lower()
    hit = [t for t in terms if t.lower() in low]
    if hit:
        return TERM, f"the current prompt contains {hit}"
    if report_commit is not None:
        later = [c for c in prompt_add_commits if order[c] > order[report_commit]]
        if later:
            return SEEN, f"in an eval report ({report_commit[:9]}) before prompt version commit {later[0][:9]}"
    return CLEAN, "written separately, its words are not in the prompt, no prompt edit has followed a run of it"


def audit():
    """[{id, status, reason, terms}] for every held-out J3 control in the committed file. Needs git."""
    from evals.j3_controls import HELD_TERMS
    order = {c: i for i, c in enumerate(_git("log", "--reverse", "--format=%H").split())}
    adds = []
    for p in sorted((ROOT / PROMPTS).glob("judge_conflict_v*.md")):
        out = _git("log", "--reverse", "--format=%H", "--diff-filter=A", "--", f"{PROMPTS}/{p.name}").split()
        adds += out[:1]
    text = (ROOT / PROMPTS / current_prompt_name()).read_text()
    rows = []
    for line in (ROOT / HELD_FILE).read_text().splitlines():
        r = json.loads(line)
        if r["judge"] != "j3":
            continue
        cc = _first(HELD_FILE, f'"id": "{r["id"]}"')
        rc = _first(REPORTS, f"| {r['id']} |")
        terms = HELD_TERMS.get(r["id"], [])
        st, why = classify(cc, rc, set(adds), terms, text, order) if terms else ("no_terms", "no HELD_TERMS entry: add the control's distinguishing words")
        rows.append({"id": r["id"], "status": st, "reason": why, "terms": terms})
    return rows


def summary_lines():
    """Lines for the controls report. Never raises: a missing git checkout says so instead of claiming held-out status."""
    if not available():
        return ["Held-out status was not computed (no git history here); the `held-out` label alone is a claim, not a check."]
    try:
        rows = audit()
    except (RuntimeError, OSError, KeyError, ValueError) as e:
        return [f"Held-out status could not be computed ({e}); the `held-out` label alone is a claim, not a check."]
    clean = [r["id"] for r in rows if r["status"] == CLEAN]
    other = [r for r in rows if r["status"] != CLEAN]
    L = [f"Held-out status is derived from git (evals/heldout_audit.py), not from the label. Clean held-out J3 controls: {len(clean)} of {len(rows)} {clean}. "
         "A control is clean when it was written apart from the prompt, none of its words is in the current prompt, and no prompt version was added after its first run."]
    if other:
        L.append("Not clean: " + "; ".join(f"{r['id']} {r['status']}" for r in other) + ". These are still reported as held-out rows above because they were authored separately; read them as seen.")
    return L


def main():
    if not available():
        print("no git history here"); return 1
    rows = audit()
    for r in rows:
        print(f"{r['id']:7} {r['status']:20} {r['reason']}")
    print(f"clean {sum(r['status'] == CLEAN for r in rows)} of {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    raise SystemExit(main())
