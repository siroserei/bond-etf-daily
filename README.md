# 债券 ETF 日度跟踪

本仓库是本地网站的公开只读版本。访客打开 Streamlit 网站即可查看已发布的数据，不需要本地 Excel 或 Wind。

## 每日更新

1. 在 Wind 中刷新并保存上一级目录的 `20261031债券ETF数据库.xlsx`。
2. 双击本目录的 `update_and_push.bat`。它从 Excel 生成 `data.json` 并推送到 GitHub。
3. Streamlit 部署若已连接本仓库的 `main` 分支，将自动获取更新。访客重新打开网站即可看到最新数据。

首次运行需要本机 Python、openpyxl、Git，以及可用的 GitHub 推送权限。`update_data.py` 依赖上一级目录的 `app.py`。

净申赎为份额变化乘当日单位净值的估算值。网站会标注底稿中未更新的份额与规模日期。

资料来源：Wind，国盛证券研究所。
