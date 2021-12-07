import os
#import whoosh
from whoosh import qparser
from whoosh.index import open_dir, create_in
from whoosh.scoring import TF_IDF, BM25F
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NUMERIC, NGRAMWORDS
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import StopFilter
from whoosh.lang.porter import stem

import time
from datetime import datetime, timedelta


def dataClean(fieldData):
	#lowercase, stop words, extra word removal,stemming
	#print("main   "+fieldData)
	
	tokenizer = RegexTokenizer()
	
	#lowercase conversion
	fieldData=fieldData.lower()	
	
	#remove extra words
	for r in (("music", ""), ("sound", ""),("&gt","")):
		fieldData = fieldData.replace(*r)
    
	'''
 	#stemming with whoosh (from whoosh.analysis import StemFilter is needed)
	stream = tokenizer(fieldData)
	stemmer = StemFilter()
	data_clean=""
	for token in stemmer(stream):
		data_clean=data_clean+token.text+" "
	print(data_clean)
	'''

	
	#stop words with stopfilter in whoosh
	data_clean=""
	stopper = StopFilter() #stop word removal
	tokens = stopper(tokenizer(fieldData))
	
	#stemming with stem in whoosh
	for t in tokens:
		s=stem(t.text) #stem
		data_clean=data_clean+s+" "
	#print(data_clean)
	
	
	return data_clean
	


list3=[]
dirpath = os.path.dirname(os.path.abspath(__file__))
dirname = os.path.join(dirpath, "indexdir")

if not os.path.exists(dirname):
    os.mkdir(dirname)

#build schema in whoosh
# building of the schema needs to be in a seperate script.
schema = Schema(
    DocNumber=NUMERIC(stored=True),
    TitleOfPage=TEXT(stored=True, phrase=True, sortable=False),
    WebAddress=TEXT(stored=True, phrase=True, sortable=False),
    StartTime=TEXT(stored=True, phrase=True, sortable=False),
	OriginalContent=TEXT(stored=True, phrase=True, sortable=False),
    FieldContent=NGRAMWORDS(minsize=2, maxsize=10,stored=True, field_boost=1.0, tokenizer=None, at='start', queryor=True, sortable=True)
)

#   do eveything for whoosh
#print("documentNumber = ",documentNumber," list2.size = ",len(list2))
queryString = "compute these vectors exactly"


ix = open_dir(dirname)
qp = qparser.MultifieldParser(['TitleOfPage', 'DocNumber', 'WebAddress', 'StartTime', 'OriginalContent', 'FieldContent'], ix.schema, group=qparser.OrGroup)



w = BM25F(B=0.75, K1=1.5)


def SearchTerm(searchData):

	list3=[]
	query = qp.parse(dataClean(searchData))
	

	with ix.searcher(weighting=w) as searcher:
			#results = searcher.search(dataClean(searchData), terms=True)
		results = searcher.search(query, terms=True, limit=10)
		found_doc_num = results.scored_length()
	#	run_time = results.runtime

		#print("Search done found_doc_num = ",found_doc_num)

		
		if results:
			i=0
			for hit in results:
				i+=1

				hit = dict(hit)
				#print("\n\n")
				#print(title_page,doc_num,web_address,st_time,fld_content, score, '\n')
				
				# change time to seconds for formating
				st_time = time.strptime(hit['StartTime'], "%M:%S")
				st_time = str(int(timedelta(minutes=st_time.tm_min, seconds= st_time.tm_sec).total_seconds()))
				hit['st_time_vido'] = st_time

				# should ideally be saving data from hit instead of list
				list3.append(hit)

	return list3

