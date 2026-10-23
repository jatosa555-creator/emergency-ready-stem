"""Build only the portable plugin after actual live verification; never submits."""
from pathlib import Path
from urllib.request import urlopen,Request
from urllib.parse import urlparse
import argparse,hashlib,json,zipfile
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--demo-url',required=True);a=p.parse_args()
u=urlparse(a.demo_url)
if u.scheme!='https' or not u.hostname or u.username or u.password or u.hostname in {'example.com','localhost'}:p.error('Use a real reviewer-accessible HTTPS video URL without credentials')
manifest=json.loads((R/'plugin/plugin.json').read_text(encoding='utf-8'))
mcp=json.loads((R/'plugin/mcp.json').read_text(encoding='utf-8'))
endpoint=mcp['mcpServers']['emergency-knowledge-bridge']['url'];base=endpoint.removesuffix('/mcp')
with urlopen(base+'/health',timeout=30)as r:health=json.load(r)
if health.get('status')!='ok' or health.get('version')!='0.4.0' or health.get('items')!=12:raise SystemExit('Unexpected production health')
req=Request(endpoint,method='POST',headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream'},data=json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/list'}).encode())
with urlopen(req,timeout=30)as r:names={x['name']for x in json.load(r)['result']['tools']}
if names!={'list_collections','search_references','get_reference'}:raise SystemExit('Unexpected live tools')
with urlopen(a.demo_url,timeout=30)as r:
 if not r.headers.get('Content-Type','').startswith('video/'):raise SystemExit('Demo URL must return a video directly')
 if not r.read(256):raise SystemExit('Demo is empty')
review=manifest['extensions']['com.openai']['review'];review['demo_recording_url']=a.demo_url
cases=review['test_cases']
assert len(cases['positive'])==5 and len(cases['negative'])==3
files={f.relative_to(R/'plugin').as_posix():f.read_bytes()for f in (R/'plugin').rglob('*')if f.is_file()}
assert len([x for x in files if x.endswith('/SKILL.md')])==4
assert all(x in {'plugin.json','mcp.json'}or x.startswith(('skills/','assets/'))for x in files)
assert not any(x.endswith(('.pyc','.env'))or '..' in Path(x).parts for x in files)
files['plugin.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
out=R/'dist/emergency-ready-stem-v0.4.0.zip';out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for name,data in sorted(files.items()):
  i=zipfile.ZipInfo(name,(2026,10,23,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;z.writestr(i,data)
receipt={'file':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':len(files),'health':health,'tools':sorted(names),'demo_url':a.demo_url,'status':'Built and live-checked; portal validation and review still separate'}
out.with_suffix('.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
