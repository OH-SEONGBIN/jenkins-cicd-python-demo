#!/usr/bin/env python3
import argparse, csv, os, time
from xml.etree import ElementTree as ET
from pathlib import Path

def parse_junit(p):
    if not Path(p).exists(): return (0,0,0,0,0.0)
    root = ET.parse(p).getroot()
    suites = root.findall(".//testsuite") or [root]
    t=f=e=s=0; total=0.0
    for su in suites:
        t+=int(su.attrib.get("tests",0))
        f+=int(su.attrib.get("failures",0))
        e+=int(su.attrib.get("errors",0))
        s+=int(su.attrib.get("skipped",0))
        total+=float(su.attrib.get("time",0.0))
    return (t,f,e,s,total)

def parse_cov(p):
    if not Path(p).exists(): return 0.0
    root = ET.parse(p).getroot()
    rate = root.attrib.get("line-rate")
    return round(float(rate)*100,2) if rate else 0.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--junit", required=True)
    ap.add_argument("--cov",   required=True)
    ap.add_argument("--flake", default="")
    ap.add_argument("--out",   default="metrics/ci_metrics.csv")
    a=ap.parse_args()

    t,f,e,s,total = parse_junit(a.junit)
    cov = parse_cov(a.cov)
    lint = sum(1 for _ in open(a.flake,"r",encoding="utf-8")) if a.flake and Path(a.flake).exists() else 0
    passed = max(0, t-f-e-s)
    pass_ratio = round((passed/t)*100,2) if t else 0.0

    Path("metrics").mkdir(exist_ok=True)
    hdr = ["commit","tests","passed","failures","errors","skipped","pass_ratio","junit_time_sec","coverage_pct","lint_count"]
    row = [os.getenv("GIT_COMMIT",""), t, passed, f, e, s, pass_ratio, round(total,2), cov, lint]

    new = not Path(a.out).exists()
    with open(a.out,"a",newline="",encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(hdr)
        w.writerow(row)
    print(f"[metrics] pass={pass_ratio}%, cov={cov}%, lint={lint}, junit_time={round(total,2)}s")

if __name__=="__main__":
    main()