from __future__ import annotations
import csv,hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
manifest=R/'docs/public-file-manifest.json'
REVIEW_DATE='2026-11-06'
BINARY={'.png','.jpg','.jpeg','.gif','.webp','.ico','.pdf','.woff','.woff2','.ttf'}
def canonical(p):
 # Hash what Git stores: LF for text, exact bytes for binaries, on every operating system.
 raw=p.read_bytes()
 return raw if p.suffix.lower() in BINARY or b'\0' in raw else raw.replace(b'\r\n',b'\n')
files=sorted((p for p in R.rglob('*') if p.is_file() and not {'.git','node_modules','__pycache__'}&set(p.parts) and p.name!='public-file-manifest.json'),key=lambda p:p.relative_to(R).as_posix())
errors=[]
patterns=[r'(?i)C:\\Projects\\Project-robot-trader',r'(?i)D:\\Robot',r'(?i)file:///',r'(?i)ZZP_TRIANGLE',r'(?i)CATCH-LONG',r'(?i)H36AAH_RECT',r'(?i)AAF_DESC',r'(?i)account.?number',r'(?i)broker.?login',r'(?i)password\s*[:=]',r'(?i)api[_ -]?key\s*[:=]',r'(?i)secret\s*[:=]']
for p in files:
 if p.suffix.lower() in {'.md','.txt','.json','.csv','.html','.css','.js','.mjs','.svg','.gitignore'}:
  try:t=p.read_text(encoding='utf-8-sig')
  except Exception as e:errors.append(f'Unreadable {p.relative_to(R)}: {e}');continue
  if p.name!='audit_public_site.py':
   for pattern in patterns:
    if re.search(pattern,t):errors.append(f'Sensitive/path match in {p.relative_to(R)}')
 if p.suffix.lower()=='.csv':
  with p.open(encoding='utf-8-sig',newline='') as f:headers=next(csv.reader(f),[])
  if {'TradeID','OpportunityID','EntryPrice','StopPrice','TargetPrice','ExitPrice','SignalTimeUTC','EntryTimeUTC','ExitTimeUTC'} & set(headers):errors.append(f'Trade-level CSV fields in {p.relative_to(R)}')
for req in ['README.md','src/index.html','dist/index.html','docs/security-review.md','public/data/benchmark_summary.csv','public/data/annual_portfolio_results.csv','public/data/monthly_portfolio_results.csv','public/images/powerbi/03-Executive.png']:
 if not (R/req).exists():errors.append('Missing '+req)
for image in [p for folder in (R/'public/images/powerbi',R/'dist/images/powerbi') if folder.exists() for p in folder.glob('*.png')]:
 raw=image.read_bytes(); oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 if oid=='a8eca13931878c6b686c30f3b4890e0398d977ce':errors.append(f'Known contaminated screenshot blob present: {image.relative_to(R)}')
if b'project-vortex-bi-showcase' not in (R/'src/index.html').read_bytes():errors.append('Website does not identify the companion BI repository')
if b'14-page' not in (R/'dist/index.html').read_bytes():errors.append('Built page does not describe the 14-page public PBIP')
market=json.loads((R/'public/data/replay/pyramiding-win-session.json').read_text(encoding='utf-8'))
if market.get('sourceSessionDate')!='2022-09-30' or market.get('sourceTimezoneAuthenticated') is not False:errors.append('Replay date provenance or timezone qualification is missing')
if market.get('sourceSessionClockStart')!='09:00' or market.get('sourceSessionClockTimezoneAuthenticated') is not False or market.get('candles', [{}])[-1].get('t')!=530:errors.append('Qualified source-session clock labels must span 09:00 to 17:50')
built_html=(R/'dist/index.html').read_text(encoding='utf-8')
if '30 Sep 2022' not in built_html or 'source clock timezone is unverified' not in built_html.lower():errors.append('Visible replay date disclosure is missing or unqualified')
if 'Source-session clock · timezone unverified' not in built_html or '09:00 to 17:50' not in built_html:errors.append('Visible source-session clock qualification is missing')
if any(k in market for k in ('entry1SourceEpoch','entry2SourceEpoch','sourceSessionStartUTC','sourceSessionEndUTC')):errors.append('Exact source timestamps must remain private')
screens=list((R/'public/images/powerbi').glob('[0-9][0-9]-*.png'))
payload={'reviewed':REVIEW_DATE,'scope':'website source, generated dist, public aggregate data, chart images, Power BI screenshots and documentation','file_count':len(files),'gallery_screenshot_count':len(screens),'known_contaminated_blob':'a8eca13931878c6b686c30f3b4890e0398d977ce','errors':errors,'files':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(canonical(p)).hexdigest(),'bytes':len(canonical(p))} for p in files]}
manifest.write_bytes((json.dumps(payload,indent=2)+'\n').encode('utf-8'))
print(json.dumps({k:v for k,v in payload.items() if k!='files'},indent=2))
if errors:raise SystemExit(1)
