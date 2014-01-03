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
re_file_type_post = re.compile("\.([Cc][Bb][RrZz])$")

re_year_pre  = re.compile("\(?\d{4}\)?")
re_year_post = re.compile("\(?(\d{4})\)?")

re_issue_pre  = re.compile("#?[^\w]\d{1,3}(?:\.\d)?(?:[^\d]|$)")
re_issue_post = re.compile("#?[^\w](\d{1,3}(?:\.\d)?)(?:[^\d]|$)")

re_tot_issues_pre  = re.compile("\([oO][fF][ _]\d{1,2}\)")
re_tot_issues_post = re.compile("\([oO][fF][ _](\d{1,2})\)")

re_vol_pre  = re.compile("(?:v|Volume |Vol[. ])(?:\d{1,4})")
re_vol_post = re.compile("(?:v|Volume |Vol[. ])(\d{1,4})")

re_crap_pre  = re.compile("(?:\(.*\)(?:\s|$)?)+")
re_crap_post = re.compile("(\(.*\)(?:\s|$)?)+")

re_crap2_pre  = re.compile("\|(?:.*)$")
re_crap2_post = re.compile("\|(?:[\|\s]*)(.*$)")

re_series_pre  = re.compile(".*")
re_series_post = re.compile("^(.*?)[-\s]*$")

parsers = OrderedDict((("type",   (re_file_type_pre,re_file_type_post,'')),
                       ("vol",    (re_vol_pre, re_vol_post,'|')),
                       ("year",   (re_year_pre, re_year_post,'|')),
                       ("num_iss",(re_tot_issues_pre,re_tot_issues_post,'')),
                       ("issue",  (re_issue_pre, re_issue_post,'')),
                       ("crap",   (re_crap_pre, re_crap_post,'|')),
                       ("crap2",  (re_crap2_pre, re_crap2_post,'')),
                       ("series",  (re_series_pre, re_series_post,''))))

def setup(fn):
     url_conn = sqlite.connect(fn)
     cursor = url_conn.cursor()
     cursor.execute('CREATE TABLE IF NOT EXISTS comicbooks (id INTEGER PRIMARY KEY, series VARCHAR(50), volume VARCHAR(10), issue VARCHAR(10), year INTEGER, hash CHAR(32), summary VARCHAR(200), path VARCHAR(200))')
     url_conn.commit()

def get_reg(reg, file):
    r_all = reg.findall(file)
    try:
        r = r_all[0]
    except:
        r = None
    return r

def get_file_info(filename):
    left_to_parse = filename.replace('_',' ')
    info = {}
    for p in parsers.keys():
        val = get_reg(parsers[p][0], left_to_parse)
        if val is not None:
            left_to_parse = left_to_parse.replace(val,parsers[p][2])
            val = get_reg(parsers[p][1], val)
            info[p] = val.strip() # remove any leading/trailing spaces. Easier here than in regex
    # print(left_to_parse)
    return info

for root,subs,files in os.walk(dirs):
    for file in files:
        if file.lower().endswith("cbr") or file.lower().endswith("cbz"):
            #print(root + "/" + file)
            info = get_file_info(file)
            print(info)
            #print(info['series'])

