#!/usr/bin/env python2
import os
import sys
import re

try:
    dirs = sys.argv[1]
except:
    dirs = '.'

re_year = re.compile("\((\d{4})\)")
# TODO fix for ##.# issues
re_issue = re.compile("#?[^\da-zA-Z](\d{1,3})[^\d]")
re_tot_issues = re.compile("\([oO][fF][ _](\d{1,2})\)")
re_vol = re.compile("v\d{1}")

parsers = {"Issue:": re_issue,
           "Total:": re_tot_issues,
           "Year :": re_year,
           "Vol  :": re_vol}

def get_reg(reg, file):
    r_all = reg.findall(file)
    try:
        r = r_all[0]
    except:
        r = None
    return r

def remove_str(orig, sub):
    f = orig.find(sub)
    if f == -1:
        return orig
    f_len = len(sub)
    return orig[0:f] + orig[f+f_len:]

def get_info(filename):
    left_to_parse = filename
    info = {}
    for p in parsers.keys():
        val = get_reg(parsers[p], left_to_parse)
        if val is not None:
            print(p + val)
            left_to_parse = remove_str(left_to_parse,val)
            print(left_to_parse)

for root,subs,files in os.walk(dirs):
    for file in files:
        if file.lower().endswith("cbr") or file.lower().endswith("cbz"):
            print(root + "/" + file)
            get_info(file)
