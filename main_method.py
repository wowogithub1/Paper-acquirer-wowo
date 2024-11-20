import os
import shared_data
import graphical_user_interface
import csv_tran
import get_meta_data_from_semanticScholar
import altmetric_api
import get_reference_data_from_semanticScholar
import get_citation_data_from_semanticScholar
import get_full_text_from_semanticScholar
import get_full_text_from_scihub
import get_journal_rank_from_easyScholar
import main_method

def get_meta_data_main(start_path,start_doi,target_path,target_meta_data):
    try:
        csv_tran.csv_tran(start_path,target_path)
        get_meta_data_from_semanticScholar.get_meta_data_from_semantic_scholar(start_doi,target_path)
        target_meta_data = shared_data.temp
        altmetric_api.get_altmetric(target_meta_data)
        get_journal_rank_from_easyScholar.get_journal_rank_from_easyScholar(target_meta_data)
        #os.remove(shared_data.start_file_path)
    except Exception as e:
        print(f"获取{target_path}文献元数据时出现错误: {e}")    