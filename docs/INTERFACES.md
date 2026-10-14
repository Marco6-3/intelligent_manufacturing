# V1 公共接口约定

**优先级最高**：组员写代码前阅读；变更需通过 PR 并通知受影响模块。

## 机器人与坐标
- 固定 **六自由度 UR5e**，关节向量 `q.shape == (6,)`、`dtype=float64`；关节顺序以 B 组提交模型和 `docs/ROBOT_MODEL.md` 为准，冻结前禁止臆造索引。
- SI 单位：位置 m、时间 s、角度 rad、速度 rad/s、加速度 rad/s²。
- `T_world_tcp.shape == (4,4)` 表示世界系到工具中心位姿；`T[:3,:3]` 正交，最后一行为 `[0,0,0,1]`。
- FK/IK 必须明确同一基座和 TCP；若基座不是 world，必须明确 `T_world_base`。
- 位置误差 m；旋转误差 rad，分别报告。姿态 IK 不能只满足平移。
- 机器人关节限位来自实际加载模型，不写死未经核对的限制。

## API（当前已经有验证类型，算法待实现）

```python
from src.contracts import Pose, JointTrajectory, IKResult
# C: fk(q: ndarray) -> ndarray  # (4, 4)
# D: ik(T_target: ndarray, q_init: ndarray) -> IKResult
# E: plan_joint(q_start, q_goal, duration, dt) -> JointTrajectory
# E: plan_cartesian(T_start, T_goal, duration, dt, q_seed, ik_solver) -> JointTrajectory
# F: execute_trajectory(trajectory: JointTrajectory) -> ExecutionLog
```

## 类契约
- `Pose`: 4×4 齐次矩阵，验证形状/有限性/齐次矩阵合法性。
- `IKResult`: `q` 六维、`success: bool`、`position_error_m`、`orientation_error_rad`、`iterations`、`message`。
- `JointTrajectory`: `time_s: (N,)`, `q_rad: (N,6)`；时间从 0 单调严格递增，N>=2。
- `ExecutionLog`: 时间、指令关节角和实测关节角形状一致，记录控制误差。
- 错误输入抛出 `ValueError`；IK 数值失败返回 `success=False` 而不是虚构角度为可行解。
- 输入输出均为普通 NumPy 数组；不要在核心算法中引入 GUI/MuJoCo viewer 依赖。

## 集成约定
- B 输出 `docs/ROBOT_MODEL.md` 说明模型来源、base/TCP、关节名、限位、夹爪策略。
- C 与 D 统一使用上述约定；测试应包含可达 FK→IK、不可达与接近奇异构型。
- E 以采样 `time_s` 为时间真值；F 根据轨迹时间而非自行猜测帧率执行。
- G 从真实数据记录中计算指标，区分规划误差、执行跟踪误差、末端误差；不可虚构结果。
- 初始骨架的 `src.main` 只确认公共契约，不代表机器人仿真已经完成。

## 代码所有权与接口冻结
A 管理 `src/contracts.py` 和 `README.md`。B–H 各自负责模块目录；对公共接口的更改通过单独 PR 审查，必要时升级版本。
