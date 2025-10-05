from abc import ABC, abstractmethod
import pandas as pd
from scheduling_utils import SchedulingUtils

class BaseScheduler(ABC):
    """
    调度器抽象基类
    所有具体调度算法需要实现此接口
    """
    @abstractmethod
    def schedule(self, orders: pd.DataFrame, resources: pd.DataFrame) -> pd.DataFrame:
        """
        调度方法
        :param orders: 订单数据
        :param resources: 资源数据
        :return: 生产计划
        """
        pass


def run_schedulers(orders_path: str, resources_path: str, scheduler_classes: list):
    """
    运行多个调度器并返回结果
    :param orders_path: 订单文件路径
    :param resources_path: 资源文件路径
    :param scheduler_classes: 调度器类列表
    :return: 各调度器结果字典 {调度器名称: 生产计划}
    """
    orders = pd.read_csv(orders_path)
    resources = pd.read_csv(resources_path)
    
    results = {}
    for scheduler_class in scheduler_classes:
        scheduler = scheduler_class()
        plan = scheduler.schedule(orders, resources)
        results[scheduler.__class__.__name__] = plan
    
    return results


def select_best_plan(plans: dict, evaluator):
    """
    选择最优生产计划
    :param plans: 调度结果字典 {调度器名称: 生产计划}
    :param evaluator: 评估函数，接受plan返回评估分数
    :return: (最优计划, 调度器名称)
    """
    scored_plans = [(name, evaluator(plan)) for name, plan in plans.items()]
    best_name, _ = max(scored_plans, key=lambda x: x[1])
    return plans[best_name], best_name