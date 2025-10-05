import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math
import matplotlib.dates as mdates

def load_order_data():
    # 读取订单数据
    df = pd.read_csv('input/订单列表.csv')
    df['交期'] = pd.to_datetime(df['交期'], format='%Y-%m-%d', errors='coerce')
    return df

def calculate_production_plan(df):
    """
    计算生产计划
    返回: 包含每日生产量的Series
    """
    date_range = pd.date_range(start='2025-03-01', end=df['交期'].max())
    daily_total = pd.Series(0, index=date_range)
    
    # 1. 按天平均分配算法
    # for _, row in df.iterrows():
    #     if pd.notna(row['交期']):  # 确保交期有效
    #         days = (row['交期'] - datetime(2025, 3, 1)).days + 1
    #         if days > 0:  # 确保交期在3月1日之后
    #             daily_avg = row['数量'] / days
    #             for i in range(days):
    #                 date = datetime(2025, 3, 1) + timedelta(days=i)
    #                 daily_total[date] += daily_avg
    
    # 2. 从10月30日开始倒排的均衡算法
    end_date = datetime(2025, 10, 30)
    start_date = datetime(2025, 3, 1)
    total_days = (end_date - start_date).days + 1
    # 计算全局平均值
    total_quantity = df['数量'].sum()
    daily_avg = math.ceil(total_quantity / total_days)
    # 初始化每日生产量和未分配订单
    daily_total = pd.Series(0, index=pd.date_range(start=start_date, end=end_date))
    unallocated_orders = df.copy().sort_values('交期', ascending=False)
    for i in range(total_days - 1, -1, -1):
        current_date = start_date + timedelta(days=i)
        # 循环处理未分配的订单(已按交期从晚到早排序)
        for idx, row in unallocated_orders.iterrows():
            if pd.notna(row['交期']) and row['交期'] >= current_date:
                # 计算可分配数量
                assign = min((daily_avg - daily_total[current_date]), row['数量'])
                daily_total[current_date] += assign
                unallocated_orders.at[idx, '数量'] -= assign
                # 如果订单已全部分配，则标记为已分配
                if unallocated_orders.at[idx, '数量'] <= 0:
                    unallocated_orders = unallocated_orders.drop(idx)
        print
    # 打印未分配完的订单
    if not unallocated_orders.empty:
        print("\n未分配完的订单:")
        print(unallocated_orders[['序号', '数量']])
        print(f"总剩余数量: {unallocated_orders['数量'].sum()}")
    return daily_total

def plot_production_plan(daily_total):
    """绘制生产计划图表"""
    plt.figure(figsize=(15, 6))
    daily_total = daily_total[daily_total > 0]  # 只显示有数据的日期
    if not daily_total.empty:
        # 计算3月1日到10月30日的总天数
        start_date = datetime(2025, 3, 1)
        end_date = datetime(2025, 10, 30)
        total_days = (end_date - start_date).days + 1       
        # 计算所有订单的总数量
        total_quantity = df['数量'].sum()       
        # 计算全局平均值并向上取整
        avg_value = math.ceil(total_quantity / total_days)

        # 绘制生产计划
        daily_total.plot(kind='line', marker='o', label='每日生产量')
        # 绘制平均线
        plt.axhline(y=avg_value, color='r', linestyle='--', label=f'平均值: {avg_value:.2f}')
        
        plt.title('每日生产计划(2025-03-01起)')
        plt.xlabel('日期')
        plt.ylabel('数量')
        plt.xticks(rotation=90)
        ax = plt.gca()
        
        ax.set_xlim([datetime(2025, 3, 1), daily_total.index.max()])
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(3,13)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m'))
        
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("没有有效的生产数据显示")

if __name__ == "__main__":
    df = load_order_data()
    production_plan = calculate_production_plan(df)
    plot_production_plan(production_plan)