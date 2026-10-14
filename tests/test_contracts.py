import numpy as np
import pytest
from src.contracts import Pose, JointTrajectory, IKResult, ExecutionLog


def test_pose_identity():
    assert np.allclose(Pose(np.eye(4)).T_world_tcp, np.eye(4))


def test_pose_reject_reflection():
    t = np.eye(4)
    t[0, 0] = -1
    with pytest.raises(ValueError):
        Pose(t)


def test_trajectory_shape_and_time():
    traj = JointTrajectory([0, 0.1, 0.2], np.zeros((3, 6)))
    assert traj.q_rad.shape == (3, 6)
    with pytest.raises(ValueError):
        JointTrajectory([0, 0.2, 0.1], np.zeros((3, 6)))
    with pytest.raises(ValueError):
        JointTrajectory([0, 0.2], np.zeros((2, 7)))


def test_ik_result():
    result = IKResult(np.zeros(6), False, 0.5, 0.1, 30, "not converged")
    assert not result.success
    with pytest.raises(ValueError):
        IKResult(np.zeros(6), True, -0.1, 0, 1)


def test_execution_log_rmse():
    log = ExecutionLog(np.array([0, 1]), np.zeros((2, 6)), np.ones((2, 6)))
    assert np.isclose(log.joint_rmse_rad, 1)
