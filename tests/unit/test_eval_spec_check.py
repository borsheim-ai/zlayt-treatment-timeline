"""evals.run --check-spec: REQUIREMENTS section 6 blocks vs golden export, byte-equal. T-038 AC2, R-EX-6."""
import json
from evals import run as R

def test_real_spec_matches_golden():
    """AC2: today's REQUIREMENTS section 6 block 1 and 2 equal LETTER_TEXT and INTERNAL_NOTES_TEXT."""
    s = R.check_spec()
    assert s == {"spec_matches_golden": True, "letter_equal": True, "internal_notes_equal": True}

def test_changing_one_character_in_a_temp_copy_makes_it_false(tmp_path):
    """AC2: one changed character in a temp copy of REQUIREMENTS (letter block, then notes block) flips spec_matches_golden to false."""
    text = R.REQUIREMENTS.read_text()
    b1, b2 = R.spec_blocks(text)
    for i, blk, key in ((1, b1, "letter_equal"), (2, b2, "internal_notes_equal")):
        p = tmp_path / f"req{i}.md"
        p.write_text(text.replace(blk, blk.replace("2026", "2027", 1), 1))
        s = R.check_spec(p)
        assert s["spec_matches_golden"] is False and s[key] is False

def test_cli_writes_spec_matches_golden_to_latest_json(tmp_path):
    """AC2: `--check-spec` writes spec_matches_golden into latest.json and exits 0."""
    assert R.main(["--check-spec", "--out", str(tmp_path)]) == 0
    assert json.loads((tmp_path / "latest.json").read_text())["spec_matches_golden"] is True
