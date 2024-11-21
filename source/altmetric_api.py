# imports
import csv
import pandas as pd
import re
import json
import requests
import sys
import datetime
import os
import time

# fields to be scrapped from altmetric
metric_keys = [
    "score",
    "cited_by_fbwalls_count",
    "cited_by_rdts_count",
    "cited_by_tweeters_count",
    "cited_by_gplus_count",
    "cited_by_msm_count",
    "cited_by_delicious_count",
    "cited_by_qs_count",
    "cited_by_posts_count"
]

def get_altmetric(input_file):
    # reads in or asks user for input file
    DOIs = []
    df = pd.read_csv(input_file, quoting=csv.QUOTE_ALL)
    old_columns = df.columns.tolist()
    # 检查是否存在 DOI 列
    if 'DOI' in df.columns:
        doi_df = df[['DOI']]  # 提取 DOI 列
        DOIs = doi_df['DOI'].values.tolist()  # 将 DOI 列数据放入 DOIs 列表中

    papers = []  # 用于存储论文信息
    results = []  # 用于存储解析后的 JSON 数据
    data1={
            "score": "",
            "cited_by_fbwalls_count": "",
            "cited_by_rdts_count": "",
            "cited_by_tweeters_count": "",
            "cited_by_wikipedia_count": "",
            "cited_by_accounts_count": "",
            "cited_by_feeds_count": "",
            "cited_by_gplus_count": "",
            "cited_by_posts_count": "",
            "cited_by_msm_count": "",
            "cited_by_delicious_count": "",
            "cited_by_qs_count": ""
         }

    for doi in DOIs:
        doi = str(doi)
        # Get request for this doi will be sent to altmetric
        request_url = "https://api.altmetric.com/v1/doi/" + doi
        try:
         response = requests.get(request_url)
         data = response.json()
         if  response.status_code == 429:
                print("请求过多，稍后重试...")
                time.sleep(10)  # 等待10秒再重试
                continue 
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP错误: {http_err}，对于DOI: {doi}")
            data=data1
        except requests.exceptions.RequestException as req_err:
            print(f"请求错误: {req_err}，对于DOI: {doi}")
            time.sleep(1)  # 等待10秒再重试
            data=data1
        except Exception as e:
            print(f"解析JSON时遇到异常: {e}，对于DOI: {doi}")
            data=data1
        # 假设您的结果数据保存在 results 列表中
        # output_file = "output.json"  # 用于保存 JSON 数据的文件名
        if not data:
         print("未获取到data数据")
         data=data1
         
        '''
        # 将结果写入 JSON 文件
        output_file = f"{doi.replace('/', '_')}_data.json" # 生成输出文件的文件名
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        '''
        score = data.get("score", "")
        cited_by_fbwalls_count= data.get("cited_by_fbwalls_count", "")
        cited_by_rdts_count= data.get("cited_by_rdts_count", "")
        cited_by_tweeters_count= data.get("cited_by_tweeters_count", "")
        cited_by_wikipedia_count= data.get("cited_by_wikipedia_count", "")
        cited_by_accounts_count= data.get("cited_by_accounts_count", "")
        cited_by_feeds_count= data.get("cited_by_feeds_count", "")
        cited_by_gplus_count= data.get("cited_by_gplus_count", "")
        cited_by_posts_count= data.get("cited_by_posts_count", "")
        cited_by_msm_count= data.get("cited_by_msm_count", "")
        cited_by_delicious_count= data.get("cited_by_delicious_count", "")
        cited_by_qs_count= data.get("cited_by_qs_count", "")

    # 构造论文信息字典
        paper_info = {
        'score' : score,
        'cited_by_fbwalls_count': cited_by_fbwalls_count,
        'cited_by_rdts_count': cited_by_rdts_count,
        'cited_by_tweeters_count': cited_by_tweeters_count,
        'cited_by_wikipedia_count': cited_by_wikipedia_count,
        'cited_by_accounts_count': cited_by_accounts_count,
        'cited_by_feeds_count': cited_by_feeds_count,
        'cited_by_gplus_count': cited_by_gplus_count,
        'cited_by_posts_count': cited_by_posts_count,
        'cited_by_msm_count': cited_by_msm_count,
        'cited_by_delicious_count': cited_by_delicious_count,
        'cited_by_qs_count': cited_by_qs_count

    }
        papers.append(paper_info)
        time.sleep(1)
        
    # 创建DataFrame
    df2 = pd.DataFrame(papers)
    df1 = pd.read_csv(input_file)
    result_df = pd.concat([df1, df2], axis=1)  # 合并 DataFrame
    result_df.to_csv(input_file, index=False, encoding='utf-8-sig')  # 保存为CSV文件

