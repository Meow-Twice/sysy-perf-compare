import sys
import re
import json
from datetime import datetime
import prettytable
from math import nan, isclose

columns = ['series', 'case_name', 'time1', 'time2', 'rate', 'effect']

pattern_perf = re.compile(r'TOTAL: \d+H\-\d+M\-\d+S\-\d+us')

def parse_sec(perf: str) -> float:
    groups = pattern_perf.findall(perf)
    assert len(groups) == 1
    t = datetime.strptime(groups[0], 'TOTAL: %HH-%MM-%SS-%fus')
    return t.hour * 3600 + t.minute * 60 + t.second + 1e-6 * t.microsecond

def calc_rate(tim1: float, tim2: float) -> float:
    return tim1 / tim2

if len(sys.argv) < 3:
    print('Usage: python3 -u perf.py result1.json result2.json', file=sys.stderr)
    sys.exit(1)

file1, file2 = sys.argv[1], sys.argv[2]

with open(file1, 'r') as fp:
    result1 = json.load(fp=fp)

time1 = dict()
for r in result1:
    try:
        perf_sec = parse_sec(r['perf'])
    except:
        continue
    time1[(r['series_name'], r['case_name'])] = perf_sec

with open(file2, 'r') as fp:
    result2 = json.load(fp=fp)

time2 = dict()
for r in result2:
    try:
        perf_sec = parse_sec(r['perf'])
    except:
        continue
    time2[(r['series_name'], r['case_name'])] = perf_sec

table = prettytable.PrettyTable(field_names=columns)
for series, casename in sorted(set(time1.keys()).intersection(time2.keys())):
    tim1, tim2 = time1[(series, casename)], time2[(series, casename)]
    try:
        rate = calc_rate(tim1, tim2)
    except:
        rate = nan
    effect = '.' if isclose(tim1, tim2) else ('+' if tim1 >= tim2 else '-')
    table.add_row((series, casename, '{0:.4f}'.format(tim1), '{0:.4f}'.format(tim2), '{0:.4f}'.format(rate), effect))

print(table)
