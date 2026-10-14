# 智能制造导论 · 题目11

**基于 MuJoCo 的六轴工业机器人运动学分析与搬运轨迹仿真系统**

课程项目｜8 人团队｜2026-10-15 至 2026-11-04

> 当前为 **Day-0 协作框架**，不代表运动学、抓取或仿真已完成。所有演示结果以测试和实验为准。

## 快速入口
- [任务认领与验收](docs/TASKS.md)
- [接口规范（必须先读）](docs/INTERFACES.md)
- [Git 协作规范](CONTRIBUTING.md)
- [阶段计划](docs/PLAN.md)
- [AI 使用记录模板](docs/AI_USAGE.md)

## 技术范围
UR5e 六轴模型（来自 MuJoCo Menagerie，模型及资源按上游许可证引用）；Python、NumPy、SciPy、MuJoCo。正运动学、逆运动学、轨迹规划、搬运仿真、奇异点与可达性分析。

## 开发环境
建议 Python 3.11；精确依赖以 `requirements.txt` 为准。

```bash
git clone https://github.com/Marco6-3/intelligent_manufacturing.git
cd intelligent_manufacturing
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m src.main
```

目前 `src.main` 只做接口框架检查，不加载机器人。B 组完成模型导入后，再接入真实 MuJoCo 场景。不要把空壳标记为“搬运系统可用”。

## 核心约定
- 关节顺序固定为 UR5e 模型的六个受控关节；角度/角速度单位 rad、rad/s；长度 m；时间 s。
- 末端位姿统一为 `T_world_tcp` (4×4, float)，随模型建立再冻结 TCP 定义。
- 接口与异常见 [docs/INTERFACES.md](docs/INTERFACES.md)，修改接口须先由 A 协调。
- 功能分支 `feat/B-scene` 等；通过 PR 合并 `main`，不直接覆盖其他人的文件。

## 原始课程要求
至少两类可运行/可演示文件；技术说明书、AI 使用声明、5–10 页 PPT，8 分钟汇报。优先保证正逆运动学、轨迹、奇异性、可达性、结果可复现。

## 外部资源
- https://github.com/google-deepmind/mujoco_menagerie/tree/main/universal_robots_ur5e
- https://mujoco.readthedocs.io/
- https://petercorke.github.io/robotics-toolbox-python/
