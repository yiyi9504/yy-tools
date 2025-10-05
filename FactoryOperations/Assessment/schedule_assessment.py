import pandas as pd

GrossMargin = 0.3
WorkerNumer = 8
WorkerBaseSalary = 3000

def load_data():
    plan = pd.read_csv('output/plan_x.csv')
    orders = pd.read_csv('input/订单列表.csv')
    products = pd.read_csv('input/产品列表.csv')
    accessories = pd.read_csv('input/配件列表.csv')
    materials = pd.read_csv('input/原料价格表.csv')
    return plan, orders, products, materials

# 计算原材料与人工成本
def calculate_material_cost(plan, orders, products, materials):
    merged = pd.merge(plan, orders.drop(columns=[col for col in plan.columns.difference(['序号']) if col in orders.columns]), on='序号', how='left')
    merged = pd.merge(merged, products.drop(columns=[col for col in merged.columns.difference(['产品代码']) if col in products.columns]), on='产品代码', how='left')
    merged = pd.merge(merged, materials.drop(columns=[col for col in merged.columns.difference(['原料']) if col in materials.columns]), on='原料', how='left')
    merged['单位成本'] = merged['重量（克）'] * merged['价格（元/吨）'] / 1000000
    merged['总成本'] = merged['单位成本'] * merged['数量']
    total_cost = merged['总成本'].sum()
    return total_cost, merged

if __name__ == '__main__':
    plan, orders, products, materials = load_data()
    total_cost, details = calculate_material_cost(plan, orders, products, materials)
    
    print(f"原材料成本总额: {total_cost:.2f} 元")
    print("\n详细计算数据:")
    print(details[['序号', '产品代码', '原料', '重量（克）', '价格（元/吨）', '数量', '单位成本', '总成本']])
    
    # 计算毛利润
    gross_profit = total_cost * GrossMargin
    print(f"\n毛利润: {gross_profit:.2f} 元")
    # 生产用时
    plan['生产启动日期'] = pd.to_datetime(plan['生产启动日期'])
    plan['生产结束日期'] = pd.to_datetime(plan['生产结束日期'])
    # 计算每个订单的生产天数并求和
    production_days = (plan['生产结束日期'] - plan['生产启动日期']).dt.days.sum()
    production_months = production_days / 30
    total_quantity = plan['数量'].sum()
    print(f"生产周期: {production_days} 天，产出 {total_quantity} 件商品")
    # 人力基本工资
    worker_salary = WorkerNumer * WorkerBaseSalary * production_months
    print(f"人力基本工资: {worker_salary:.2f} 元")
    # 计算设备月摊成本
    equipment = pd.read_csv('input/设备资源.csv')
    equipment['总价值'] = equipment['单价(w)'] * 10000 * equipment['台数']
    equipment['月摊成本'] = equipment['总价值'] / equipment['保期(月)']
    total_monthly_cost = equipment['月摊成本'].sum() * production_months
    print(f"设备月摊成本: {total_monthly_cost:.2f} 元")
    # 净利润
    net_profit = gross_profit - worker_salary - total_monthly_cost
    print(f"净利润: {net_profit:.2f} 元")

    # 月合净利润
    monthly_net_profit = (gross_profit - worker_salary - total_monthly_cost) / production_months
    print(f"\n月合净利润: {monthly_net_profit:.2f} 元")
    # 年合资产投入产出比
    annual_net_profit = monthly_net_profit * 12
    equipment_total_value = equipment['总价值'].sum()
    annual_equipment_cost = equipment_total_value / (equipment['保期(月)'].mean() / 12)  # 设备年摊成本
    print(f"年合净利润: {annual_net_profit/10000:.2f} 万元")
    print(f"设备年摊成本: {annual_equipment_cost/10000:.2f} 万元")
    investment_return_ratio = annual_net_profit / annual_equipment_cost
    print(f"年合资产投入产出比: {investment_return_ratio:.2%}")