1. 项目名称：paper_acquirer 
2. 项目简介：基于Python的文献元数据和原文获取工具，包装了数个API，可自动从多个文献数据库中获得相关信息，并自动下载文献全文。（新手上路，代码可算能动了，已经算意外之喜……）
   
3. 论文元信息字段：externalIds,DOI,Title,Authors,paperCount,citationCount,hIndex,Journal,journal_rank,SCI_IF,SCI_IF5,Fields of Study,Publication Date,Reference Count,Citation Count,Influential Citation Count,score,cited_by_fbwalls_count,cited_by_rdts_count,cited_by_tweeters_count,cited_by_wikipedia_count,cited_by_accounts_count,cited_by_feeds_count,cited_by_gplus_count,cited_by_posts_count,cited_by_msm_count,cited_by_delicious_count,cited_by_qs_count
   
4. 论文元数据数据库：Semantic Scholar、Altmetric、easyScholar

5. 论文原文获取：开源→Semantic Scholar
                 非开源→sci-hub

6. 参考信息来源：Semantic Scholar 官方说明→https://www.semanticscholar.org/product/api/tutorial
                 Altmetric 官方说明→https://api.altmetric.com/
                 easyScholar →https://www.easyscholar.cc/
                 Semantic Scholar官方API→https://github.com/allenai/s2-folks/tree/main
                 sci-hub非官方API→https://github.com/zaytoun/scihub.py


7. 项目运行环境：Python 3.6+ ；科学上网


# Journal_rank 缩写表格（from easyScholar）
缩写	   解释	                缩写	          解释	                    缩写	解释
swufe	   西南财经大学	        cqu	              重庆大学	                sciif	SCI影响因子-JCR
cufe	   中央财经大学	        nju	              南京大学	                sci	    SCI分区-JCR
uibe	   对外经济贸易大学	    xju	              新疆大学	                ssci	SSCI分区-JCR
sdufe	   山东财经大学	        cug	              中国地质大学	            jci	    JCI指数-JCR
xdu	       西安电子科技大学	    ccf	              中国计算机学会	        sciif5	SCI五年影响因子-JCR
swjtu	   西南交通大学	        cju	              长江大学（不是计量大学）	sciwarn	中科院预警
ruc	       中国人民大学	        zju	              浙江大学	                sciBase	SCI基础版分区-中科院
xmu	       厦门大学	            zhongguokejihexin 中国科技核心期刊	        sciUp	SCI升级版分区-中科院
sjtu	   上海交通大学	        fms	              FMS	                    ajg	    ABS学术期刊指南
fdu	       复旦大学	            utd24	          UTD24	                    ft50	FT50
hhu	       河海大学	            eii	              EI检索	                cscd	中国科学引文数据库
pku	       北大核心	            cssci	          南大核心	                ahci	A&HCI
scu	       四川大学	            sciUpSmall	      中科院升级版小类分区	    esi	    ESI学科分类
sciUpTop   中科院升级版Top分区	cpu	              中国药科大学	
