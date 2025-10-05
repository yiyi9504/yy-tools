import pandas as pd
import os
import sys

def xlsx_to_csv(input_file, output_folder='output'):
    """
    将xlsx文件的每个工作表转换为单独的csv文件
    :param input_file: 输入的xlsx文件路径
    :param output_folder: 输出文件夹路径
    """
    try:
        # 创建输出文件夹
        os.makedirs(output_folder, exist_ok=True)
        # 读取所有工作表
        sheets = pd.read_excel(input_file, sheet_name=None)
        # 遍历每个工作表并保存为csv
        for sheet_name, df in sheets.items():
            # 替换特殊字符避免文件名问题
            safe_name = ''.join(c if c.isalnum() else '_' for c in sheet_name)
            output_path = os.path.join(output_folder, f"{safe_name}.csv")
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"已生成: {output_path}")
        
        print(f"转换完成，共生成 {len(sheets)} 个csv文件")
    except Exception as e:
        print(f"错误发生: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python xlsx2csv.py <xlsx文件路径> [输出文件夹]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else 'output'
    xlsx_to_csv(input_file, output_folder)