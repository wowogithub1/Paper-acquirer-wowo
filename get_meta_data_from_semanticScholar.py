import os
import time
import pandas as pd
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
import re
import shared_data

def clean_doi(doi):
    return re.sub(r'[<>:"/\\|?*]', '_', doi)  # 用下划线替换不合法字符

def get_meta_data_from_semantic_scholar(doi_start,target_folder):
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
 doi_df = pd.read_csv(doi_start)  # csv 文件路径
 doi_list = doi_df['DOI'].tolist()  # 假设 'DOI' 是列名



 # Define the search query and filters
 fields = "title,authors.name,authors.paperCount,authors.citationCount,authors.hIndex,journal,externalIds,publicationDate,referenceCount,citationCount,influentialCitationCount,fieldsOfStudy"
 limit = 1000  # Fetch up to 1000 papers in one request
 # 用于存储结果的列表
 papers = []

 for paper_id in doi_list:
  try:
   response = http.get(
    f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}",
    headers={'x-api-key': API_KEY},
    params={
        'fields': fields,
        'limit': limit,
    }
    )
   response.raise_for_status()  # Ensures we stop if there's an error
   data = response.json()

   '''
  # 保存 JSON文件,方便查询调试
   cleaned_doi = clean_doi(paper_id)  # 清理 DOI,生成合法的文件名
   with open(f'citation_data_{cleaned_doi}.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)  # 保存 JSON 文件
   '''

  # 输出到CSV文件的逻辑
   externalIds = data.get('externalIds', {})  # 使用 {} 作为默认值，防止 KeyError
   title = data.get('title')
   authors = ', '.join(author['name'] for author in data.get('authors', []))  # 合并作者名字为一个字符串
   au_paper_count = ', '.join(str(author['paperCount']) for author in data.get('authors', [])) 
   au_citation_count = ', '.join(str(author['citationCount']) for author in data.get('authors', []))  
   au_h_index  = ', '.join(str(author['hIndex']) for author in data.get('authors', [])) 
   journal =data.get('journal', {}).get('name', {})
   fieldsOfStudy = data.get('fieldsOfStudy', '')  # 提取论文领域
   publicationDate = data.get('publicationDate', '')  # 提取出版日期
   referenceCount = data.get('referenceCount', '')  # 提取引用数量
   citationCount = data.get('citationCount', '')  # 提取被引用数量
   influentialCitationCount = data.get('influentialCitationCount', '')  # 提取影响力引用数量
  
    # 构造论文信息字典
   paper_info = {
        'externalIds': externalIds,
        'DOI' : '{}',
        'Title': title,
        'Authors': authors,
        'paperCount': au_paper_count,
        'citationCount': au_citation_count,
        'hIndex': au_h_index,
        'Journal': journal,
        'Fields of Study': fieldsOfStudy,
        'Publication Date': publicationDate,
        'Reference Count': referenceCount,
        'Citation Count': citationCount,
        'Influential Citation Count': influentialCitationCount,
    }
   papers.append(paper_info)
   time.sleep(0.2)  # 避免请求过快被服务器拒绝
  except Exception as e:
   print(f"处理 DOI {paper_id} 时发生错误: {e}，已跳过该项。")

 # 创建DataFrame并保存为CSV
 df = pd.DataFrame(papers)
 df.to_csv('given_paper_data.csv', index=False, encoding='utf-8-sig')  # 保存为CSV文件

 # 读取 CSV 文件
 df = pd.read_csv('given_paper_data.csv')
 # 定义一个提取 DOI 的函数
 def extract_doi(text):
    # 使用正则表达式查找包含 "doi:" 的部分并提取其后的内容
    match = re.search(r"'DOI':\s*'([^']+)'", text)
    if match:
        return match.group(1)  # 返回匹配的 DOI 部分
    return ''  # 如果没有匹配，返回空字符串
 '''
 def extract_journal(text):
   match = re.search(r"'journalName':\s*'([^']+)'", text)
   if match:
        return match.group(1)  # 返回匹配的 DOI 部分
   return ''  # 如果没有匹配，返回空字符串
 '''
 # 应用提取 DOI 的函数，生成新列 'DOI'
 df['DOI'] = df['externalIds']
 df['DOI'] = df['DOI'].astype(str)
 df['DOI'] = df['DOI'].apply(extract_doi)
 df['DOI'] = df['DOI'].astype(str)

 # 保存更新后的 DataFrame 到新的 CSV 文件
 output_file_name = os.path.join(target_folder, "paper_meta_data.csv") 
 df.to_csv(output_file_name, index=False)
 shared_data.temp = output_file_name

 if os.path.exists('given_paper_data.csv'):
    os.remove('given_paper_data.csv')  # 删除文件
 '''
 # Handle continuation token if there are more results to fetch
 if 'token' in data:
    print(f"Continuation Token: {data['token']}")
 '''

if __name__ == "__main__":
    get_meta_data_from_semantic_scholar('dois.csv','.')

