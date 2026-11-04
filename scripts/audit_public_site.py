from __future__ import annotations
import csv,hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
manifest=R/'docs/public-file-manifest.json'
files=[p for p in R.rglob('*') if p.is_file() and '.git' not in p.parts and p.name!='public-file-manifest.json']
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
for req in ['README.md','src/index.html','dist/index.html','docs/security-review.md','public/data/benchmark_summary.csv','public/data/annual_portfolio_results.csv','public/data/monthly_portfolio_results.csv','public/images/powerbi/executive-overview.png','public/images/powerbi/report-gallery.png']:
 if not (R/req).exists():errors.append('Missing '+req)
if b'project-vortex-bi-showcase' not in (R/'src/index.html').read_bytes():errors.append('Website does not identify the companion BI repository')
if b'14-page' not in (R/'dist/index.html').read_bytes():errors.append('Built page does not describe the 14-page public PBIP')
payload={'reviewed':'2026-11-04','scope':'website source, generated dist, public aggregate data, chart images, Power BI screenshots and documentation','file_count':len(files),'errors':errors,'files':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(files)]}
manifest.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in payload.items() if k!='files'},indent=2))
if errors:raise SystemExit(1)
