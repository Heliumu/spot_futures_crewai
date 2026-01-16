# test_current_config_paths.py
from aitrados_api.common_lib.tools.toml_manager import TomlManager

print("=== Testing current config paths ===")

# 尝试不同的路径格式
test_paths = [
    "broker.ctp",
    "broker\\ctp",  # Windows风格
    "broker/ctp",   # Unix风格
    "broker",       # 父级
    "auto_run_brokers",
    "broker.ctp.provider",
    "broker.ctp.userid",
    "broker.ctp.password",
]

for path in test_paths:
    try:
        result = TomlManager.get_value(path)
        print(f"✓ Path '{path}': {result}")
    except Exception as e:
        print(f"✗ Path '{path}': Error - {e}")

print("\n=== Manual TOML read for comparison ===")
import toml
try:
    with open("config.toml", "r", encoding="utf-8") as f:
        manual_config = toml.load(f)
    print("Manual read - broker.ctp:", manual_config.get("broker", {}).get("ctp"))
    print("Manual read - broker:", manual_config.get("broker"))
except Exception as e:
    print("Manual read failed:", e)
