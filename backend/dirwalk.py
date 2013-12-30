#!/usr/bin/env python2
import os
import sys
import re
from collections import OrderedDict

try:
    dirs = sys.argv[1]
except:
    dirs = '.'

re_file_type_pre  = re.compile("\.[Cc][Bb][RrZz]$")
re_file_type_post = re.compile("\.(cbr|cbz|CBR|CBZ)$")

re_year_pre = re.compile("\(\d{4}\)")
re_year_post = re.compile("\((\d{4})\)")

# TODO fix for ##.# issues
re_issue_pre  = re.compile("#?[^\w]\d{1,3}(?:\.\d)?(?:[^\d]|$)")
re_issue_post = re.compile("#?[^\w](\d{1,3}(?:\.\d)?)(?:[^\d]|$)")

re_tot_issues_pre  = re.compile("\([oO][fF][ _]\d{1,2}\)")
re_tot_issues_post = re.compile("\([oO][fF][ _](\d{1,2})\)")

re_vol_pre  = re.compile("v\d{1}")
re_vol_post = re.compile("v(\d{1})")

re_crap_pre = re.compile("(?:\(.*\)(?:\s|$)?)+")
re_crap_post = re.compile("(\(.*\)(?:\s|$)?)+")

parsers = OrderedDict((("Type :", (re_file_type_pre,re_file_type_post)),
                       ("Vol  :", (re_vol_pre, re_vol_post)),
                       ("Year :", (re_year_pre, re_year_post)),
                       ("Total:", (re_tot_issues_pre,re_tot_issues_post)),
                       ("Issue:", (re_issue_pre, re_issue_post)),
                       ("Crap :", (re_crap_pre, re_crap_post))))

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
    left_to_parse = filename.replace('_',' ')
    info = {}
    for p in parsers.keys():
        val = get_reg(parsers[p][0], left_to_parse)
        if val is not None:
            left_to_parse = remove_str(left_to_parse,val) # remove section from filename
            val = get_reg(parsers[p][1], val)
            print(p + val)
    print(left_to_parse)

for root,subs,files in os.walk(dirs):
    for file in files:
        if file.lower().endswith("cbr") or file.lower().endswith("cbz"):
            print(root + "/" + file)
            get_info(file)
