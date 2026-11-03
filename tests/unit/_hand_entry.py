"""T-165 test helper. lib01's record 3 has no recorded extract answer at the current prompt (FIXTURE_MISS stub), so a fixture-backend run of that packet reads
`failed` / `run_partial` naming record 3 (the extract step failed for a record). The paralegal's way out is the tray manual entry (D-031): enter each named record by
hand (its first sentence, as summary and quote), which clears an extract-only failure (T-165). Tests that need a ready case call this after waiting."""


def enter_failed_records_by_hand(c, tok):
    """If the case failed only because the extract step failed for named records, enter each by hand and return the new status; otherwise return the status unchanged."""
    case = c.get(f"/api/cases/{tok}").json()
    err = case.get("error") or {}
    if case["status"] != "failed" or not err.get("extract_only"):
        return case["status"]
    for n in err["records"]:
        first = next(r for r in case["records"] if r["id"] == f"r{n}")["sentences"][0]["text"]
        assert c.post(f"/api/cases/{tok}/records/r{n}/entry", json={"summary": first, "excerpt": first}).status_code == 201
    return c.get(f"/api/cases/{tok}/status").json()["status"]
