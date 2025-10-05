from scheduler import BaseScheduler
import pandas as pd
import numpy as np

class WeightedPriorityScheduler(BaseScheduler):
    """
    加权优先调度算法
    根据客户优先级、订单金额等因素加权计算优先级
    """
    def __init__(self, 
                 customer_weight: float = 0.4,
                 revenue_weight: float = 0.4,
                 urgency_weight: float = 0.2):
        self.customer_weight = customer_weight
        self.revenue_weight = revenue_weight
        self.urgency_weight = urgency_weight
    
    def calculate_priority(self, order: pd.Series) -> float:
        """计算订单优先级分数"""
        # 标准化各指标（假设已有相关字段）
        customer_priority = order.get('客户优先级', 1)
        revenue = order.get('金额', 0)
        days_remaining = order.get('交付期限天数', 7)
        
        # 计算加权分数
        score = (self.customer_weight * customer_priority +
                self.revenue_weight * revenue +
                self.urgency_weight * (1/days_remaining))
        return score
    
    def schedule(self, orders: pd.DataFrame, resources: pd.DataFrame) -> pd.DataFrame:
        # 计算每个订单的优先级
        orders['优先级分数'] = orders.apply(self.calculate_priority, axis=1)
        # 按优先级排序
        sorted_orders = orders.sort_values('优先级分数', ascending=False)
        
        # 生成生产计划
        plan = sorted_orders.copy()
        plan['生产启动日期'] = pd.to_datetime('today')
        # 简化的生产时间估算
        plan['生产结束日期'] = plan['生产启动日期'] + pd.to_timedelta(
            plan['数量']/1000 * (1 - plan['优先级分数'].rank(pct=True)), 
            unit='d')
        
        return plan