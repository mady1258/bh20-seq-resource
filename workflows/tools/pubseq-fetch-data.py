#!/usr/bin/env python3

import argparse
import json
import os
import requests
import sys

parser = argparse.ArgumentParser(description="""

Fetch metadata (JSON) from PubSeq and optionally the FASTA files.  IDs
can be passed in on the command line or in a file.

""")
parser.add_argument('--out', type=str, help='Directory to write to',
required=True)
parser.add_argument('--ids', type=str, help='File with ids', required=False)
parser.add_argument('id', nargs='*', help='id(s)')
args = parser.parse_args()

dir = args.out
if not os.path.exists(dir):
    raise Exception(f"Directory {dir} does not exist")

ids = args.id
if (len(ids)==0):
    print(f"Reading {args.ids}")
    with open(args.ids) as f:
        ids = [ l.strip() for l in f.readlines() ]

for id in ids[0:2]:
    print(id)
    r = requests.get(f"http://covid19.genenetwork.org/api/sample/{id}.json")
    if r:
        m_url = r.json()[0]['metadata']
        mr = requests.get(m_url)
        meta = mr.json()
        with open(dir+"/"+id+".json","w") as outf:
            json.dump(meta, outf, indent=4)
    else:
        raise Exception(f"Can not find record for {id}")
