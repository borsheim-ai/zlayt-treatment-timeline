"""T-214 (D-065): a flag whose only source is code (the phrase list, or a computed gap/conflict) is never a "Prepared answer". prepared is true only when a curated answer is behind the item."""
from tests.unit.test_prepared_provenance_r3 import _client, _run


def _flags(c, tok):
    return c.get(f"/api/cases/{tok}").json()["flags"]


def test_code_only_flags_are_not_prepared_on_the_curated_sample(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    tok = _run(c)
    fl = _flags(c, tok)
    by_id = {f["id"]: f for f in fl}
    assert by_id["f_r7_1"]["origin"] == "lexicon"
    assert by_id["f_r7_1"]["prepared"] is False and by_id["f_r7_1"]["origin_label"] == "Found by code (phrase list)"
    for f in fl:
        if f["origin"] == "lexicon":
            assert f["prepared"] is False and f["origin_label"] == "Found by code (phrase list)", f["id"]
        elif f["origin"] == "code":
            assert f["prepared"] is False and f["origin_label"] == "Found by code", f["id"]
        else:
            assert f["prepared"] is True and f.get("origin_label") is None, f["id"]      # a curated answer is behind it
    item = c.get(f"/api/cases/{tok}/items/f_r7_1").json()["item"]
    assert item["prepared"] is False and item["origin_label"] == "Found by code (phrase list)"


def test_recorded_set_flags_are_never_prepared(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch)
    tok = _run(c)
    fl = _flags(c, tok)
    assert fl and all(f["prepared"] is False for f in fl)
    assert all(f.get("origin_label") for f in fl if f["origin"] in ("lexicon", "code"))
