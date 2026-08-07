# GitHub 双周周报自动生成工具

这个项目会根据你的 GitHub 活动自动生成双周工作总结，并把报告写入 [report](report) 目录。

规则是：
- 每个周期固定为 14 天，例如 8.3-8.16、8.17-8.30
- 周期开始时会先创建对应的 Markdown 文件作为占位
- 当周期结束后，脚本会把该周期内的 GitHub 活动（PR / Issue / Commit）写入该文件

## 目录说明

- [scripts/generate_biweekly_report.py](scripts/generate_biweekly_report.py)：主生成脚本
- [scripts/run_reports.sh](scripts/run_reports.sh)：本地运行脚本
- [report](report)：生成后的周报输出目录
- [.github/workflows/biweekly-report.yml](.github/workflows/biweekly-report.yml)：GitHub Actions 自动执行配置

## 本地运行

```bash
./scripts/run_reports.sh --latest
```

也可以指定周期：

```bash
./scripts/run_reports.sh --start 2026-08-10 --end 2026-08-23
```

## GitHub Actions

仓库开启 Actions 后，工作流会在每周一自动执行；默认会生成当前最新的双周周期报告，并把结果提交到 report 目录。

## 环境要求

- Python 3.9+
- 可选：GitHub Token（设置 `GITHUB_TOKEN` 后可提升接口配额）

