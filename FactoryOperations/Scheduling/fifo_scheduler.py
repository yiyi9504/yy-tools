from scheduler import BaseScheduler
import pandas as pd

class FIFOScheduler(BaseScheduler):
    """
    先进先出调度算法
    """
    def schedule(self, orders: pd.DataFrame, resources: pd.DataFrame) -> pd.DataFrame:
        # 简单按订单顺序安排生产
        plan = orders.copy()
        plan['生产启动日期'] = pd.to_datetime('today')
        plan['生产结束日期'] = plan['生产启动日期'] + pd.to_timedelta(plan['数量']/40000, unit='d')  # 假设每天生产1000件
        return plan