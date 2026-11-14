# 债券 ETF 日度跟踪

Streamlit 网站入口：`streamlit_app.py`。网站读取仓库中的 `data.json`，访客无需 Excel 或 Wind。

## 每日更新

1. 在 Wind 中刷新并保存项目根目录的 `20261031债券ETF数据库.xlsx`。
2. 双击本目录的 `update_and_push.bat`。它读取 Excel、更新 `data.json`，再推送到 GitHub。
3. Streamlit Community Cloud 从 GitHub 获取更新。访客重新打开或点击页面的“刷新数据”查看新数据。

第一次运行前，电脑需具备 Python、openpyxl、Git，并已完成 GitHub 的 Git 登录。`update_data.py` 依赖本目录上一级的 `app.py` 解析工作簿；不要单独移动仓库目录。

资料来源：Wind，国盛证券研究所。当前没有净申赎和基准指数的独立历史序列，页面会标注数据缺口。
