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
	print(data_clean)
	
	
	return data_clean
	


list3=[]
dirname = "indexdir"

if not os.path.exists(dirname):
    os.mkdir(dirname)

#build schema in whoosh
schema = Schema(
    DocNumber=NUMERIC(stored=True),
    #DocNumber=ID(stored=True, unique=False),
    TitleOfPage=TEXT(stored=True, phrase=True, sortable=False),
    WebAddress=TEXT(stored=True, phrase=True, sortable=False),
    StartTime=TEXT(stored=True, phrase=True, sortable=False),
    #FieldContent=TEXT(analyzer=StemmingAnalyzer(), stored=True, phrase=True, sortable=True)
    FieldContent=NGRAMWORDS(minsize=2, maxsize=10,stored=True, field_boost=1.0, tokenizer=None, at='start', queryor=True, sortable=True)
)

#create index
ix = create_in(dirname, schema)
writer = ix.writer()


list1=[]
list2=[]
documentNumber = -1
title_of_page=''
webAddress=''
startTime =''
fieldContent =''
data_dir='../../data/cs-410/'
for filename in os.listdir(data_dir):
	#print('filename : ',filename)
	fileName=data_dir+filename
	#print('fileName : ',fileName)
	with open(fileName,'r') as f:
		lines=f.readlines()
		for ii in range(len(lines)):
			list1=[]
			if ii==0:
				title_of_page=''
				title_of_page=lines[ii].split('\n')[0].title()
				#list1.append(title_of_page)
				#print("list1 = ",list1)
			else:
				if ii==1:
					webAddress=''
					if lines[ii].lower().startswith("http"):
						webAddress=lines[ii].split('\n')[0]
					#list1.append(webAddress)
					#print("list1 = ",list1)
				else:
					#print("else part list1 = ",list1)
					xx=lines[ii].split(' : ')
					#print("xx = ",xx)
					if len(xx)>0:
						startTime=xx[0]
					else:
						startTime=''
					if len(xx)>1:
						fieldContent=xx[1]
					else:
						fieldContent=''
					#list1.append(startTime)
					#list1.append(fieldContent)
		
					#print("else 2nd part list1 = ",list1)
					#print("before documentNumber = ",documentNumber)
					documentNumber += 1
					#print("after documentNumber = ",documentNumber)
					#list2.append(list1)
					fieldContentCleaned =dataClean(fieldContent)
					list1.append(title_of_page)
					list1.append(webAddress)
					list1.append(startTime)
					list1.append(fieldContent)
					list2.append(list1)
					#print("All fields : title_of_page = ",title_of_page," Doc-num = ",documentNumber,", webAddress = ", webAddress, ", st-time = ",startTime, ", fieldContent = ",fieldContentCleaned)
					#print("list2 = ",list2)
	#   			add documentNumber,webAddress, startTime, fieldContentCleaned to whoosh
					try:
						#print("writer.add_document working....")
						writer.add_document(TitleOfPage=title_of_page, DocNumber=documentNumber, WebAddress=webAddress, StartTime=startTime, FieldContent=fieldContentCleaned,)
					except:
						#print("writer.add_document did not work....")
						writer.add_document(TitleOfPage=title_of_page, DocNumber=documentNumber, WebAddress=u'None', StartTime=startTime, FieldContent=u'None',)

writer.commit()
#   do eveything for whoosh
#print("documentNumber = ",documentNumber," list2.size = ",len(list2))

#queryString = " bM25 "
#queryString = " relevant document"
queryString = " similarity function "
#queryString = " simila funct "
#queryString = " funct simila"
#queryString = " function "
#queryString = "compute these vectors exactly"
#queryString = "vector"
#queryString = " bM25 "
#search_type = "BM25"


ix = open_dir(dirname)
qp = qparser.MultifieldParser(['TitleOfPage', 'DocNumber', 'WebAddress', 'StartTime', 'FieldContent'], ix.schema, group=qparser.OrGroup)

query = qp.parse(queryString)

w = BM25F(B=0.75, K1=1.5)

print("Search starting.....")
'''
with ix.searcher(weighting=w) as searcher:
	results = searcher.search(query, terms=True, limit=10)
	found_doc_num = results.scored_length()
#	run_time = results.runtime

	

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
			print("\n\n\n")
			print("In hit : ",title_page,doc_num,web_address,st_time,fld_content, score, '\n')
			list3.append(list2[doc_num])
			print("In hit : docnum = ",doc_num," list2 = ",list2[doc_num])
			#if i>=10:
			#		break
			
print("Search done found_doc_num = ",found_doc_num)
#print("documentNumber = ",documentNumber," list2.size = ",len(list2))
print("Search end.....\n\n")
print("list3 = ",list3)
#return list3
list3=[]
'''
def SearchTerm(searchData):

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
				list3.append(list2[doc_num])
				#print("docnum = ",doc_num," list2 = ",list2[doc_num])
				#if i>=10:
					#break

	#print("documentNumber = ",documentNumber," list2.size = ",len(list2))
	#print("Search end.....\n\n")
	#print("list3 = ",list3)
	return list3

searchResult=SearchTerm(queryString)
print("Search result = ",searchResult)
print("size = ",len(searchResult))
print("output : max 10 records ,  list of list -> [  [Title-page, web-address, star-time, content], [], []   ]")
