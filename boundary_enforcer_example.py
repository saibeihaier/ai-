"""边界执行器示例 – 钳制配置参数并检测漂移"""

import time
import numpy as np
from collections import deque

class ConfigBoundary:
    def __init__(self, config_module, gene_interpreter):
        self.config = config_module
        self.interpreter = gene_interpreter
        self.history = deque(maxlen=100)
    
    def clamp(self, param_name: str, value: float) -> float:
        minv, maxv = self.interpreter.get_parameter_range(param_name)
        if minv is not None and value < minv:
            print(f"[Boundary] {param_name}={value} 低于最小值 {minv}，已钳制")
            return minv
        if maxv is not None and value > maxv:
            print(f"[Boundary] {param_name}={value} 超过最大值 {maxv}，已钳制")
            return maxv
        return value
    
    def set_config(self, param_name: str, value: float):
        clamped = self.clamp(param_name, value)
        setattr(self.config, param_name, clamped)
        self.history.append({"time": time.time(), param_name: param_name, value: clamped})
    
    def detect_drift(self, window=20, threshold=0.01) -> dict:
        """检测参数是否有单向漂移趋势"""
        if len(self.history) < window:
            return {"drift_detected": False}
        # 按参数分组
        param_values = {}
        for record in self.history:
            p = record["param_name"]
            if p not in param_values:
                param_values[p] = []
            param_values[p].append(record["value"])
        drifts = {}
        for p, values in param_values.items():
            if len(values) >= window:
                x = np.arange(len(values))
                slope = np.polyfit(x, values, 1)[0]
                if abs(slope) > threshold:
                    drifts[p] = slope
        return {"drift_detected": bool(drifts), "details": drifts}