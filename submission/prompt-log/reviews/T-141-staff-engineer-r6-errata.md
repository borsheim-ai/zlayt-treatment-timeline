# Errata to reviews/T-141-staff-engineer-r6.md (same review, same verdict: fail)

The main review file is write-once under the reviewer guard, so the corrections are recorded here. None changes a finding or the verdict.

1. Counts paragraph (body, "Counts against the r5 control"): "43 of the 67 r5 mismatches are fixed" should read "43 of the 66 counted r5 mismatches are fixed (N1 excluded); 23 pre-existing mismatches remain; 1 new mismatch (Q15)". The JSON exercised and whats_right entries already say 43.
2. Brief check 2: the FAIL list should also name the bare hit and impact forms (R29 and R35). The JSON F2 finding covers them.
3. F2 acceptance test: the V13 line is tests/unit/test_t141_r3_variants.py:29, not :25.
4. Exercised, line 3: the hash for conflicts.py is a SHA-1 from shasum (01ef80b4a5ea63cdb72996a5e74ba6eeddaad9cc), not SHA-256.
5. F1 evidence: the test at tests/unit/test_t141_d061_closed_exemption.py:43-48 uses comma, semicolon and sentence splits, not only semicolon and sentence splits.
