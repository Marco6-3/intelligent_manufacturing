# 团队开发规范

## 分支 / PR
- main 为可集成分支；每人从最新 main 创建分支：`feat/B-scene`、`feat/C-fk`、`feat/D-ik`、`feat/E-trajectory`、`feat/F-control`、`feat/G-analysis`、`docs/H-report`。
- 不直接推送覆盖 main；通过 Pull Request 审查合并。
- A 组长负责共享接口/配置。公共接口变更必须先讨论再修改，不能私自改变量的维度与单位。
- PR 至少写：功能、运行方式、测试结果、数据/模型来源、AI 使用说明、未完成事项。
- 禁止把大体积模型、仿真缓存、`.venv`、自动生成视频直接塞进小 PR；可以把小样例与必要引用保存进仓库。

## 每次提交前
```bash
python -m pytest -q
python -m src.main
```

## 组员提交格式
```
模块：C / 正运动学
实现：...
运行：python -m pytest tests/test_contracts.py -q
结果：...
模型坐标与单位：...
AI工具与人工核验：...
依赖或风险：...
```

## PR 基础审核
1. 可以复现，不只截图；2. 不破坏公共接口；3. 有失败条件、关节限位与数值异常处理；4. 相应测试或可重复实验；5. 结论严格来自结果。
