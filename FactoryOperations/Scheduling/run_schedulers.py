"""
调度主程序
运行多个调度算法并生成最优生产计划
"""
import pandas as pd
from scheduler import run_schedulers, select_best_plan
from scheduling_utils import SchedulingUtils
from fifo_scheduler import FIFOScheduler
from weighted_priority_scheduler import WeightedPriorityScheduler

def evaluate_plan(plan: pd.DataFrame) -> float:
    """
    评估生产计划
    这里可以自定义评估逻辑，比如:
    - 总生产时间
    - 资源利用率
    - 客户优先级满足度
    """
    # 示例: 评估生产周期(越短越好)
    duration = (plan['生产结束日期'].max() - plan['生产启动日期'].min()).days
    return -duration  # 返回负值表示时间越短分数越高

def main():
    # 1. 读取输入
    utils = SchedulingUtils()
    data = utils.read_input_files(
        orders_path='input/订单列表.csv',
        resources_path='input/设备资源.csv'
    )
    
    # 2. 运行所有调度算法
    schedulers = [FIFOScheduler] #, WeightedPriorityScheduler
    results = run_schedulers(
        orders_path='input/订单列表.csv',
        resources_path='input/设备资源.csv',
        scheduler_classes=schedulers
    )
    
    # 3. 选择最优计划
    best_plan, best_name = select_best_plan(results, evaluate_plan)
    print(f"最优调度算法: {best_name}")
    
    # 4. 保存结果
    utils.save_plan(best_plan)
    print("生产计划已保存到 output/plan_x.csv")

if __name__ == '__main__':
    main()