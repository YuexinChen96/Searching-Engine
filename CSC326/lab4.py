import bottle
#from autocorrect import spell
from bottle import *
import httplib2
import sqlite3
c_page = 0
dic = {}
urls = []
correct = False
c_word_l = ''
#first keyword


@get('/')
def home():
	c_page = 0
	return template('home_page')

@get('/keywords')
def create():
	global c_page
	global dic
	global urls
	global f_kw
	global correct
	global c_word_l
	urls = []
	#if correct:
	#	print 'cuo le'
	#	word_l = c_word_l.split(' ')
	#	f_kw = word_l[0]
	#else:
	keywords = request.query_string
	word_l = keywords.lower().replace('keyword=','').split('+')
	f_kw = word_l[0].split('=')[1]
	print f_kw
	word_l[0] = f_kw
	print word_l

	for x in word_l:
		temp = x
		'''if spell(x) != x:
			spell(x)
			correct = True
			print 'zhu zi hao'
		'''

	if not word_l:
		return template('error')
	for word in word_l:
		print word
		print 'lao mi'
		db = sqlite3.connect("Crawler.db")
		t_cursor = db.cursor()
		t_cursor.execute("select word_id from M_Lexicon where word = (?)", (word,))
		this_word_id = t_cursor.fetchone()
		if this_word_id:
			this_word_id = this_word_id[0]
			t_cursor.execute("select doc_ids from Inverted_Index where word_id = (?)", (this_word_id,))
			doc_ids = t_cursor.fetchone()[0]
			list_doc_ids = [int(e) for e in doc_ids.split()]
			page_rank_dict = {}
			for id in list_doc_ids:
				t_cursor.execute("select doc_id, page_rank from Page_Rank_Index where doc_id = (?)", (id,))
				rank_result = t_cursor.fetchone()
				if rank_result:
					page_rank_dict[rank_result[0]] = rank_result[1]
			print "reach here1"
			url_dict = {}
			for key in page_rank_dict:
				t_cursor.execute("select url from Document_Index where doc_id = (?)", (key,))
				url_result = t_cursor.fetchone()
				url_dict[url_result[0]] = page_rank_dict[key]
			db.close()
			final = []
			print "reach here2"
			for l in sorted(url_dict,key=url_dict.get,reverse=True):
				final.append(l)
			dic[f_kw] = {}
			print "reach here3"
			urls += final#---------------------------------------------assert backend
		else:
			print 'zha le'
			db.close()
			pass
	maxUrls = len(urls)
	if maxUrls/5 != 0:
		maxPage = int(maxUrls/5+1)
	else:
		maxPage = int(maxUrls/5)	
	page = 0
	count = 1
	try:
		for x in range(maxPage):
			dic[f_kw][x] = []
		for y in range(maxUrls):
			dic[f_kw][page].append(urls[y])
			if count%5 == 0:
				page += 1
			count += 1
		c_page = 1
		
		return template('lab4', pages = dic[f_kw], c_page = c_page, word = f_kw, flag = correct, word_l = c_word_l)
	except:
		return template('error')		
		

@get('/search')
def search():
	global c_page
	global dic
	global urls
	global f_kw
	maxNum = 1000000000
	exe = request.query_string
	print exe
	if exe == "%3E%3E=%3E%3E":
		c_page += 1
	elif exe == "%3C%3C=%3C%3C":
		c_page -= 1
	else:
		c_page = (int(exe.split('=')[1]))
	return template('lab4', pages = dic[f_kw], c_page = c_page, word = f_kw)
				

if __name__ == '__main__':
	run (host='localhost', port = 8080, reloader = True)
