from html.parser import HTMLParser
from pathlib import Path
import re,json
class P(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.rows=[];self.row=None;self.capture=False
 def handle_starttag(self,t,a):
  d=dict(a);cl=d.get('class','')
  if t=='div':self.stack.append(cl)
  if t=='span' and 'kt-blocks-accordion-title'==cl:
   self.row={'title':'','parents':self.stack.copy(),'urls':[]};self.rows.append(self.row);self.capture=True
  if t=='a' and self.row and re.search(r'\.(pdf|docx?)(?:$|\?)',d.get('href',''),re.I):self.row['urls'].append(d['href'])
 def handle_endtag(self,t):
  if t=='div' and self.stack:self.stack.pop()
  if t=='span':self.capture=False
 def handle_data(self,d):
  if self.capture:self.row['title']+=d

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser(description='Inspecciona una captura del catálogo, sin cambiar IDs ni la biblioteca.')
 ap.add_argument('html',type=Path);a=ap.parse_args();p=P();p.feed(a.html.read_text());print(json.dumps(p.rows,ensure_ascii=False,indent=2))
