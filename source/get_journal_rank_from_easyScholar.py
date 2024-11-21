import os
import time
import pandas as pd
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
import re
import shared_data

def get_journal_rank_from_easyScholar(meta_data):
# Fetch the API key from environment variables
 secretKey = ''
 '''
 if not API_KEY:
    raise ValueError("API key not found in environment variables.")
 '''

 http = Session()
 http.mount('https://', HTTPAdapter(max_retries=Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods={"HEAD", "GET", "OPTIONS"}
 )))

  # 读取存储 journal 信息的 CSV 文件
 journal_df = pd.read_csv(meta_data)  # csv 文件路径
 journal_list = journal_df['Journal'].tolist()  # 假设 'Journal' 是列名

 # 用于存储结果的列表
 journals = []

 for journal in journal_list :
        try:
            response = http.get(
                f"https://www.easyscholar.cc/open/getPublicationRank",
                headers={},
                params={
                    'secretKey': secretKey,
                    'publicationName': journal,
                }
                )

            response.raise_for_status()  # Ensures we stop if there's an error
            data = response.json()
            # 输出到CSV文件的逻辑

            official_rank = data.get('data', {}).get('officialRank', {}).get('all', {})
            #combined_official_rank = ', '.join( for key, value in data.get())
            '''
                # 保存 JSON文件,方便查询调试
            with open(f'{journal}.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)  # 保存 JSON 文件
            '''
                # 处理 rankInfo
            
            journal_info = {
                'journal_rank': official_rank,  # 根据期刊的名称获取官方等级
                'SCI_IF': official_rank.get('sciif', '') , # 假设你需要的排名详情
                'SCI_IF5':official_rank.get('sciif5', ''),
                'JCI' : official_rank.get('jci', '')
            }
            journals.append(journal_info)
            time.sleep(0.55)  # 避免频繁请求
        except Exception as e:
                print(f"处理 DOI {journal} 时发生错误: {e}，已跳过该项。")

 result_df = pd.DataFrame(journals)
 journal_index = journal_df.columns.get_loc('Journal')
 a = journal_df.columns.tolist()
 b = result_df.columns.tolist()
 new_column_order = a[:journal_index+1] + b + a[journal_index+1:]
 #print(new_column_order)
 new_df = pd.DataFrame(columns=new_column_order)

 for col in new_column_order:
    if col in journal_df.columns:
        new_df[col] = journal_df[col]  # 从 journal_df 获取数据
    if col in result_df.columns:
        new_df[col] = result_df[col]  

 new_df.to_csv(meta_data, index=False, encoding='utf-8-sig')
    


if __name__ == "__main__":
    get_journal_rank_from_easyScholar('paper_meta_data.csv')

