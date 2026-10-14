"""Day-0 框架入口；不是已完成的机器人仿真。"""
import numpy as np
from src.contracts import Pose, JointTrajectory


def main():
    Pose(np.eye(4))
    JointTrajectory(np.array([0., 1.]), np.zeros((2, 6)))
    print("团队数据契约 OK；UR5e 模型/运动学/搬运功能待 B-H 实现。")


if __name__ == "__main__":
    main()
