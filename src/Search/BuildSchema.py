import os
#import whoosh
from whoosh import qparser
from whoosh.index import open_dir, create_in
from whoosh.scoring import TF_IDF, BM25F
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, NUMERIC, NGRAMWORDS
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import StopFilter
from whoosh.lang.porter import stem

from datetime import datetime

# building of the schema needs to be in a seperate script.
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
dirname = "indexdir"

if not os.path.exists(dirname):
    os.mkdir(dirname)

#build schema in whoosh
schema = Schema(
    DocNumber=NUMERIC(stored=True),
    TitleOfPage=TEXT(stored=True, phrase=True, sortable=False),
    WebAddress=TEXT(stored=True, phrase=True, sortable=False),
    StartTime=TEXT(stored=True, phrase=True, sortable=False),
	OriginalContent=TEXT(stored=True, phrase=True, sortable=False),
    FieldContent=NGRAMWORDS(minsize=2, maxsize=10,stored=True, field_boost=1.0, tokenizer=None, at='start', queryor=True, sortable=True),
)


# building of the schema needs to be in a seperate script.
#create index
ix = create_in(dirname, schema)
writer = ix.writer()


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
						startTime = datetime.strptime(startTime, "%M:%S")
						startTime = startTime.strftime('%S')
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
					#print("All fields : title_of_page = ",title_of_page," Doc-num = ",documentNumber,", webAddress = ", webAddress, ", st-time = ",startTime, ", fieldContent = ",fieldContentCleaned)
					#print("list2 = ",list2)
	#   			add documentNumber,webAddress, startTime, fieldContentCleaned to whoosh
					try:
						#print("writer.add_document working....")
						writer.add_document(TitleOfPage=title_of_page, DocNumber=documentNumber, WebAddress=webAddress, StartTime=startTime,OriginalContent=fieldContent, FieldContent=fieldContentCleaned)

					except:
						#print("writer.add_document did not work....")
						writer.add_document(TitleOfPage=title_of_page, DocNumber=documentNumber, WebAddress=u'None', StartTime=startTime, OriginalContent=fieldContent, FieldContent=u'None')

writer.commit()