from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    principal = float(data['principal'])
    annual_rate = float(data['annual_rate']) / 100
    inflation_rate = float(data['inflation_rate']) / 100
    monthly_income = float(data['monthly_income'])
    monthly_expense = float(data['monthly_expense'])
    months = int(data['months'])
    operations = data['operations']

    balances = [principal]
    incomes = [monthly_income]
    expenses = [monthly_expense]
    current_balance = principal
    monthly_rate = annual_rate / 12
    monthly_inflation = inflation_rate / 12

    income_changes = {}
    expense_changes = {}

    for op in operations:
        if op['type'] == 'salary':
            income_changes[op['month']] = income_changes.get(op['month'], 0) + op['amount']
        elif op['type'] == 'expense':
            expense_changes[op['month']] = expense_changes.get(op['month'], 0) + op['amount']

    for month in range(1, months + 1):
        current_income = monthly_income #* (1 + monthly_inflation) ** month
        current_expense = monthly_expense * (1 + monthly_inflation) ** month

        # 应用累积的收入和支出变化
        for change_month, change_amount in income_changes.items():
            if month >= change_month:
                current_income += change_amount #* (1 + monthly_inflation) ** (month - change_month + 1)

        for change_month, change_amount in expense_changes.items():
            if month >= change_month:
                current_expense += change_amount * (1 + monthly_inflation) ** (month - change_month + 1)

        # 应用一次性支出
        for op in operations:
            if op['type'] == 'oneTime' and op['month'] == month:
                current_expense += op['amount']

        net_savings = current_income - current_expense
        current_balance = (current_balance + net_savings) * (1 + monthly_rate)
        
        balances.append(current_balance)
        incomes.append(current_income)
        expenses.append(current_expense)

        if current_balance <= 0:
            return jsonify({
                'result': f'资金在第 {month} 个月耗尽',
                'balances': balances,
                'incomes': incomes,
                'expenses': expenses,
                'depleted': True,
                'depleted_month': month
            })

    return jsonify({
        'result': f'{months} 个月后的最终余额: {current_balance:.2f}',
        'balances': balances,
        'incomes': incomes,
        'expenses': expenses,
        'depleted': False
    })

if __name__ == '__main__':
    app.run(debug=True)