import tornado.ioloop
import tornado.web
import lxml
import urllib2
import httplib2
import xmltodict
import uuid
import base64
import binascii
import re
from lxml import etree, html

def extractUrl(url,decodeBase64Url,uuid,requestHost):
    filename = urllib2.unquote(decodeBase64Url).decode('utf8').split('/')[-1]
    fullUrlPath = decodeBase64Url.replace(filename,"")
	
    match = re.search(r'href=[\'"]?([^\'" >]+)', url)
    if match:
        result = match.group(0)
	result1=result.replace('href="','')
	if ".ico" in result1 or ".js" in result1 or ".css" in result1:
		if "http://" not in result1 and "https://" not in result1:
			newUrl = fullUrlPath+"/"+result1
			returnStr = url.replace(str(result.encode('utf-8')),'href="'+str(newUrl.encode('utf-8')))
		else:
			returnStr = url
	else:
		if "http://" not in result1 and "https://" not in result1:
		    	encodeUrl = base64.b64encode(fullUrlPath+"/"+result1)
			newUrl = "http://"+requestHost+"/query?uuid="+uuid+"&url="+encodeUrl
			returnStr = url.replace(str(result.encode('utf-8')),'href="'+str(newUrl.encode('utf-8')))
		else:
		    	encodeUrl = base64.b64encode(result1)
			newUrl = "http://'+requestHost+'/query?uuid="+uuid+"&url="+encodeUrl
			returnStr = url.replace(str(result.encode('utf-8')),'href="'+str(newUrl.encode('utf-8')))
	return returnStr

def getPageContents(url):
    h = httplib2.Http(".cache")
    resp, content = h.request(url, "GET")
    return content

def testUrl(url,search=re.compile(r'[^a-z0-9./:]#').search):
    return not bool(search(url))
	
class MainHandler(tornado.web.RequestHandler):
    def get(self):
	print self.request.remote_ip
	#self.write(self.request.remote_ip)

class AnswerHandler(tornado.web.RequestHandler):
    def get(self):
	#print self.request.uri
	#print self.request.host

	uuid = self.get_argument('uuid',True)
	base64Url = self.get_argument('url',True)
	decodeBase64Url = base64.b64decode(base64Url)
	if testUrl(decodeBase64Url)==True:
		html1 = getPageContents(decodeBase64Url)
		document_root = html.fromstring(html1)
		prettyHTML=etree.tostring(document_root, encoding='unicode', pretty_print=True)
		list1 = prettyHTML.split("\n")
		resultList=[]
		for x in list1:
			if 'href="' in x:
				resultList.append(str(extractUrl(str(x.encode('utf-8')),decodeBase64Url,uuid,self.request.host)))
			else:
				resultList.append(x.strip())
		for x in resultList:
			self.write(x)
	else:
		self.write("Invalid Url<br>")

if __name__ == "__main__":
    application = tornado.web.Application([
        #(r"/", MainHandler),
	(r"/query", AnswerHandler),
    ])
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
