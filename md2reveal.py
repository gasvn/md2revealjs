#coding:utf-8
import os
import sys, os, argparse
import shutil
import cv2 as cv
from HTMLParser import HTMLParser
class ImageHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.path = "None"
		self.ratio=0
	def handle_starttag(self,tag,attrs):
		if tag == 'img':
			self.path=attrs[0][1]
			self.ratio=float(attrs[1][1][5:-1])/100
def resizeANDsave(mdroot,path,ratio):
	img=cv.imread(mdroot+path)
	#print path
	oh, ow, _ = img.shape
	nh=int(oh*ratio)
	nw=int(ow*ratio)
	img=cv.resize(img,(nw,nh), interpolation=cv.INTER_CUBIC)
	name=path.split('.')
	newpath=name[0]+'_html.'+name[1]
	cv.imwrite(mdroot+newpath,img)
	return '![]('+newpath+')\n'

def makeRjs(mdroot,revealjslib):

	os.system("cp -R "+revealjslib+". "+mdroot)
	print "copy revealjs libs to md root."

	md=open(mdroot+"index.md","r")
	html=open(mdroot+"index.html","r")
	htmlcontent = html.read()
	pos = htmlcontent.find("<div class=\"slides\">")+len("<div class=\"slides\">")
	if pos != -1:
		print "find insert position."
		print mdroot+"index.md"
		contentadd="\n"
		firstpage=True
		for eachline in md:
			if eachline== "\n":
				continue
			line=eachline.strip('\n')
			if firstpage and str(line)=="!page!":
				contentadd=contentadd+"<section data-markdown>"+"\n"+"<textarea data-template>"+"\n"
				firstpage=False
				print "new page"
			elif str(line)=="!page!":
				contentadd=contentadd+"</textarea>"+"\n"+"</section>"+"\n"
				contentadd=contentadd+"<section data-markdown>"+"\n"+"<textarea data-template>"+"\n"
				print "new page"
			else:
				img=ImageHTMLParser()
				img.feed(line)
				#print img.path,img.ratio
				if img.path!="None":
					eachline=resizeANDsave(mdroot,img.path,img.ratio)
					#print eachline
				contentadd=contentadd+eachline+"\n"
		# if md[-1]!="!page!":
		contentadd=contentadd+"</textarea>"+"\n"+"</section>"+"\n"
		#print contentadd
		htmlcontent = htmlcontent[:pos] + contentadd + htmlcontent[pos:]
		html=open(mdroot+"index.html","w")
		html.write(htmlcontent)
	html.close()
	print "done."

parser = argparse.ArgumentParser(description='Markdown to Revealjs.')
parser.add_argument('--root', type=str, help='mdroot', default="demo/")
args = parser.parse_args()
mdroot=args.root
revealjslib="reveal.js/"
makeRjs(mdroot,revealjslib)


