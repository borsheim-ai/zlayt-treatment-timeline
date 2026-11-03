"""Flag matching used by evals.run and tests: a port of the reference matcher in evals/golden/check_golden.py
(same type; cites; gap dates; overlapping evidence on every cite.all record; one-to-one maximum bipartite assignment).
check_golden.py is a script (runs on import), so the functions are copied here; tests/unit/test_eval_matching.py pins parity."""
import re


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def overlap(cand_ex, gold_ex):
    """Candidate excerpt must CONTAIN the golden span, or be a fragment of it covering >= 50% of its length."""
    c, g = norm(cand_ex).lower(), norm(gold_ex).lower()
    return bool(c) and bool(g) and (g in c or (c in g and len(c) >= 0.5 * len(g)))


def flag_matches(g, c):
    """g: golden flag; c: candidate {type, evidence:[{record_no, excerpt}], from_date?, to_date?, days?}."""
    if g["type"] != c["type"]:
        return False
    recs_c = {e["record_no"] for e in c["evidence"]}
    if not all(r in recs_c for r in g["cite"]["all"]):
        return False
    if g["cite"]["any"] and not any(r in recs_c for r in g["cite"]["any"]):
        return False
    if g["type"] == "gap":
        return (g["from_date"], g["to_date"], g["days"]) == (c.get("from_date"), c.get("to_date"), c.get("days"))
    for r in g["cite"]["all"]:
        gold = [e["excerpt"] for e in g["evidence"] if e["record_no"] == r and e.get("field", "excerpt") in ("excerpt", "source")]
        if gold and not any(overlap(ce["excerpt"], ge) for ce in c["evidence"] if ce["record_no"] == r for ge in gold):
            return False
    return True


def assign_detail(golden, cands):
    """One-to-one: each candidate satisfies at most one golden flag. Returns (matched golden ids, deduped candidates, indexes of matched candidates)."""
    uniq, seen_ = [], set()
    for c in cands:
        k = (c["type"], tuple(sorted((e["record_no"], norm(e["excerpt"])) for e in c["evidence"])), c.get("from_date"), c.get("to_date"))
        if k not in seen_:
            seen_.add(k)
            uniq.append(c)
    owner = {}

    def try_(gi, seen):
        for ci, c in enumerate(uniq):
            if ci in seen or not flag_matches(golden[gi], c):
                continue
            seen.add(ci)
            if ci not in owner or try_(owner[ci], seen):
                owner[ci] = gi
                return True
        return False

    for gi in range(len(golden)):
        try_(gi, set())
    return {golden[gi]["id"] for gi in owner.values()}, uniq, set(owner)


def assign(golden, cands):
    return assign_detail(golden, cands)[0]
