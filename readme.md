# GitHub 周报自动生成工具

本项目根据 GitHub 活动自动生成每周工作报告，并将结果写入 `report` 目录。

## 周期规则

- 所有时间统一使用北京时间（Asia/Shanghai）。
- 常规周期为周六 00:00（含）至下周六 00:00（不含），报告显示为“周六—周五”。
- GitHub Actions 每周六北京时间 00:10 执行（UTC 周五 16:10）。
- 每次自动执行会填充刚结束的周期，并创建刚开始周期的占位报告。
- 首个迁移周期为 2026-08-10 00:00 至 2026-08-15 00:00，报告显示为 2026.08.10—2026.08.14。

## 本地运行

```bash
./scripts/run_reports.sh --latest
```

`--latest` 会处理最近结束的周期及当前周期。也可以使用结束时间不包含的自定义区间：

```bash
./scripts/run_reports.sh --start 2026-08-10 --end 2026-08-15
```

## 文件说明

- `scripts/generate_biweekly_report.py`：报告生成脚本（文件名暂时保留以兼容原工作流）。
- `.github/workflows/biweekly-report.yml`：每周自动执行配置。
- `report`：报告输出目录。

环境要求：Python 3.9+，可选 GitHub Token 用于提高 API 配额。