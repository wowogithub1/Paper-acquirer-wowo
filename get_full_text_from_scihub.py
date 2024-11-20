from scihub_api import SciHub
import csv
import os
import uuid
import time
import pandas as pd

def download_papers_from_scihub(work_dir,read_dir):
    full_text_folder_path = os.path.join(work_dir, 'not_open_access_papers')
    # 创建下载目录（如果不存在的话）
    os.makedirs(full_text_folder_path, exist_ok=True)
    # 合并文件夹路径和文件名
    sh = SciHub()# 创建 SciHub 实例

    #单个文献下载
    #result = sh.download('10.1371/journal.pone.0048753',path=full_text_file_path)


    # 读取 DOI 的 CSV 文件
    with open(read_dir, newline='') as csvfile:
        #reader = csv.reader(csvfile)
        df = pd.read_csv(csvfile)
        # 假设 DOI 在 CSV 文件的第一列中   
        failed_dois = []
        # 遍历每一行，假设DOI信息在名为'doi'的列中
        for doi in df['DOI']:
         try:
            print(f"Downloading {doi}...")  # 打印正在下载的 DOI

        #更新下载路径
            unique_filename = f"{doi.replace('/', '_')}.pdf"
            full_text_file_path = os.path.join(full_text_folder_path, unique_filename)  

            # 尝试下载文献，并在失败时重试
            download_successful = False
            retries = 3  # 最大重试次数
            for attempt in range(retries):
                try:
                    # 下载文献
                    result = sh.download(doi, path=full_text_file_path)
                    download_successful = True  # 下载成功
                    #print(f"Downloaded: {result}")  # 打印下载结果
                    print(f"Downloaded successfully: {doi}")  # 打印下载结果
                    break  # 跳出重试循环
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == retries - 1:
                        print(f"最终重试失败，无法下载 DOI: {doi}")
                    time.sleep(2.5)  # 等待几秒后重试
                    failed_dois.append(doi)
            time.sleep(3)  # 等待 3 秒，防止被 Sci-Hub 封 IP
         except Exception as e:
            print(f"Failed to download DOI: {doi}, error: {e}")
            failed_dois.append(doi)
            continue

    
    failed_csv_file = os.path.join(full_text_folder_path, 'final-failed-papers-dois.csv')
    failed_df = pd.DataFrame(failed_dois, columns=['DOI'])
    failed_df.to_csv(failed_csv_file, index=False)
    print(f"失败的DOI已保存到 '{failed_csv_file}' 文件。")   
