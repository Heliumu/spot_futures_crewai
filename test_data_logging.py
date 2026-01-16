# test_data_logging.py
import logging
from tools.enhanced_data_fetching_tool import EnhancedEDBDataTool

def test_data_logging():
    """测试数据日志功能"""
    # 设置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/test_data.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("测试数据日志功能开始")
    
    # 创建工具实例
    tool = EnhancedEDBDataTool()
    
    # 测试获取数据
    start_date = "2025-07-18"
    end_date = "2026-01-16"
    
    # 获取库存数据
    logger.info("测试库存数据分析")
    result = tool.get_inventory_analysis_data(start_date, end_date)
    logger.info(f"库存分析结果: {result}")
    
    # 获取基差数据
    logger.info("测试基差数据分析")
    result = tool.get_basis_analysis_data(start_date, end_date)
    logger.info(f"基差分析结果: {result}")

if __name__ == "__main__":
    test_data_logging()
