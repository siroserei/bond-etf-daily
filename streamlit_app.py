import json
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='债券 ETF 日度跟踪',layout='wide')
DATA=Path(__file__).with_name('data.json')

@st.cache_data
def read_data(modified):
    return json.loads(DATA.read_text(encoding='utf-8'))

if st.button('↻ 刷新数据'):
    read_data.clear()
    st.rerun()
d=read_data(DATA.stat().st_mtime)
funds=pd.DataFrame(d['funds'])
types={'利率债ETF':'利率债','信用债ETF':'信用债','可转债ETF':'可转债'}
st.title('债券 ETF 日度跟踪')
st.caption(f"数据日期：{d['asOf']} · ETF {len(funds)} 只 · 资料来源：Wind，国盛证券研究所")

major=st.radio('ETF 范围',['全部']+list(types),horizontal=True)
if major!='全部': funds=funds[funds['分类']==types[major]]
if major=='信用债ETF':
    sub=st.radio('二级分类',['全部','基准做市ETF','科创债ETF','其他信用债ETF'],horizontal=True)
    if sub!='全部':
        raw={'基准做市ETF':'基准做市','科创债ETF':'科创债','其他信用债ETF':'其他'}[sub]
        funds=funds[funds['信用债分类']==raw]

codes=funds['基金代码'].tolist()
def number(v): return f'{v:,.2f}'
c1,c2,c3,c4=st.columns(4)
c1.metric('ETF 数量',f'{len(funds)} 只')
c2.metric('总规模',number(funds['基金规模最新（↓）'].sum())+' 亿元')
c3.metric('平均换手率',number(funds['换手率最新'].mean())+'%')
c4.metric('平均贴水率',number(funds['贴水率最新'].mean()))

window=st.selectbox('历史区间',['近 20 日','近 60 日','年初至今'])
n={'近 20 日':20,'近 60 日':60,'年初至今':None}[window]
def aggregate(metric,mode='mean'):
    s=d['series'][metric]
    dates=s['dates'][-n:] if n else s['dates']
    values=[]
    for day in dates:
        idx=s['dates'].index(day)
        nums=[s['funds'].get(code,[None]*len(s['dates']))[idx] for code in codes]
        nums=[x for x in nums if isinstance(x,(int,float))]
        values.append((sum(nums) if mode=='sum' else sum(nums)/len(nums)) if nums else None)
    return dates,values

st.header('01　规模变化与市场表现')
dates,raw=aggregate('scale','sum')
scale=[x/1e8 if x is not None else None for x in raw]
delta=[None]+[(scale[i]-scale[i-1] if scale[i] is not None and scale[i-1] is not None else None) for i in range(1,len(scale))]
fig=go.Figure()
fig.add_bar(x=dates,y=delta,name='日度规模变化〔左轴，亿元〕',marker_color=['#bd302c' if x and x>=0 else '#16845d' for x in delta])
fig.add_scatter(x=dates,y=scale,name='规模合计〔右轴，亿元〕',yaxis='y2',line=dict(color='#294f7d',width=2.5))
fig.update_layout(height=430,margin=dict(l=25,r=25,t=35,b=20),yaxis2=dict(overlaying='y',side='right',showgrid=False),legend=dict(orientation='h'),plot_bgcolor='white',hovermode='x unified')
st.plotly_chart(fig,use_container_width=True)
st.caption('资料来源：Wind，国盛证券研究所')
st.write('说明：柱形为当日规模减上一交易日规模；蓝线为所选 ETF 规模合计。规模变化包含价格变化，不等于净申赎。')

st.header('02　折溢价率、换手率与贴水率')
dates,premium=aggregate('premium')
_,turnover=aggregate('turnover')
fig=go.Figure()
fig.add_scatter(x=dates,y=premium,name='平均折溢价率〔左轴，%〕',line=dict(color='#c57921',width=2.5))
fig.add_scatter(x=dates,y=turnover,name='平均换手率〔右轴，%〕',yaxis='y2',line=dict(color='#294f7d',width=2.5))
fig.update_layout(height=430,margin=dict(l=25,r=25,t=35,b=20),yaxis2=dict(overlaying='y',side='right',showgrid=False),legend=dict(orientation='h'),plot_bgcolor='white',hovermode='x unified')
st.plotly_chart(fig,use_container_width=True)
st.caption('资料来源：Wind，国盛证券研究所')
st.write('说明：折溢价率与换手率取所选 ETF 的算术平均值；缺失值不参与计算。')

discount=funds[['基金代码','贴水率最新']].dropna().sort_values('贴水率最新')
fig=go.Figure(go.Bar(x=discount['基金代码'],y=discount['贴水率最新'],marker_color=['#bd302c' if x>=0 else '#16845d' for x in discount['贴水率最新']]))
fig.update_layout(height=420,margin=dict(l=25,r=25,t=35,b=60),plot_bgcolor='white',xaxis_tickangle=-60)
st.plotly_chart(fig,use_container_width=True)
st.caption('资料来源：Wind，国盛证券研究所')
st.write('说明：展示最新贴水率截面；当前工作簿没有贴水率完整历史序列。')

st.header('03　ETF 明细')
query=st.text_input('搜索代码或名称')
if query:
    funds=funds[funds['基金代码'].astype(str).str.contains(query,case=False,regex=False)|funds['基金名称'].astype(str).str.contains(query,case=False,regex=False)]
display=funds[['基金代码','基金名称','分类','信用债分类','基金规模最新（↓）','基金规模单日变动','换手率最新','贴水率最新']].copy()
latest={code:next((x for x in reversed(values) if isinstance(x,(int,float))),None) for code,values in d['series']['premium']['funds'].items()}
display['折溢价率最新（%）']=display['基金代码'].map(latest)
st.dataframe(display,use_container_width=True,hide_index=True)
st.caption('资料来源：Wind，国盛证券研究所')
st.info('净申赎、10Y 国债收益率、3Y 中短票收益率及可转债指数对比，待工作簿补入对应日度数据。')
