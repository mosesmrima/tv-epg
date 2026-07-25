#!/usr/bin/env python3
"""Merge many XMLTV files into one.

Reads every *.xml file in the input directory, collects the channel and
programme elements, removes duplicate channels by id, and writes a single
XMLTV document. XMLTV is a flat format (no nested channel or programme
elements), so a simple non-greedy scan is safe and fast.
"""
import sys, os, glob, re

def main():
    indir, outfile = sys.argv[1], sys.argv[2]
    channels = {}
    programmes = []
    for path in sorted(glob.glob(os.path.join(indir, "*.xml"))):
        try:
            data = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for m in re.finditer(r"<channel\b.*?</channel>", data, re.S):
            cid = re.search(r'id="([^"]*)"', m.group(0))
            if cid:
                channels.setdefault(cid.group(1), m.group(0))
        programmes.extend(re.findall(r"<programme\b.*?</programme>", data, re.S))
    with open(outfile, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<tv generator-info-name="tv-epg">\n')
        for c in channels.values():
            f.write(c + "\n")
        for p in programmes:
            f.write(p + "\n")
        f.write("</tv>\n")
    print(f"merged channels={len(channels)} programmes={len(programmes)}")

if __name__ == "__main__":
    main()
