import os
from requests import Session
import pandas as pd
import urllib3
urllib3.disable_warnings()
import time
from full_text_from_semanticScholar_api import download_paper
from tenacity import retry, stop_after_attempt, wait_fixed
import shared_data 

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def attempt_download(session, doi, directory, user_agent):
    return download_paper(session, doi, directory, user_agent)

def download_papers_from_csv(csv_file: str, directory: str):
    # 读取CSV文件
    df = pd.read_csv(csv_file)
    user_agent = 'requests/2.0.0'
    directory = os.path.join(directory, 'open_access_papers')
    os.makedirs(directory, exist_ok=True)

    # 创建一个请求会话
    with Session() as session:
        failed_dois = []
        # 遍历每一行，假设DOI信息在名为'doi'的列中
        for doi in df['DOI']:
            print(f"正在下载DOI: {doi}")
            try:
                pdf_path = attempt_download(session, doi, directory, user_agent)        
                if pdf_path:
                    new_pdf_path = os.path.join(directory, f"{doi.replace('/', '_')}.pdf")  # 用下划线替换斜杠
                    os.rename(pdf_path, new_pdf_path)  # 重命名文件
                    print(f"成功下载论文，保存路径: {new_pdf_path}")
                else:
                    print(f"DOI {doi} 的论文无法下载或不是开放获取。")
                    failed_dois.append(doi)
            except Exception as e:
                print(f"下载DOI {doi} 的论文时出错: {e}")
                failed_dois.append(doi)
            time.sleep(3)    # 休眠3秒，防止请求频率过高

    if failed_dois:
        failed_csv_file = os.path.join(directory, 'open-access-failed-dois.csv')
        shared_data.temp = failed_csv_file
        failed_df = pd.DataFrame(failed_dois, columns=['DOI'])
        failed_df.to_csv(failed_csv_file, index=False)
        print(f"失败的DOI已保存到 '{failed_csv_file}' 文件。")

if __name__ == '__main__':
    csv_file = r'dois.csv'  # 替换为你的CSV文件路径
    directory = r'D:\paper_acquirer\task_2024-11-20_17-35-11\target'  # 论文存储的目录
      # 用户代理
    download_papers_from_csv(csv_file, directory)