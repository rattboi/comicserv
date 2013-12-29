#!/usr/bin/env python2
import os
import sys
import re

try:
    dirs = sys.argv[1]
except:
    dirs = '.'

re_year = re.compile("\((\d{4})\)")
re_issue = re.compile("#?[^\da-zA-Z](\d{1,3})[^\d]")
re_tot_issues = re.compile("\([oO][fF][ _](\d{1,2})\)")
re_vol = re.compile("v\d{1}")

def print_reg(str, reg, file):
    r_all = reg.findall(file)
    try:
        r = r_all[0]
    except:
        r = None
    if r is not None: 
        print(str +  ": " + r)

for root,subs,files in os.walk(dirs):
    for file in files:
        if file.lower().endswith("cbr") or file.lower().endswith("cbz"):
            print(root + "/" + file)
            print_reg("Issue", re_issue, file)
            print_reg("Total", re_tot_issues, file)
            print_reg("Year ", re_year, file)
            print_reg("Vol  ", re_vol, file)


