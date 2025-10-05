import pandas as pd
import math

DailyAvg = 2500 # 34222  # 全局平均日产量

# 读取设备资源数据
device_df = pd.read_csv('input/设备资源.csv')
# 获取实际设备数量(按机器型号分组取最大台数)
real_devices = device_df.groupby('机器型号')['台数'].max().reset_index()
# 合并回原数据
device_df = device_df.merge(real_devices, on='机器型号', suffixes=('', '_实际'))
# 计算总产能
device_df['总产能'] = device_df['日产量'] * device_df['台数_实际']
device_df['平均产能'] = device_df['总产能'] / device_df['台数_实际']

# 按制作类型分析
production_types = device_df['制作类型'].unique()
people_num = 0
for p_type in production_types:
    type_df = device_df[device_df['制作类型'] == p_type]
    total_capacity = type_df['总产能'].sum()
    
    print(f"\n制作类型: {p_type}")
    print(f"总产能: {total_capacity:.0f}",f"({type_df['平均产能'].mean():.0f} 台/天)")
    print(f"需求日产量: {DailyAvg}")
    people_num += DailyAvg * 3 / type_df['平均产能'].mean()

    if total_capacity >= DailyAvg:
        utilization = DailyAvg / total_capacity * 100
        print(f"设备利用率: {utilization:.2f}%")
    else:
        deficit = DailyAvg - total_capacity
        # 计算需要增加的设备(取该类型设备中效率最高的)
        best_device = type_df.loc[type_df['日产量'].idxmax()]
        needed = int(deficit / best_device['日产量']) + 1
        cost = needed * best_device['单价(w)']
        print(f"设备缺口率: {100-total_capacity/DailyAvg*100:.2f}%")
        print(f"产能不足，需要增加: {needed}台 {best_device['机器型号']}")
        print(f"预计投入: {cost:.2f}W元")
        
print(f"\n人工班次总需求: {math.ceil(people_num)} 班/天 (每班8小时)")