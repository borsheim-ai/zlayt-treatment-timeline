/* SYNTHETIC mock case built from evals/golden/sample.txt (dev harness only) */
window.ZL_MOCK = {
 "token": "MOCKTOKEN0123456789abc",
 "name": "Rivera sample",
 "status": "ready",
 "demo_mode": true,
 "backend": "fixture",
 "records": [
  {
   "id": "r1",
   "seq": 1,
   "source_label": "Austin EMS run report",
   "date_raw": "2026-01-09",
   "date_iso": "2026-01-09",
   "date_status": "parsed",
   "date_candidates": [],
   "duplicate_of": null,
   "injection_tag": false,
   "encounter": true,
   "char_start": 106,
   "char_end": 313,
   "text": "=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\""
  },
  {
   "id": "r2",
   "seq": 2,
   "source_label": "Central ER discharge summary",
   "date_raw": "2026-01-09",
   "date_iso": "2026-01-09",
   "date_status": "parsed",
   "date_candidates": [],
   "duplicate_of": null,
   "injection_tag": false,
   "encounter": true,
   "char_start": 315,
   "char_end": 553,
   "text": "=== Record 2 ===\nDate: 2026-01-09\nSource: Central ER discharge summary\nExcerpt: \"Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.\""
  },
  {
   "id": "r3",
   "seq": 3,
   "source_label": "Dr. Alvarez, primary care",
   "date_raw": "2026-01-16",
   "date_iso": "2026-01-16",
   "date_status": "parsed",
   "date_candidates": [],
   "duplicate_of": null,
   "injection_tag": false,
   "encounter": true,
   "char_start": 555,
   "char_end": 773,
   "text": "=== Record 3 ===\nDate: 2026-01-16\nSource: Dr. Alvarez, primary care\nExcerpt: \"Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved.\""
  },
  {
   "id": "r4",
   "seq": 4,
   "source_label": "Capital PT, initial evaluation",
   "date_raw": "2026-01-23",
   "date_iso": "2026-01-23",
   "date_status": "parsed",
   "date_candidates": [],
   "duplicate_of": null,
   "injection_tag": false,
   "encounter": true,
   "char_start": 775,
   "char_end": 952,
   "text": "=== Record 4 ===\nDate: 2026-01-23\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.\""
  },
  {
   "id": "r5",
   "seq": 5,
   "source_label": "Capital PT, visit 8",
   "date_raw": "2026-02-20",
   "date_iso": "2026-02-20",
   "date_status": "parsed",
   "date_candidates": [],
   "duplicate_of": null,
   "injection_tag": false,
   "encounter": true,
   "char_start": 954,
   "char_end": 1088,
   "text": "=== Record 5 ===\nDate: 2026-02-20\nSource: Capital PT, visit 8\nExcerpt: \"Pain 4/10, improving. Patient reports missing 3 days of work.\""
  },
  {
   "id": "r6",
   "seq": 6,
   "source_label": "Capital PT, visit 9",
   "date_raw": "2026-03-06",
   "date_iso": "2026-03-06",
   "date_status": "parsed",
   "date_candidates": [],
   "duplicate_of": null,
   "injection_tag": false,
   "encounter": true,
   "char_start": 1090,
   "char_end": 1223,
   "text": "=== Record 6 ===\nDate: 2026-03-06\nSource: Capital PT, visit 9\nExcerpt: \"Discharged from PT after two missed appointments. Pain 3/10.\""
  },
  {
   "id": "r7",
   "seq": 7,
   "source_label": "Hill Country Pain Management, new patient",
   "date_raw": "2026-05-18",
   "date_iso": "2026-05-18",
   "date_status": "parsed",
   "date_candidates": [],
   "duplicate_of": null,
   "injection_tag": false,
   "encounter": true,
   "char_start": 1225,
   "char_end": 1453,
   "text": "=== Record 7 ===\nDate: 2026-05-18\nSource: Hill Country Pain Management, new patient\nExcerpt: \"New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.\""
  },
  {
   "id": "r8",
   "seq": 8,
   "source_label": "Austin Imaging, cervical MRI",
   "date_raw": "2026-05-29",
   "date_iso": "2026-05-29",
   "date_status": "parsed",
   "date_candidates": [],
   "duplicate_of": null,
   "injection_tag": false,
   "encounter": true,
   "char_start": 1455,
   "char_end": 1677,
   "text": "=== Record 8 ===\nDate: 2026-05-29\nSource: Austin Imaging, cervical MRI\nExcerpt: \"C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.\""
  },
  {
   "id": "r9",
   "seq": 9,
   "source_label": "Hill Country Pain Management, follow-up",
   "date_raw": "2026-06-12",
   "date_iso": "2026-06-12",
   "date_status": "parsed",
   "date_candidates": [],
   "duplicate_of": null,
   "injection_tag": false,
   "encounter": true,
   "char_start": 1679,
   "char_end": 1877,
   "text": "=== Record 9 ===\nDate: 2026-06-12\nSource: Hill Country Pain Management, follow-up\nExcerpt: \"Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.\""
  }
 ],
 "undated_entries": [],
 "entries": [
  {
   "id": "e1",
   "seq": 1,
   "record_ids": [
    "r1"
   ],
   "date": "2026-01-09",
   "date_status": "parsed",
   "provider": "Austin EMS run report",
   "summary": "Summary: 41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Aler",
   "ai_drafted": true,
   "source_kind": "record",
   "excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.",
   "excerpt_start": 180,
   "excerpt_end": 312,
   "state": "verified",
   "reasons": [],
   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "e1",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "e2",
   "seq": 2,
   "record_ids": [
    "r2"
   ],
   "date": "2026-01-09",
   "date_status": "parsed",
   "provider": "Central ER discharge summary",
   "summary": "Summary: Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclob",
   "ai_drafted": true,
   "source_kind": "record",
   "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.",
   "excerpt_start": 396,
   "excerpt_end": 552,
   "state": "verified",
   "reasons": [],
   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "e2",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "e3",
   "seq": 3,
   "record_ids": [
    "r3"
   ],
   "date": "2026-01-16",
   "date_status": "parsed",
   "provider": "Dr. Alvarez, primary care",
   "summary": "Summary: Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks.",
   "ai_drafted": true,
   "source_kind": "record",
   "excerpt": "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved.",
   "excerpt_start": 633,
   "excerpt_end": 772,
   "state": "verified",
   "reasons": [],
   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "e3",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "e4",
   "seq": 4,
   "record_ids": [
    "r4"
   ],
   "date": "2026-01-23",
   "date_status": "parsed",
   "provider": "Capital PT, initial evaluation",
   "summary": "Summary: Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $1",
   "ai_drafted": true,
   "source_kind": "record",
   "excerpt": "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.",
   "excerpt_start": 858,
   "excerpt_end": 951,
   "state": "needs_review",
   "reasons": [],
   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "e4",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "e5",
   "seq": 5,
   "record_ids": [
    "r5"
   ],
   "date": "2026-02-20",
   "date_status": "parsed",
   "provider": "Capital PT, visit 8",
   "summary": "Summary: Pain 4/10, improving. Patient reports missing 3 days of work.",
   "ai_drafted": true,
   "source_kind": "record",
   "excerpt": "Pain 4/10, improving. Patient reports missing 3 days of work.",
   "excerpt_start": 1026,
   "excerpt_end": 1087,
   "state": "verified",
   "reasons": [],
   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "e5",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "e6",
   "seq": 6,
   "record_ids": [
    "r6"
   ],
   "date": "2026-03-06",
   "date_status": "parsed",
   "provider": "Capital PT, visit 9",
   "summary": "Summary: Discharged from PT after two missed appointments. Pain 3/10.",
   "ai_drafted": true,
   "source_kind": "record",
   "excerpt": "Discharged from PT after two missed appointments. Pain 3/10.",
   "excerpt_start": 1162,
   "excerpt_end": 1222,
   "state": "verified",
   "reasons": [],
   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "e6",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "e7",
   "seq": 7,
   "record_ids": [
    "r7"
   ],
   "date": "2026-05-18",
   "date_status": "parsed",
   "provider": "Hill Country Pain Management, new patient",
   "summary": "Summary: New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Da",
   "ai_drafted": true,
   "source_kind": "record",
   "excerpt": "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.",
   "excerpt_start": 1319,
   "excerpt_end": 1452,
   "state": "verified",
   "reasons": [],
   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "e7",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "e8",
   "seq": 8,
   "record_ids": [
    "r8"
   ],
   "date": "2026-05-29",
   "date_status": "parsed",
   "provider": "Austin Imaging, cervical MRI",
   "summary": "Summary: C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenera",
   "ai_drafted": true,
   "source_kind": "record",
   "excerpt": "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.",
   "excerpt_start": 1536,
   "excerpt_end": 1676,
   "state": "needs_review",
   "reasons": [],
   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "e8",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "e9",
   "seq": 9,
   "record_ids": [
    "r9"
   ],
   "date": "2026-06-12",
   "date_status": "parsed",
   "provider": "Hill Country Pain Management, follow-up",
   "summary": "Summary: Recommend cervical epidural steroid injection. Patient states symptoms began after the Jan",
   "ai_drafted": true,
   "source_kind": "record",
   "excerpt": "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.",
   "excerpt_start": 1771,
   "excerpt_end": 1876,
   "state": "verified",
   "reasons": [],
   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "e9",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  }
 ],
 "amounts": [
  {
   "id": "a1",
   "record_ids": [
    "r2"
   ],
   "entry_id": "e2",
   "text": "$6,240",
   "value_cents": 624000,
   "kind": "charge",
   "excerpt": "ER charges: $6,240.",
   "excerpt_start": 533,
   "excerpt_end": 552,
   "state": "verified",
   "reasons": [],
   "why": "Labelled as a charge in the record, the figure is in the record, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "a1",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "a2",
   "record_ids": [
    "r8"
   ],
   "entry_id": "e8",
   "text": "$2,150",
   "value_cents": 215000,
   "kind": "charge",
   "excerpt": "Charge: $2,150.",
   "excerpt_start": 1661,
   "excerpt_end": 1676,
   "state": "verified",
   "reasons": [],
   "why": "Labelled as a charge in the record, the figure is in the record, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "a2",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "a3",
   "record_ids": [
    "r4"
   ],
   "entry_id": "e4",
   "text": "$185",
   "value_cents": 18500,
   "kind": "rate",
   "excerpt": "Charge per visit $185.",
   "excerpt_start": 929,
   "excerpt_end": 951,
   "state": "needs_review",
   "reasons": [
    "AMOUNT_RATE_NOT_TOTALED"
   ],
   "why": "This is a per-visit rate; the records never say how many visits were billed, so it is not totaled.",
   "review_status": "pending",
   "edited": null,
   "duplicate_note": null,
   "ladder": {
    "item_id": "a3",
    "backend": "fixture",
    "state": "needs_review",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  }
 ],
 "flags": [
  {
   "id": "f_gap_r6_r7",
   "type": "gap",
   "category": "gap_over_30",
   "source_kind": "record",
   "title": "Gap of 73 days",
   "explanation": "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).",
   "computed": {
    "days": 73,
    "threshold": 30,
    "from_record": "r6",
    "to_record": "r7"
   },
   "evidence": [
    {
     "record_id": "r6",
     "excerpt": "Date: 2026-03-06",
     "start": 1107,
     "end": 1123
    },
    {
     "record_id": "r6",
     "excerpt": "Source: Capital PT, visit 9",
     "start": 1124,
     "end": 1151
    },
    {
     "record_id": "r7",
     "excerpt": "Date: 2026-05-18",
     "start": 1242,
     "end": 1258
    },
    {
     "record_id": "r7",
     "excerpt": "Source: Hill Country Pain Management, new patient",
     "start": 1259,
     "end": 1308
    }
   ],
   "origin": "code",
   "reviewer_note": null,
   "state": "verified",
   "reasons": [],
   "why": "Calculated by code from the record headers.",
   "review_status": "pending",
   "edited": null,
   "ladder": {
    "item_id": "f_gap_r6_r7",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "f_acc_1",
   "type": "conflict",
   "category": "accident_date_after_treatment",
   "source_kind": "record",
   "title": "Stated accident date is later than recorded treatment",
   "explanation": "Stated accident date 2026-01-19 (\u201cDate of accident per intake form: 2026-01-19.\u201d) is later than the first recorded treatment, 2026-01-09 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose between them.",
   "computed": {},
   "evidence": [
    {
     "record_id": "r7",
     "excerpt": "Date of accident per intake form: 2026-01-19.",
     "start": 1407,
     "end": 1452
    },
    {
     "record_id": "r1",
     "excerpt": "Date: 2026-01-09",
     "start": 123,
     "end": 139
    },
    {
     "record_id": "r2",
     "excerpt": "Date: 2026-01-09",
     "start": 332,
     "end": 348
    }
   ],
   "origin": "code",
   "reviewer_note": null,
   "state": "verified",
   "reasons": [],
   "why": "Calculated by code; all three quotes are word for word in the records.",
   "review_status": "pending",
   "edited": null,
   "ladder": {
    "item_id": "f_acc_1",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "f_plan_4_6",
   "type": "conflict",
   "category": "treatment_plan_vs_actual",
   "source_kind": "record",
   "title": "Planned visits differ from visits attended",
   "explanation": "Plan of care lists 12 visits (Capital PT, initial evaluation); discharge is recorded at visit 9 after two missed appointments.",
   "computed": {},
   "evidence": [
    {
     "record_id": "r4",
     "excerpt": "Plan of care: 12 visits.",
     "start": 904,
     "end": 928
    },
    {
     "record_id": "r6",
     "excerpt": "Discharged from PT after two missed appointments.",
     "start": 1162,
     "end": 1211
    }
   ],
   "origin": "code",
   "reviewer_note": null,
   "state": "needs_review",
   "reasons": [
    "LEXICON_ONLY"
   ],
   "why": "The phrase list and the model disagree on this flag.",
   "review_status": "pending",
   "edited": null,
   "ladder": {
    "item_id": "f_plan_4_6",
    "backend": "fixture",
    "state": "needs_review",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "f_pre_3",
   "type": "pre_existing",
   "category": "pre_existing",
   "source_kind": "record",
   "title": "Earlier complaint mentioned",
   "explanation": "Dr. Alvarez, primary care (January 16, 2026) mentions low back pain in 2023.",
   "computed": {},
   "evidence": [
    {
     "record_id": "r3",
     "excerpt": "Patient reports low back pain in 2023, resolved.",
     "start": 724,
     "end": 772
    }
   ],
   "origin": "code",
   "reviewer_note": null,
   "state": "needs_review",
   "reasons": [
    "LLM_ONLY"
   ],
   "why": "The model found this; the phrase list did not.",
   "review_status": "pending",
   "edited": null,
   "ladder": {
    "item_id": "f_pre_3",
    "backend": "fixture",
    "state": "needs_review",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "f_deg_8",
   "type": "pre_existing",
   "category": "degenerative_language",
   "source_kind": "record",
   "title": "Degenerative wording in imaging",
   "explanation": "Austin Imaging, cervical MRI (May 29, 2026): \u201cFindings may represent degenerative change; correlate clinically.\u201d",
   "computed": {},
   "evidence": [
    {
     "record_id": "r8",
     "excerpt": "Findings may represent degenerative change; correlate clinically.",
     "start": 1595,
     "end": 1660
    }
   ],
   "origin": "code",
   "reviewer_note": null,
   "state": "verified",
   "reasons": [],
   "why": "Calculated by code from the record headers.",
   "review_status": "pending",
   "edited": null,
   "ladder": {
    "item_id": "f_deg_8",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  },
  {
   "id": "f_pat_9",
   "type": "causation",
   "category": "patient_report",
   "source_kind": "record",
   "title": "Reported onset",
   "explanation": "Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): \u201cPatient states symptoms began after the January collision.\u201d",
   "computed": {},
   "evidence": [
    {
     "record_id": "r9",
     "excerpt": "Patient states symptoms began after the January collision.",
     "start": 1818,
     "end": 1876
    }
   ],
   "origin": "code",
   "reviewer_note": null,
   "state": "verified",
   "reasons": [],
   "why": "Quote found word for word; the phrase list and the model agree, and the second check agreed.",
   "review_status": "pending",
   "edited": null,
   "ladder": {
    "item_id": "f_pat_9",
    "backend": "fixture",
    "state": "verified",
    "human": {
     "action": null,
     "edited_text": null,
     "at": null
    }
   }
  }
 ],
 "tray": [],
 "dates_to_confirm": [],
 "injection": {
  "records": [],
  "banner": null
 },
 "warnings": [],
 "totals": {
  "accepted": {
   "cents": 0,
   "count": 0,
   "label": "Accepted charges"
  },
  "pending": {
   "cents": 839000,
   "count": 2,
   "label": "Pending review"
  },
  "detected_not_a_total": {
   "cents": 839000,
   "count": 2,
   "label": "Detected (not a total)"
  },
  "not_totaled": [
   {
    "id": "a3",
    "kind": "rate",
    "text": "$185"
   }
  ]
 },
 "review": {
  "queue": [
   "f_plan_4_6",
   "f_pre_3",
   "a3",
   "e4",
   "e8",
   "e1",
   "e2",
   "e3",
   "e5",
   "e6",
   "e7",
   "e9",
   "a1",
   "a2",
   "f_gap_r6_r7",
   "f_acc_1",
   "f_deg_8",
   "f_pat_9"
  ],
  "counts": {
   "pending": 0
  },
  "ready_to_export": false
 }
};
