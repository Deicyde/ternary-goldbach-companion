"""Write each display's and step's page into the segment files, from the regions of steps.py.

New code.  A display item gets `page` (physical, of its region on the arXiv PDF), `printed_page`
and its title, "Display, p. <printed page>"; a step gets `page` and `printed_page` of its first
region.  The physical page minus the printed page offset is the printed page.

Usage: python3 -I pages.py <displays json> <steps json> <regions-steps json>
"""
import json
import sys

disp_path, steps_path, reg_path = sys.argv[1:4]
R = json.load(open(reg_path))
off = R['pdf']['printed_page_offset']
D, S = json.load(open(disp_path)), json.load(open(steps_path))
for rec in D['displays']:
    regs = R['displays'].get(rec['id'])
    if regs:
        rec['page'] = regs[0]['page']
        rec['printed_page'] = regs[0]['page'] - off
        rec['title'] = f"Display, p. {rec['printed_page']}"
for rec in S['steps']:
    regs = R['steps'].get(rec['id'])
    if regs:
        rec['page'] = regs[0]['page']
        rec['printed_page'] = regs[0]['page'] - off
for path, obj in ((disp_path, D), (steps_path, S)):
    json.dump(obj, open(path, 'w'), indent=1, ensure_ascii=False)
