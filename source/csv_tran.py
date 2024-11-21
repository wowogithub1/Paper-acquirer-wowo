import csv
import os
import pandas as pd
import shared_data

def csv_tran(target_file,output_file):
 csv_file_path = target_file
 output_file_path = output_file

 def extract_doi_and_save(csv_file_path, output_folder):
    try:
        # 读取 CSV 文件
        df = pd.read_csv(csv_file_path)
        df.columns = df.columns.str.upper()

        # 检查是否存在 DOI 列
        if 'DOI' in df.columns:
            df = df.dropna(subset=['DOI'])  # 删除 DOI 列中包含空值的行
            doi_df = df[['DOI']]  # 提取 DOI 列
            output_file_path = os.path.join(output_folder, 'doi_start.csv')
            shared_data.start_file_path = output_file_path
            doi_df.to_csv(output_file_path, index=False)  # 保存为新的 CSV 文件
            print("成功", f"DOI 列已提取并保存为：{output_file_path}")
        else:
             print("警告", "在选定的 CSV 文件中未找到 DOI 列。")
    except Exception as e:
        print("错误", f"处理过程中发生错误：{str(e)}")

 extract_doi_and_save(csv_file_path,output_file_path)

 
