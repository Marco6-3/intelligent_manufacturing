"""各小组共用的数据契约；独立于 MuJoCo 和图形环境。"""
from dataclasses import dataclass
import numpy as np


def _array(a, shape, name):
    v = np.asarray(a, dtype=np.float64)
    if v.shape != shape or not np.all(np.isfinite(v)):
        raise ValueError(f"{name} must have shape {shape} and finite values; got {v.shape}")
    return v.copy()


@dataclass
class Pose:
    T_world_tcp: np.ndarray

    def __post_init__(self):
        t = _array(self.T_world_tcp, (4, 4), "T_world_tcp")
        if not np.allclose(t[3], [0, 0, 0, 1], atol=1e-8):
            raise ValueError("invalid homogeneous matrix bottom row")
        r = t[:3, :3]
        if not np.allclose(r.T @ r, np.eye(3), atol=1e-6) or not np.isclose(np.linalg.det(r), 1, atol=1e-6):
            raise ValueError("rotation must be in SO(3)")
        self.T_world_tcp = t


@dataclass
class IKResult:
    q: np.ndarray
    success: bool
    position_error_m: float
    orientation_error_rad: float
    iterations: int
    message: str = ""

    def __post_init__(self):
        self.q = _array(self.q, (6,), "IKResult.q")
        if not isinstance(self.success, (bool, np.bool_)):
            raise ValueError("success must be bool")
        if (not np.isfinite(self.position_error_m) or self.position_error_m < 0
                or not np.isfinite(self.orientation_error_rad) or self.orientation_error_rad < 0):
            raise ValueError("IK errors must be finite nonnegative numbers")
        if self.iterations < 0:
            raise ValueError("iterations must be nonnegative")


@dataclass
class JointTrajectory:
    time_s: np.ndarray
    q_rad: np.ndarray

    def __post_init__(self):
        t = np.asarray(self.time_s, dtype=np.float64)
        q = np.asarray(self.q_rad, dtype=np.float64)
        if t.ndim != 1 or len(t) < 2 or not np.all(np.isfinite(t)):
            raise ValueError("time_s must be finite 1D with >=2 samples")
        if q.shape != (len(t), 6) or not np.all(np.isfinite(q)):
            raise ValueError("q_rad must be finite Nx6")
        if not np.isclose(t[0], 0, atol=1e-10) or np.any(np.diff(t) <= 0):
            raise ValueError("time_s must begin at zero and be strictly increasing")
        self.time_s, self.q_rad = t.copy(), q.copy()


@dataclass
class ExecutionLog:
    time_s: np.ndarray
    q_command_rad: np.ndarray
    q_measured_rad: np.ndarray

    def __post_init__(self):
        command = JointTrajectory(self.time_s, self.q_command_rad)
        measured = np.asarray(self.q_measured_rad, dtype=np.float64)
        if measured.shape != command.q_rad.shape or not np.all(np.isfinite(measured)):
            raise ValueError("q_measured_rad must be finite Nx6")
        self.time_s = command.time_s
        self.q_command_rad = command.q_rad
        self.q_measured_rad = measured.copy()

    @property
    def joint_rmse_rad(self) -> float:
        return float(np.sqrt(np.mean((self.q_command_rad - self.q_measured_rad) ** 2)))
