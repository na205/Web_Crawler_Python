import MySQLdb
import requests
import re
from urllib2 import urlopen,urlparse
import time
from bs4 import BeautifulSoup as bs
def func(url,title,doa,fileunder,time):
	db = MySQLdb.connect("localhost","root","naveen","test")
	cursor=db.cursor()
	try:
		cursor.execute("""INSERT INTO urldata VALUES(%s,%s,%s,%s,%s)""",(title,url,doa,fileunder,time))
		db.commit()
	except:
		db.rollback()
	db.close()
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
def isValidUrl(url):
	if regex.match(url) is not None:
        	return True;
    	return False
def crawl2(url,title):
	html=requests.get(page).text
	soup=bs(html)
        for info in soup.findAll('div', class_="post-info"):
		flag=True
		link,link1,under,under1,date="","","","",""
		for titleinfo in info.findAll('div',class_="post-title-info"):
			for posttitle in titleinfo.findAll('h2',class_="post-title"):
				link=posttitle.find('a',rel="bookmark")
				if link != None:
					link1=link.text
				db = MySQLdb.connect("localhost","root","naveen","test")
				cursor=db.cursor()
				try:
					if link != None:
						sql="SELECT * FROM urldata WHERE url = '%s'" % (link)
						cursor.execute(sql)
						res=cursor.fetchall()
						if len(res) > 0:
							flag=False
							break
				except:
					db.rollback()
				db.close()
			under=titleinfo.find('a',rel="category tag")
			if under != None:
				under=under.text
		date=info.find('div',class_="post-date").text
		if flag: func(link1,link,date,under,time.time())

url="http://www.geeksforgeeks.org"
clist=[url]
crawled=[]
while clist:
	page=clist.pop()
	html=requests.get(page).text
	soup=bs(html)
	tags=soup.findAll('a', class_="page larger")
	for l in tags:
		if l not in clist:
			clist.append(l['href'])
	if page not in crawled:
		crawl2(page,soup.title.string)
		crawled.append(page)
