import os
#import whoosh
from whoosh import qparser
from whoosh.index import open_dir, create_in
from whoosh.scoring import TF_IDF, BM25F
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NUMERIC, NGRAMWORDS
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import StopFilter
from whoosh.lang.porter import stem



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

				title_page = hit['TitleOfPage']
				doc_num = hit['DocNumber']
				web_address = hit['WebAddress']
				st_time = hit['StartTime']
				fld_content = hit['FieldContent']
				score = hit.score

				#print("\n\n")
				#print(title_page,doc_num,web_address,st_time,fld_content, score, '\n')

				# should ideally be saving data from hit instead of list
				list3.append(dict(hit))
				#list3.append(list2[doc_num])
				#print("docnum = ",doc_num," list2 = ",list2[doc_num])
				#if i>=10:
					#break

	#print("documentNumber = ",documentNumber," list2.size = ",len(list2))
	#print("Search end.....\n\n")
	#print("list3 = ",list3)
	return list3

#searchResult=SearchTerm(queryString)
#print("Search result = ",searchResult)
#print("size = ",len(searchResult))
#print("output : max 10 records ,  list of list -> [  [Title-page, web-address, star-time, content], [], []   ]")
