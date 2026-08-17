# my GitHub 周报

根据 GitHub 活动自动生成每周工作报告，位于 `report` 目录下。

## 周期规则

- 北京时间（Asia/Shanghai）。
- 记录周期为周六 00:00（含）至下周六 00:00（不含）。
- GitHub Actions 每周六00:10 执行（UTC 周五 16:10）。
- 每次自动执行会填充刚结束的周期，并创建刚开始周期的占位报告。
- 首个周期为 2026-08-10 00:00 至 2026-08-15 00:00，报告显示为 2026.08.10—2026.08.14。

## 文件说明

- `scripts/generate_biweekly_report.py`：报告生成脚本（文件名暂时保留以兼容原工作流）。
- `.github/workflows/biweekly-report.yml`：每周自动执行配置。
- `report`：报告输出目录。
