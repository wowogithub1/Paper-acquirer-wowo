import os
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import pandas as pd
import json
import re

# Fetch the API key from environment variables
API_KEY = ''

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

# 读取存储 DOI 的 CSV 文件
doi_df = pd.read_csv('dois.csv')  # 假定 CSV 文件名为 dois.csv
doi_list = doi_df['DOI'].tolist()  # 假设 'DOI' 是列名
# 用于存储结果的列表
papers = []

# 检索字段
fields = "externalIds,title,publicationDate,authors,fieldsOfStudy,referenceCount,citationCount,influentialCitationCount"
# 检索信息
query = "Altmetrics Altmetric"
limit = 1000  # Fetch up to 1000 papers in one request
publication_types = "JournalArticle,Review"  # Filter by publication types
fields_of_study = "computer science"  # Filter by fields of study
year = "2020-2023"  # Papers published between 2020 and 2023

token = None  # 初始化 token
while True:
    # 进行请求，判断是否有 token，需要继续查询
    params = {
        'query': query,
        'fields': fields,
        'limit': limit,
        #'publicationTypes': publication_types,
        #'fieldsOfStudy': fields_of_study,
        #'year': year
    }
    if token:
        params['token'] = token  # 如果有 token，则添加到请求参数中


    response = http.get(
    "https://api.semanticscholar.org/graph/v1/paper/search/bulk",
    headers={'x-api-key': API_KEY},
    params=params
    )

    response.raise_for_status()  # Ensures we stop if there's an error
    data = response.json()

 # 输出到CSV文件的逻辑
    for paper in data.get('data', []):
     externalIds = paper.get('externalIds', {})  # 使用 {} 作为默认值，防止 KeyError
     title = paper.get('title')
     authors = ', '.join(author['name'] for author in paper.get('authors', []))  # 合并作者名字为一个字符串
     fieldsOfStudy = paper.get('fieldsOfStudy', [])  # 提取论文领域
     publicationDate = paper.get('publicationDate', '')  # 提取出版日期
     referenceCount = paper.get('referenceCount', '')  # 提取引用数量
     citationCount = paper.get('citationCount', '')  # 提取被引用数量
     influentialCitationCount = paper.get('influentialCitationCount', '')  # 提取影响力引用数量

    # 构造论文信息字典
     paper_info = {
        'externalIds': externalIds,
        'DOI' : '{}',
        'Title': title,
        'Authors': authors,
        'Fields of Study': fieldsOfStudy,
        'Publication Date': publicationDate,
        'Reference Count': referenceCount,
        'Citation Count': citationCount,
        'Influential Citation Count': influentialCitationCount,
    }
     papers.append(paper_info)

    token = data.get('token')
    if not token:  # 如果没有 token 了，说明所有页都已经请求完毕，退出循环
        break


# 创建DataFrame并保存为CSV
df = pd.DataFrame(papers)
df.to_csv('semantic_scholar_meta_data.csv', index=False, encoding='utf-8-sig')  # 保存为CSV文件

# 读取 CSV 文件
df = pd.read_csv('semantic_scholar_meta_data.csv')
# 定义一个提取 DOI 的函数
def extract_doi(text):
    # 使用正则表达式查找包含 "doi:" 的部分并提取其后的内容
    match = re.search(r"'DOI':\s*'([^']+)'", text)
    if match:
        return match.group(1)  # 返回匹配的 DOI 部分
    return ''  # 如果没有匹配，返回空字符串

# 假设需要提取的列名为 'citing_paper_Ids'
# 应用提取 DOI 的函数，生成新列 'DOI'
df['externalIds'] = df['externalIds'].astype(str)
df['DOI'] = df['externalIds'].apply(extract_doi)

# 保存更新后的 DataFrame 到新的 CSV 文件
output_path = "semantic_scholar_meta_data.csv"
df.to_csv(output_path, index=False)

'''
# Handle continuation token if there are more results to fetch
if 'token' in data:
    print(f"Continuation Token: {data['token']}")
'''