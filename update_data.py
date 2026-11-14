from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from app import load
data=load()
(ROOT/'data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('已生成 data.json：',data['asOf'],'，',len(data['funds']),'只 ETF')
