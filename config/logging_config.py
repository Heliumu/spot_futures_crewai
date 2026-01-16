# config/logging_config.py
import logging
import os
from datetime import datetime

def setup_logging():
    """设置详细的日志配置"""
    # 创建logs目录
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,  # 关键：设置为DEBUG级别
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(
                filename=f'logs/data_fetch_{datetime.now().strftime("%Y%m%d")}.log', 
                mode='a', 
                encoding='utf-8'
            ),
            logging.StreamHandler()  # 同时输出到控制台
        ]
    )
    
    # 为特定模块设置DEBUG级别
    logging.getLogger("tools.edt_data_tool_enhanced_debug").setLevel(logging.DEBUG)
    logging.getLogger("__main__").setLevel(logging.DEBUG)
    
    return logging.getLogger(__name__)
