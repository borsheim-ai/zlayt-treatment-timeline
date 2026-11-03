# T-184 review, combined M3+M4 gate (D-075), staff-engineer-reviewer

Verdict: **pass**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.

Demo assets (72 annotated screenshots, burned-in-caption demo.webm, NARRATION.md). The product-manager panel's open major at 43ce6eb (video still showed the old 'code can read' sentence) was closed by c2dd104, and I checked that myself on the committed video. No blocker, no major open. Two minors.

Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).

## Findings
1. **minor** AC evidence on the card is stale: it cites 167.6 s and a capture at 4e4ff36, the committed video is 173.2 s recorded at 43ce6eb. Evidence: python3 tools/board.py show T-184 AC 1 evidence: 'artifacts/demo.webm 167.6 s ... Captured at 4e4ff36'; frame sample says 'duration 173.16'; c2dd104 commit message 're-recorded at 43ce6eb'. SUBMISSION_CHECKLIST.md:12 and NEEDS_CHRIS.md:26 say '174 s' (173.16 rounds to 173).
2. **minor** The re-recorded video was reviewed only by frame sampling (me); no panel persona watched it end to end. Evidence: GATE-M3M4-verify-pm-r2.md closes M4 (captions) at 38655da and leaves M3 open; c2dd104 landed after it. My sample is 1 frame per 6 s, deliberately coarse; deploy/SNAPSHOT.md:33 (cited in verify-pm-r2) says video pixels are not OCR-checked by the snapshot tool.

```json
{
 "card": "T-184",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git archive a932fc9: artifacts/demo.webm, demo.vtt, NARRATION.md, CAPTIONS.md, screenshots/final/; AC 1 of T-184",
 "exercised": [
  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
  "python3 tools/board.py show <card> for the AC of this card",
  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
  "ffmpeg-less frame sample of artifacts/demo.webm with artifacts/review-evidence/T-184-gate-staff/frames.py (30 frames, 6 s step): duration 173.16 s, 1280x886, so the <= 180 s AC holds",
  "tesseract over all 30 frames: grep 'can read' returns nothing; grep 'does not take a date of service' hits t126 and t096; looked at t126.png: Step 3 MRI note reads 'The letter does not take a date of service from the records', and the 'Saved: amount 1 $6,240.00 counted' line and the Undo button are visible above the caption band",
  "tesseract over the Step 3 final screenshots 25-32 (final/*.png): no 'code can read' text",
  "grep 'can read' artifacts/demo.vtt NARRATION.md CAPTIONS.md: no hits",
  "git show c2dd104 --stat: demo.webm, demo.vtt, NARRATION.md, video.py, gate-M3M4-suite-final.txt"
 ],
 "verdict": "pass",
 "scores": {
  "ac_met_at_head": 5,
  "video_matches_app_at_head": 5,
  "evidence_freshness": 3
 },
 "findings": [
  {
   "severity": "minor",
   "title": "AC evidence on the card is stale: it cites 167.6 s and a capture at 4e4ff36, the committed video is 173.2 s recorded at 43ce6eb",
   "evidence": "python3 tools/board.py show T-184 AC 1 evidence: 'artifacts/demo.webm 167.6 s ... Captured at 4e4ff36'; frame sample says 'duration 173.16'; c2dd104 commit message 're-recorded at 43ce6eb'. SUBMISSION_CHECKLIST.md:12 and NEEDS_CHRIS.md:26 say '174 s' (173.16 rounds to 173).",
   "why_it_matters": "A reader of the card sees a sha and a length that do not describe the shipped video. The claim in the packet is off by a second, not false in substance.",
   "fix": "Re-check AC 1 with the new evidence (173 s, recorded at 43ce6eb) and say '173 s' in the checklist and NEEDS_CHRIS.",
   "acceptance_test": "grep -n '174 s' submission/SUBMISSION_CHECKLIST.md submission/NEEDS_CHRIS.md returns nothing; card AC evidence names 43ce6eb."
  },
  {
   "severity": "minor",
   "title": "The re-recorded video was reviewed only by frame sampling (me); no panel persona watched it end to end",
   "evidence": "GATE-M3M4-verify-pm-r2.md closes M4 (captions) at 38655da and leaves M3 open; c2dd104 landed after it. My sample is 1 frame per 6 s, deliberately coarse; deploy/SNAPSHOT.md:33 (cited in verify-pm-r2) says video pixels are not OCR-checked by the snapshot tool.",
   "why_it_matters": "The privacy rule for the video is 'look at it by eye'; the sample here does not replace that.",
   "fix": "Chris (or the T-187 sweep) plays demo.webm once before submission.",
   "acceptance_test": "a note on T-187 or in the inbox says the video was watched at c2dd104 or later."
  }
 ],
 "whats_right": [
  "The Step 3 MRI note in the video now matches the app at HEAD, and the caption band sits below the app so Saved and Undo stay visible.",
  "The video is 173.16 s, inside the 180 s limit, and shows Your cases through the downloaded letter."
 ],
 "questions_for_chris": []
}
```
