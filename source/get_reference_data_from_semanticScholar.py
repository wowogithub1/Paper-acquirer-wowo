import os
import pandas as pd
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
import re
import shared_data

def clean_doi(doi):
    return re.sub(r'[<>:"/\\|?*]', '_', doi)  # 用下划线替换不合法字符

def get_reference_data_from_semantic_scholar(doi_start,target_folder):
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
 doi_df = pd.read_csv(doi_start)  # 假定 CSV 文件名为 dois.csv
 doi_list = doi_df['DOI'].tolist()  # 假设 'DOI' 是列名



# Define the search query and filters
 fields = "contexts,intents,isInfluential,title,authors,externalIds,year,referenceCount,citationCount,influentialCitationCount,fieldsOfStudy"
 limit = 1000  # Fetch up to 1000 papers in one request

 for paper_id in doi_list:
  response = http.get(
    f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references",
    headers={'x-api-key': API_KEY},
    params={
        'fields': fields,
        'limit': limit,
     }
  )
  response.raise_for_status()  # Ensures we stop if there's an error
  data = response.json()
 # 用于存储结果的列表
  papers = []
 '''
 # 保存 JSON文件,方便查询调试
 cleaned_doi = clean_doi(paper_id)  # 清理 DOI,生成合法的文件名
 with open(f'reference_data_{cleaned_doi}.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)  # 保存 JSON 文件
 '''
  
 # 输出到CSV文件的逻辑
 for paper in data.get('data', []):
     contextsWithIntent = paper.get('contextsWithIntent', {})
     contexts = paper.get('contexts', [])
     intents = paper.get('intents', [])
     is_influential = paper.get('isInfluential', {})
     cited_paper = paper.get('citedPaper', {})  # 获取引用论文的信息
     externalIds = cited_paper.get('externalIds', {})  # 使用 {} 作为默认值，防止 KeyError
     doi= '[]'
     authors = [author['name'] for author in cited_paper.get('authors', [])]  # 提取作者名单
     title = cited_paper.get('title', '{}')  # 提取标题
     year = cited_paper.get('year', '{}')  
     referenceCount = cited_paper.get('referenceCount', '{}')  
     citationCount = cited_paper.get('citationCount', '{}') 
     influentialCitationCount= cited_paper.get('influentialCitationCount', '{}')
     fieldsOfStudy= cited_paper.get('fieldsOfStudy', '{}')

    # 构造论文信息字典
     paper_info = {
        'raw_paper_doi' : paper_id,
        'cited_paper_Ids': externalIds,
        'DOI': doi,
        'title': title,
        'Authors': ', '.join(authors),
        'Year': year,  # 添加年份
        'Fields of Study': '; '.join(fieldsOfStudy) if isinstance(fieldsOfStudy, list) else fieldsOfStudy,  # 添加研究领域
        'Reference Count': referenceCount,  # 添加引用数量
        'Citation Count': citationCount,  # 添加被引用数量
        'Influential Citation Count': influentialCitationCount,  # 添加影响力引用数量
        'Is Influential': is_influential,
        'Contexts': '; '.join(contexts),  # 将上下文合并为一个字符串
        'Intents': ', '.join(intents),      # 将意图合并为一个字符串
    }
     papers.append(paper_info)

 # 创建DataFrame并保存为CSV
 output_file_name = os.path.join(target_folder, "reference_data.csv") 
 df = pd.DataFrame(papers)
 df.to_csv(output_file_name, index=False, encoding='utf-8-sig')  # 保存为CSV文件

 # 读取 CSV 文件
 df = pd.read_csv(output_file_name)
 # 定义一个提取 DOI 的函数
 def extract_doi(text):
    # 使用正则表达式查找包含 "doi:" 的部分并提取其后的内容
    match = re.search(r"'DOI':\s*'([^']+)'", text)
    if match:
        return match.group(1)  # 返回匹配的 DOI 部分
    return ''  # 如果没有匹配，返回空字符串

 # 假设需要提取的列名为 'citing_paper_Ids'
  # 应用提取 DOI 的函数，生成新列 'DOI'
 df['DOI'] = df['cited_paper_Ids']
 df['DOI'] = df['DOI'].astype(str)
 df['DOI'] = df['DOI'].apply(extract_doi)
 df['DOI'] = df['DOI'].astype(str)

 # 保存更新后的 DataFrame 到新的 CSV 文件
 df.to_csv(output_file_name, index=False)
 shared_data.temp = output_file_name
 
 '''
 # Handle continuation token if there are more results to fetch
 if 'token' in data:
    print(f"Continuation Token: {data['token']}")
 '''