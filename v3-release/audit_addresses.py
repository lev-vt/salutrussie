import re
from pathlib import Path
from html import unescape
from urllib.parse import unquote
import json
bad=re.compile(r"юных[\s_-]+ленинцев|yun[yi]kh[\s_-]+lenintsev|iounykh[\s_-]+lenintsev|lenintsev|ленинцев|109439|юридический адрес|registered\s+(?:office|address)|adresse (?:du siège social|juridique)|siège social",re.I)
good=re.compile(r"василевского|vasilevsk|vassilevsk",re.I)
hits=[];contacts=[];checked=0
for p in Path('.').rglob('*'):
    if not p.is_file() or '.git' in p.parts or p.suffix.lower() not in {'.html','.js','.css','.json','.xml','.svg','.md','.txt','.py','.htaccess'} or p.name=='audit_addresses.py': continue
    s=unquote(unescape(p.read_text(encoding='utf-8',errors='replace')))
    checked+=1
    if bad.search(s): hits.append({'path':str(p),'matches':len(bad.findall(s))})
    if good.search(s): contacts.append(str(p))
print('ADDRESS_AUDIT '+json.dumps({'checked':checked,'possible_old_address':hits,'contact_address':contacts},ensure_ascii=False))
