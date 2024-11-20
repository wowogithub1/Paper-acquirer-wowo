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

if __name__ == "__main__":
    #启动GUI
    graphical_user_interface.run_gui()
    if shared_data.selected_file_path == "":
        exit()

    #获取目标文献数据
    try:
        csv_tran.csv_tran(shared_data.selected_file_path,shared_data.folder_target_path)
        get_meta_data_from_semanticScholar.get_meta_data_from_semantic_scholar(shared_data.start_file_path,shared_data.folder_target_path)
        shared_data.folder_target_meta_data = shared_data.temp
        altmetric_api.get_altmetric(shared_data.folder_target_meta_data)
        get_journal_rank_from_easyScholar.get_journal_rank_from_easyScholar(shared_data.folder_target_meta_data)
        #os.remove(shared_data.start_file_path)
    except Exception as e:
        print(f"获取目标文献数据时出现错误: {e}")    
    #获取参考文献数据
    try:
        get_reference_data_from_semanticScholar.get_reference_data_from_semantic_scholar(shared_data.selected_file_path,shared_data.folder_reference_path)
        shared_data.folder_reference_meta_data = shared_data.temp
        csv_tran.csv_tran(shared_data.folder_reference_meta_data,shared_data.folder_reference_path)
        get_meta_data_from_semanticScholar.get_meta_data_from_semantic_scholar(shared_data.start_file_path,shared_data.folder_reference_path)
        shared_data.folder_reference_meta_data = shared_data.temp
        altmetric_api.get_altmetric(shared_data.folder_reference_meta_data)
        get_journal_rank_from_easyScholar.get_journal_rank_from_easyScholar(shared_data.folder_reference_meta_data)
        #os.remove(shared_data.start_file_path)
    except Exception as e:
        print(f"获取参考文献数据时出现错误: {e}")
    #获取施引文献数据
    try:
        get_citation_data_from_semanticScholar.get_citation_data_from_semantic_scholar(shared_data.selected_file_path,shared_data.folder_citation_path)
        shared_data.folder_citation_meta_data = shared_data.temp
        csv_tran.csv_tran(shared_data.folder_citation_meta_data,shared_data.folder_citation_path)
        get_meta_data_from_semanticScholar.get_meta_data_from_semantic_scholar(shared_data.start_file_path,shared_data.folder_citation_path)
        shared_data.folder_citation_meta_data = shared_data.temp
        altmetric_api.get_altmetric(shared_data.folder_citation_meta_data)
        get_journal_rank_from_easyScholar.get_journal_rank_from_easyScholar(shared_data.folder_citation_meta_data)
        #os.remove(shared_data.start_file_path)
    except Exception as e:
        print(f"获取施引文献数据时出现错误: {e}")
    if shared_data.is_get_co:
        #获取共引文献数据
        try:
            get_citation_data_from_semanticScholar.get_citation_data_from_semantic_scholar(
                shared_data.folder_reference_meta_data,
                shared_data.folder_coReference_path
                )
            shared_data.folder_coReference_meta_data = shared_data.temp
            csv_tran.csv_tran(shared_data.folder_coReference_meta_data,shared_data.folder_coReference_path)
            get_meta_data_from_semanticScholar.get_meta_data_from_semantic_scholar(shared_data.start_file_path,shared_data.folder_coReference_path)
            shared_data.folder_coReference_meta_data = shared_data.temp
            altmetric_api.get_altmetric(shared_data.folder_coReference_meta_data)
            get_journal_rank_from_easyScholar.get_journal_rank_from_easyScholar(shared_data.folder_coReference_meta_data)
            #os.remove(shared_data.start_file_path)
        except Exception as e:
            print(f"获取共引文献数据时出现错误: {e}")
        #获取共被引文献数据
        try:
            get_reference_data_from_semanticScholar.get_reference_data_from_semantic_scholar(
                shared_data.folder_citation_meta_data,
                shared_data.folder_coCitation_path
                )
            shared_data.folder_coCitation_meta_data = shared_data.temp
            csv_tran.csv_tran(shared_data.folder_coCitation_meta_data,shared_data.folder_coCitation_path)
            get_meta_data_from_semanticScholar.get_meta_data_from_semantic_scholar(shared_data.start_file_path,shared_data.folder_coCitation_path)
            shared_data.folder_coCitation_meta_data = shared_data.temp
            altmetric_api.get_altmetric(shared_data.folder_coCitation_meta_data)
            get_journal_rank_from_easyScholar.get_journal_rank_from_easyScholar(shared_data.folder_coCitation_meta_data)
            #os.remove(shared_data.start_file_path)
        except Exception as e:
            print(f"获取共被文献数据时出现错误: {e}")

    if shared_data.is_get_fulltext:
        #获取目标文献全文
        try:
            temp_test=os.path.join(shared_data.folder_target_path, 'doi_start.csv')
            if temp_test:
                shared_data.folder_target_meta_data = temp_test
            get_full_text_from_semanticScholar.download_papers_from_csv(shared_data.folder_target_meta_data,shared_data.folder_target_path)
            get_full_text_from_scihub.download_papers_from_scihub(shared_data.folder_target_path,shared_data.temp)
        except Exception as e:
            print(f"获取目标文献全文时出现错误: {e}")
        #获取参考文献全文
        try:
            temp_test=os.path.join(shared_data.folder_reference_path, 'doi_start.csv')
            if temp_test:
                shared_data.folder_reference_meta_data = temp_test
            get_full_text_from_semanticScholar.download_papers_from_csv(shared_data.folder_reference_meta_data,shared_data.folder_reference_path)
            get_full_text_from_scihub.download_papers_from_scihub(shared_data.folder_reference_path,shared_data.temp)
        except Exception as e:
            print(f"获取参考文献全文时出现错误: {e}")    
        #获取施引文献全文
        try:
            temp_test=os.path.join(shared_data.folder_citation_path, 'doi_start.csv')
            if temp_test:
                shared_data.folder_citation_meta_data = temp_test
            get_full_text_from_semanticScholar.download_papers_from_csv(shared_data.folder_citation_meta_data,shared_data.folder_citation_path)
            get_full_text_from_scihub.download_papers_from_scihub(shared_data.folder_citation_path,shared_data.temp)
        except Exception as e:
            print(f"获取施引文献全文时出现错误: {e}")

    if shared_data.is_get_co and shared_data.is_get_fulltext:
        try:
            temp_test=os.path.join(shared_data.folder_coReference_path, 'doi_start.csv')
            if temp_test:
                shared_data.folder_coReference_meta_data = temp_test
            get_full_text_from_semanticScholar.download_papers_from_csv(shared_data.folder_coReference_meta_data,shared_data.folder_coReference_path)
            get_full_text_from_scihub.download_papers_from_scihub(shared_data.folder_coReference_path,shared_data.temp)
        except Exception as e:
            print(f"获取共引文献全文时出现错误: {e}")
        try:
            temp_test=os.path.join(shared_data.folder_coCitation_path, 'doi_start.csv')
            if temp_test:
                shared_data.folder_coCitation_meta_data = temp_test
            get_full_text_from_semanticScholar.download_papers_from_csv(shared_data.folder_coCitation_meta_data,shared_data.folder_coCitation_path)
            get_full_text_from_scihub.download_papers_from_scihub(shared_data.folder_coCitation_path,shared_data.temp)
        except Exception as e:
            print(f"获取共被引文献全文时出现错误: {e}")

    print('任务已完成运行，请查看结果！')
