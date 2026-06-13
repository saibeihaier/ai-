"""基因解释器 – 将 gene_spec.json 转化为运行时策略"""

import json
import jsonschema
from typing import Any, Dict, Tuple

class GenomeInterpreter:
    def __init__(self, spec_path: str, schema_path: str = None):
        with open(spec_path, 'r', encoding='utf-8') as f:
            self.spec = json.load(f)
        if schema_path:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            jsonschema.validate(self.spec, schema)
        self._build_policy()
    
    def _build_policy(self):
        self.constraints = self.spec.get("parameter_constraints", {})
        self.principles = self.spec.get("principles", [])
        self.algorithms = self.spec.get("algorithms", {})
        self.invariants = self.spec.get("architectural_invariants", [])
    
    def get_parameter_range(self, param: str) -> Tuple[float, float]:
        c = self.constraints.get(param)
        if not c:
            return None, None
        return c.get("min"), c.get("max")
    
    def get_default_parameter(self, param: str) -> float:
        return self.constraints.get(param, {}).get("default")
    
    def check_principle(self, principle: str) -> bool:
        return principle in self.principles
    
    def get_algorithm_method(self, algo_name: str) -> str:
        return self.algorithms.get(algo_name, {}).get("method")
    
    def get_required_fields(self, contract_name: str) -> list:
        return self.spec.get("data_contracts", {}).get(contract_name, {}).get("required_fields", [])

    def generate_core_functions(self):
        """根据基因声明生成不可变的核心函数代码（示例）"""
        code = []
        # 生成颜色识别函数占位符（实际应生成完整函数）
        code.append("def color_detection_core(h,s,v):")
        code.append(f"    # 基因强制使用 {self.get_algorithm_method('color_recognition')} 方法")
        code.append("    pass")
        return "\n".join(code)

if __name__ == "__main__":
    interp = GenomeInterpreter("gene_spec.json", "gene_schema.json")
    print("基因版本:", interp.spec["gene_version"])
    print("好奇心阈值范围:", interp.get_parameter_range("curiosity_threshold"))
    print("颜色识别方法:", interp.get_algorithm_method("color_recognition"))
    print("Marks 必填字段:", interp.get_required_fields("Marks"))