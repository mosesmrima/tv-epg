#!/usr/bin/env python3
"""Split epg.channels.xml into one channels file per source site.

Writes ch_<site>.xml for each site and sites.txt with the list of sites.
Grabbing each site as a separate process isolates crashes: one bad site
config cannot abort the others.
"""
import re
from collections import defaultdict

def main():
    by_site = defaultdict(list)
    for line in open("epg.channels.xml", encoding="utf-8"):
        if "<channel" not in line:
            continue
        m = re.search(r'site="([^"]+)"', line)
        if m:
            by_site[m.group(1)].append(line.rstrip("\n"))
    for site, rows in by_site.items():
        with open(f"ch_{site}.xml", "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<channels>\n')
            f.write("\n".join(rows) + "\n")
            f.write("</channels>\n")
    with open("sites.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(by_site)) + "\n")
    print(f"sites: {len(by_site)}")

if __name__ == "__main__":
    main()
