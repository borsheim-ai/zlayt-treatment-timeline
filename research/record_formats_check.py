#!/usr/bin/env python3
"""Re-check the SYNTHETIC specimens in research/record-formats.md (T-078 round 2).

Each specimen claims to follow a rule (NUCC grouping, CMS 8-minute rule, UB-04 rate x days, totals). This script re-adds them in code so a
later edit cannot silently break one. Exit 0 = every check passes.   Run: python3 research/record_formats_check.py
"""
import datetime as dt, pathlib, re, sys
from decimal import Decimal as D

DOC = pathlib.Path(__file__).resolve().parent / "record-formats.md"
MONEY = r"\(?-?\d{1,3}(?:,\d{3})*\.\d\d\)?-?"
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def money(s):
    neg = s.startswith("(") or s.endswith("-") or s.startswith("-")
    v = D(s.strip("()-").replace(",", ""))
    return -v if neg else v


def sections(text):
    parts = re.split(r"^## (\d+)\. ", text, flags=re.M)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def blocks(sec):
    return re.findall(r"```\n(.*?)```", sec, re.S)


def mmddyy(s):
    s = s.replace("O", "0")
    return dt.date(2000 + int(s[4:6]), int(s[0:2]), int(s[2:4]))


def main():
    text = DOC.read_text()
    S = sections(text)
    formats = [n for n in S if 2 <= n <= 20]
    words = {19: "nineteen"}
    check("intro format count matches sections 2-20", f"describes the {words.get(len(formats), '?')} document" in text,
          f"{len(formats)} format sections")
    for n in formats:
        bs = blocks(S[n])
        check(f"§{n} has a specimen", bs)
        for b in bs:
            check(f"§{n} specimen labeled synthetic", re.search(r"SYNTHETIC|SINTÉTICO", b.splitlines()[0]), b.splitlines()[0][:60])

    # §3 PT: CMS 8-minute rule on total timed minutes; plan count.
    pt = blocks(S[3])[0]
    timed = [(int(m), int(u)) for m, u in re.findall(r"\b97\d{3} \w+\s+(\d+) min\s+(\d+)u", pt)]
    total = sum(m for m, _ in timed)
    cms_units = (total + 7) // 15 if total >= 8 else 0
    check("PT timed minutes total stated", f"Total timed {total} min" in pt, f"{total} min")
    check("PT units = CMS 8-minute rule", sum(u for _, u in timed) == cms_units, f"{total} min -> {cms_units} units")
    check("PT per-code (AMA) units agree", all(u == (m + 7) // 15 for m, u in timed))
    v = re.search(r"Visit (\d+) of (\d+)", pt)
    plan = re.search(r"(\d)x/wk x (\d+) wks", pt)
    check("PT plan visits = frequency x weeks", v and plan and int(v.group(2)) == int(plan.group(1)) * int(plan.group(2)))

    # §4 travel card marks per column.
    chiro = blocks(S[4])[0]
    hdr = next(l for l in chiro.splitlines() if l.startswith("DATE"))
    cols = [c.strip() for c in hdr.split("|")]
    marks = {}
    for l in chiro.splitlines():
        if re.match(r"\d\d/\d\d\s+\|", l):
            cells = [c.strip() for c in l.split("|")]
            for c, val in zip(cols, cells):
                if val == "x":
                    marks.setdefault(c, set()).add(dt.date(2026, int(cells[0][:2]), int(cells[0][3:5])))

    # §8 CMS-1500 clean: days = units, grouped dates on the travel card, line sum = Item 28.
    clean, ocr = blocks(S[8])[:2]
    lines = re.findall(r"^\s+(\d{6})\s+(\d{6})\s+\d+\s+(\w+)\s+\w+\s+(\d+) \| (\d\d)\s+(\d+)", clean, re.M)
    check("CMS-1500 clean has service lines", len(lines) >= 3, f"{len(lines)} lines")
    col_for = {"97014": "ES", "97010": "H/C", "98941": "C"}
    line_sum = D(0)
    for f, t, code, dollars, cents, units in lines:
        a, b = mmddyy(f), mmddyy(t)
        days = (b - a).days + 1
        check(f"CMS-1500 {code} {f}-{t}: days = units", days == int(units), f"{days} days, {units} units")
        dates = {a + dt.timedelta(d) for d in range(days)}
        check(f"CMS-1500 {code} {f}-{t}: every date marked on travel card", dates <= marks.get(col_for.get(code, ""), set()))
        line_sum += D(f"{dollars}.{cents}")
    item28 = re.search(r"28\. TOTAL CHARGE\s+(\d+) \| (\d\d)", clean)
    check("CMS-1500 line sum = Item 28", item28 and line_sum == D(f"{item28.group(1)}.{item28.group(2)}"), str(line_sum))

    # §8 CMS-1500 OCR: at least one separator-less amount with its truth stated; truths add up to the Item 28 truth.
    truths, bare = [], 0
    for l in ocr.splitlines():
        m = re.search(r"<- truth (\d+\.\d\d)", l)
        if not m:
            continue
        if re.search(r"\s\d{4,5}\s", l.split("<-")[0]):
            bare += 1
        if l.lstrip().startswith(("24.", "0", "O")):
            truths.append(D(m.group(1)))
        elif "28." in l:
            t28 = D(m.group(1))
    check("CMS-1500 OCR has separator-less amounts with truth", bare >= 1, f"{bare} lines")
    check("CMS-1500 OCR truths sum to Item 28 truth", truths and sum(truths) == t28 == line_sum, str(sum(truths)))

    # §9 UB-04: lines sum to 0001; a room line where rate x days = charge; occurrence codes differ and are 01-06.
    occ = []
    room_ok = False
    for b in blocks(S[9]):
        occ.append(re.search(r"OCCURRENCE\s+CODE (\d\d)", b).group(1))
        tot47 = D(0); tot48 = D(0); allm = D(0); total = None
        for l in b.splitlines():
            m = re.match(r"(\d{4})\s{2,}", l)
            if not m:
                continue
            ms = [money(x) for x in re.findall(MONEY, l)]
            allm += sum(ms)
            rev = m.group(1)
            if rev == "0001":
                total = ms
                continue
            if rev.startswith("01"):
                rate, charge = ms[0], ms[1]
                days = int(re.search(r"\d\.\d\d\s+(\d+)\s+\d", l.replace(",", "")).group(1))
                room_ok = room_ok or rate * days == charge
                check(f"UB-04 room line {rev}: rate x days = charge", rate * days == charge, f"{rate} x {days} = {charge}")
                tot47 += charge
            else:
                tot47 += ms[0]
                tot48 += ms[1] if len(ms) > 1 else 0
        check("UB-04 lines sum to 0001 FL47", total and total[0] == tot47, f"{tot47} vs {total}")
        if total and len(total) > 1:
            check("UB-04 FL48 lines sum to 0001 FL48", total[1] == tot48)
        if room_ok:
            naive = f"{allm:,.2f}"
            check("UB-04 naive-sum figure stated in the note", naive in S[9], naive)
    check("UB-04 has a rate-on-charge-line specimen", room_ok)
    check("UB-04 occurrence codes are accident codes 01-06 and vary", all(c in {"01", "02", "03", "04", "05", "06"} for c in occ)
          and len(set(occ)) >= 2, str(occ))

    # §10 ledger: running balance and totals.
    led = blocks(S[10])[0]
    bal = D(0); ch = D(0); adj = D(0)
    for l in led.splitlines():
        if not re.match(r"\d\d/\d\d/\d\d", l):
            continue
        ms = [money(x) for x in re.findall(MONEY, l)]
        if " ADJ " in l:
            adj += abs(ms[0]); bal -= abs(ms[0])
        else:
            ch += ms[0]; bal += ms[0]
        check(f"ledger running balance {l[:8]}", bal == ms[-1], f"{bal} vs {ms[-1]}")
    tl = re.search(r"TOTAL CHARGES ([\d.,]+)\s+TOTAL PMTS ([\d.,]+)\s+TOTAL ADJ \(([\d.,]+)\)\s+BALANCE DUE ([\d.,]+)", led)
    check("ledger totals", tl and (D(tl.group(1)), D(tl.group(3)), D(tl.group(4))) == (ch, adj, bal), f"{ch} {adj} {bal}")

    # §11 EOB arithmetic per line and totals.
    eob = blocks(S[11])[0]
    sums = [D(0)] * 7
    for l in eob.splitlines():
        if re.match(r"\d\d/\d\d/\d\d", l):
            b_, disc, allw, ded, coin, paid, owe = [D(x) for x in re.findall(r"\d+\.\d\d", l)]
            check(f"EOB line {l[10:15]}", b_ - disc == allw and allw - ded - coin == paid and ded + coin == owe)
            sums = [s + v for s, v in zip(sums, (b_, disc, allw, ded, coin, paid, owe))]
        elif l.startswith("TOTAL"):
            check("EOB totals", [D(x) for x in re.findall(r"\d+\.\d\d", l)] == sums)

    # §13 Spanish: a day-first date with both parts <= 12 and its truth stated.
    sp = S[13]
    amb = [d for d in re.findall(r"\b(\d\d)/(\d\d)/(\d{4})\b", blocks(sp)[0]) if int(d[0]) <= 12 and int(d[1]) <= 12]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    check("Spanish specimen has an ambiguous day-first date with stated truth",
          any(f"{int(d)} {months[int(m) - 1]} {y}" in sp for d, m, y in amb), str(amb))

    # §15 EMS: call times in order.
    ems = blocks(S[15])[0]
    times = re.findall(r"(?:PSAP|Notified|En route|On scene|At pt|Left scene|At dest|Transfer of care) (\d\d):(\d\d)", ems.split("---")[0])
    mins = [int(h) * 60 + int(m) for h, m in times]
    check("EMS times ascend", len(mins) == 8 and mins == sorted(mins), str(times))

    # §16 ambulance: units x rate = charge; lines sum to total; mileage units fractional.
    amb_b = blocks(S[16])[0]
    tot = D(0)
    for code, units, rate, charge in re.findall(r"(A04\d\d-\w\w).*?\s([\d.]+)\s+([\d,]+\.\d\d)\s+([\d,]+\.\d\d)\s*$", amb_b, re.M):
        u, r, c = D(units), money(rate), money(charge)
        check(f"ambulance {code}: units x rate = charge", u * r == c, f"{u} x {r} = {c}")
        if code.startswith("A0425"):
            check("ambulance mileage units carry a tenth", "." in units)
        tot += c
    tc = re.search(r"TOTAL CHARGES\s+([\d,]+\.\d\d)", amb_b)
    check("ambulance lines sum to total", tc and money(tc.group(1)) == tot, str(tot))

    # §17 affidavit amounts match the §10 ledger.
    aff = blocks(S[17])[0]
    a = re.search(r"charged: \$([\d,.]+)\.\s+Amount paid: \$([\d,.]+)\.\s+Amount unpaid.*?\$([\d,.]+)\.", aff)
    check("affidavit charged/paid/unpaid = ledger", a and (D(a.group(1)), D(a.group(2)), D(a.group(3))) == (ch, D(0), bal),
          a.groups() if a else "no match")

    bad = [r for r in results if not r[1]]
    for name, ok, detail in results:
        if not ok or "-v" in sys.argv:
            print(("ok   " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    print(f"record_formats_check: {len(results) - len(bad)}/{len(results)} checks pass")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
