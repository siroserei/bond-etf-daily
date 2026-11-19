"""Public, read-only copy of the local bond ETF dashboard."""

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data.json'
st.set_page_config(page_title='债券 ETF 日度跟踪', layout='wide')

@st.cache_data
def build_page(modified):
    data = json.loads(DATA.read_text(encoding='utf-8'))
    html = (ROOT / 'web' / 'index.html').read_text(encoding='utf-8')
    javascript = (ROOT / 'web' / 'app.js').read_text(encoding='utf-8')
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    # The hosted copy reads the committed snapshot; only the operator updates it.
    shim = f'<script>window.__ETF_DATA__={payload};window.fetch=async()=>({{ok:true,json:async()=>window.__ETF_DATA__}});</script>'
    return html.replace('<script src="/app.js"></script>', shim + '<script>' + javascript + '</script>')

page = build_page(DATA.stat().st_mtime_ns)
components.html(page, height=4700, scrolling=True)
