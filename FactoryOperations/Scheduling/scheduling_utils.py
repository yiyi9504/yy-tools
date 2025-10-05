import pandas as pd
from typing import Dict, Any
import os

class SchedulingUtils:
    """
    调度公共工具类
    处理文件读写、条件检查等公共逻辑
    """
    
    @staticmethod
    def read_input_files(orders_path: str, resources_path: str) -> Dict[str, pd.DataFrame]:
        """
        读取输入文件
        :return: {'orders': 订单数据, 'resources': 资源数据}
        """
        if not os.path.exists(orders_path):
            raise FileNotFoundError(f"订单文件不存在: {orders_path}")
        if not os.path.exists(resources_path):
            raise FileNotFoundError(f"资源文件不存在: {resources_path}")
            
        return {
            'orders': pd.read_csv(orders_path),
            'resources': pd.read_csv(resources_path)
        }
    
    @staticmethod
    def validate_inputs(data: Dict[str, pd.DataFrame], required_columns: Dict[str, list]) -> None:
        """验证输入数据是否包含必要列"""
        for data_type, columns in required_columns.items():
            if data_type not in data:
                raise ValueError(f"缺少数据类型: {data_type}")
                
            missing = [col for col in columns if col not in data[data_type].columns]
            if missing:
                raise ValueError(f"{data_type}数据缺少必要列: {missing}")
    
    @staticmethod
    def save_plan(plan: pd.DataFrame, output_path: str = './output/plan_x.csv') -> None:
        """保存生产计划"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plan.to_csv(output_path, index=False)
        
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'daily_production_capacity': 1000,  # 默认日产能
            'max_workers': 50,  # 最大工人数
            'work_hours_per_day': 8  # 每日工作小时数
        }